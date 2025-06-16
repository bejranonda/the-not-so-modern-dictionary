import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import difflib
import time  # เพิ่มโมดูลสำหรับการหน่วงเวลา
# from database_th import database
from database_politics import database

# ฟังก์ชัน: แปลงข้อความเป็นเสียงและเล่น
def speak_thai(text):
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
                print("ฟังไม่เข้าใจ")
            except sr.RequestError as e:
                print(f"เกิดข้อผิดพลาดกับบริการ: {e}")
            
            # เว้นระยะเวลาระหว่างการฟังเสียงใหม่
            print("----")
            # time.sleep(1)  # รอ 1 วินาที ก่อนที่จะฟังเสียงใหม่อีกครั้ง

# เรียกใช้งาน
listen_and_respond()
