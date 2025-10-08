import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from database_th import database

# ฟังก์ชัน: แปลงข้อความเป็นเสียงและเล่น
def speak_thai(text):
    print(f"ตอบกลับ: {text}")  # เพิ่มการดีบักเพื่อดูข้อความที่ตอบ
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
            print("รอฟังเสียง...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="th-TH")
                print(f"คุณพูดว่า: {text}")

                response = "ขออภัย ผมไม่เข้าใจ"

                for key in database:
                    if key in text:
                        response = database[key]
                        break

                print("ตอบกลับ:", response)
                speak_thai(response)

            except sr.UnknownValueError:
                print("ฟังไม่เข้าใจ")
            except sr.RequestError as e:
                print(f"เกิดข้อผิดพลาดกับบริการ: {e}")

listen_and_respond()
