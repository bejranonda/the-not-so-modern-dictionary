## input_slang_utils.py

from gtts import gTTS
import playsound
import os
import cv2
import numpy as np
import time
import uuid
import threading


def speak_thai(text):
    def play():
        try:
            filename = f"temp_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=text, lang='th')
            tts.save(filename)
            playsound.playsound(filename)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    threading.Thread(target=play, daemon=True).start()

def speak_both(text):
    def play():
        try:
            if '<br>' in text:
                thai_part, eng_part = text.split('<br>', 1)
            else:
                thai_part, eng_part = text, ''

            files = []

            if thai_part.strip():
                filename_th = f"temp_{uuid.uuid4().hex}_th.mp3"
                tts_th = gTTS(text=thai_part.strip(), lang='th')
                tts_th.save(filename_th)
                files.append(filename_th)

            if eng_part.strip():
                filename_en = f"temp_{uuid.uuid4().hex}_en.mp3"
                tts_en = gTTS(text=eng_part.strip(), lang='en')
                tts_en.save(filename_en)
                files.append(filename_en)

            for file in files:
                playsound.playsound(file)

        finally:
            for file in files:
                if os.path.exists(file):
                    os.remove(file)

    threading.Thread(target=play, daemon=True).start()


def detect_motion(threshold=1000000, timeout=5):
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
