import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import difflib
import time  # เพิ่มโมดูลสำหรับการหน่วงเวลา
# from database_th import database
from database_politics import database

import random
flipping_sounds = [
    "flipping sound/pageturn-102978.mp3",
    "flipping sound/turning-book-pages-and-paper-flipping-sfx-177393.mp3",
    "flipping sound/book-foley-turn-pages-2-189809.mp3",
    "flipping sound/book-page-flipping-6905.mp3",
    "flipping sound/flipping-book-101929.mp3",
    "flipping sound/flipping-novel-80266.mp3",
    "flipping sound/flipping-through-a-book-98901.mp3",
    "flipping sound/one-page-book-flip-101928.mp3"
]

invalid_sounds = [
    "error sound/error-call-to-attention-129258.mp3",
    # "error sound/error-warning-login-denied-132113.mp3",
    "error sound/fail-234710.mp3",
    "error sound/pc-speaker-error-beep-104100.mp3",
    # "error sound/system-error-notice-132470.mp3",
    # "error sound/error-2-126514.mp3",
    "error sound/error-4-199275.mp3",
    "error sound/error-9-206494.mp3",
    "error sound/error-10-206498.mp3",
]

correct_sound = "correct sound/correct-6033.mp3"

# ฟังก์ชัน: แปลงข้อความเป็นเสียงและเล่น
def speak_thai(text):
    # เล่นเสียงพลิกหน้าก่อน
    playsound.playsound(correct_sound)
    flipping = random.choice(flipping_sounds)
    playsound.playsound(flipping)
    
    # พูดคำตอบ
    tts = gTTS(text=text, lang='th')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

# ฟังก์ชัน: ฟังเสียงและตอบกลับ
def listen_and_respond():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("ระบบพร้อม ฟังเสียง...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print("รอฟังเสียง... พูดเป็นคำศัพท์ภาษาอังกฤษ")
            audio = recognizer.listen(source)
            try:
                # ใช้ภาษาที่เหมาะสม (อังกฤษ)
                text = recognizer.recognize_google(audio, language="en-US").lower()
                print(f"คุณพูดว่า: {text}")

                # ค้นหาคำใกล้เคียงที่สุด
                possible_keys = list(database.keys())
                close_matches = difflib.get_close_matches(text, possible_keys, n=1, cutoff=0.1)

                if close_matches:
                    match = close_matches[0]
                    response = database[match]
                else:
                    response = "ขออภัย ไม่พบคำใกล้เคียงในพจนานุกรม"

                print("ตอบกลับ:", response)
                speak_thai(response)

            except sr.UnknownValueError:
                invalidnotice = random.choice(invalid_sounds)
                playsound.playsound(invalidnotice)
                print("ฟังไม่เข้าใจ")
            except sr.RequestError as e:
                print(f"เกิดข้อผิดพลาดกับบริการ: {e}")
            
            # เว้นระยะเวลาระหว่างการฟังเสียงใหม่
            print("----")
            # time.sleep(1)  # รอ 1 วินาที ก่อนที่จะฟังเสียงใหม่อีกครั้ง

# เรียกใช้งาน
listen_and_respond()
