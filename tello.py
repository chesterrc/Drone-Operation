
import math
import threading
import time
from multiprocessing import Queue

import cv2
import ffmpeg
from djitellopy import Tello


def process_img():
    frame = tello.get_frame_read()
    if frame:
        time.sleep(1)
        if not frame_lock.locked():
            frame_lock.acquire()
            img_frame.put(frame)
            frame_lock.release()

def video():
    while True:
        if not frame_lock.locked():
            frame_lock.acquire()
            img = img_frame.get()
            frame_lock.release()
        if img is not None:
            cv2.imshow("Drone", img)
        
        #gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #apply histogram equalization
        #equalized = cv2.equalizeHist(gray_scale)
    

def movement():
    while True:
        key = cv2.waitKey(1) & 0xff
        if key == 27: # ESC
            tello.land()
        elif key == ord('w'):
            tello.move_forward(30)
        elif key == ord('s'):
            tello.move_back(30)
        elif key == ord('a'):
            tello.move_left(30)
        elif key == ord('d'):
            tello.move_right(30)
        elif key == ord('e'):
            tello.rotate_clockwise(30)
        elif key == ord('q'):
            tello.rotate_counter_clockwise(30)
        elif key == ord('r'):
            tello.move_up(30)
        elif key == ord('f'):
            tello.move_down(30)

if __name__ == "__main__":
    tello = Tello()
    #setup connection
    tello.connect()
    #start video
    tello.streamon()
    #buffer for img frame storage
    global img_frame
    img_frame = Queue()

    #locks for buffer
    frame_lock = threading.Lock()
    #implement treads
    t1 = threading.Thread(target=process_img)
    t2 = threading.Thread(target=video)
    t3 = threading.Thread(target=movement)
    
    
    t1.start()
    t2.start()
    t3.start()

    tello.takeoff()
    while True:
        pass