## input_slang_utils.py

from gtts import gTTS
import playsound
import os
import cv2
import numpy as np
import time
import uuid

def speak_thai(text):
    print(f"- กำลังพูด: {text}")
    filename = f"responese_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='th')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)



def detect_motion(threshold=500000, timeout=5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ไม่สามารถเปิดกล้องได้")
        return False

    start_time = time.time()
    motion_detected = False

    while time.time() - start_time < timeout:
        ret, frame1 = cap.read()
        time.sleep(0.1)
        ret, frame2 = cap.read()
        if not ret:
            break

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        motion_score = np.sum(thresh)

        print(f"ตรวจสอบการเคลื่อนไหว (motion score): {motion_score}")
        if motion_score > threshold:
            motion_detected = True
            break

    cap.release()
    return motion_detected
