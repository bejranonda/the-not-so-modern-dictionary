import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import random
import json
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# โหลดฐานข้อมูลผู้ใช้
if os.path.exists("user_added_slang.json"):
    with open("user_added_slang.json", "r", encoding="utf-8") as f:
        database = json.load(f)
else:
    database = {}

# เสียงต่าง ๆ
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
    "error sound/error-call-to-attention-129258.mp3"
]

correct_sound = "correct sound/correct-6033.mp3"

def play_flipping():
    flipping = random.choice(flipping_sounds)
    print(f"- กำลังพลิกหนังสือ: {flipping}")
    playsound.playsound(flipping)


def speak_thai(text):
    print(f"- กำลังพูด: {text}")
    tts = gTTS(text=text, lang='th')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

def recognize_thai():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 กำลังฟัง...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            recog = recognizer.recognize_google(audio, language="th-TH").lower()
            print(f"- ฟังได้ว่า: {recog}")
            return recog
        except:
            playsound.playsound(random.choice(invalid_sounds))  # เพิ่มเสียงผิดพลาด
            speak_thai("ขออภัย ฟังไม่เข้าใจ")
            return recognize_thai()


def add_slang_flow():
    speak_thai("กรุณาพูดคำสแลงภาษาไทยที่คุณต้องการเพิ่ม")
    word = recognize_thai()
    speak_thai(f"คุณพูดว่า {word} ใช่ไหม ถ้าใช่พูดว่า ใช่ ถ้าไม่ใช่พูดว่า ไม่ใช่")
    confirm = recognize_thai()
    if "ไม่ใช่" in confirm:
        speak_thai("โปรดลองใหม่อีกครั้ง")
        return

    speak_thai(f"กรุณาพูดความหมายของคำว่า {word}")
    meaning = recognize_thai()
    speak_thai(f"คุณหมายถึง {meaning} ใช่ไหม")
    confirm_meaning = recognize_thai()
    if "ไม่ใช่" in confirm_meaning:
        speak_thai("โปรดลองใหม่อีกครั้ง")
        return

    speak_thai(f"กรุณาพูดตัวอย่างประโยคที่ใช้คำว่า {word}")
    example = recognize_thai()

    database[word] = {
        "meaning": meaning,
        "example": example
    }

    # เรียงตามตัวอักษรและบันทึก
    sorted_db = dict(sorted(database.items()))
    with open("user_added_slang.json", "w", encoding="utf-8") as f:
        json.dump(sorted_db, f, ensure_ascii=False, indent=2)

    # แสดงสรุป (จำลองใบพิมพ์)
    print("\n🖨️ ใบพิมพ์คำศัพท์")
    print(f"คำสแลง: {word}")
    print(f"ความหมาย: {meaning}")
    print(f"ตัวอย่าง: {example}")
    print("------------------------")

    speak_thai(f"บันทึกคำว่า {word} เรียบร้อยแล้ว ขอบคุณค่ะ")

def main_loop():
    for voice in voices:
        print(f"Voice: {voice.name}")

    while True:
        print("🚀 Starting AI")
        play_flipping()
        speak_thai("สวัสดีค่ะ ยินดีต้อนรับสู่พจนานุกรมคำสแลง คุณต้องการเพิ่มคำศัพท์ไหม")
        command = recognize_thai()
        if "เพิ่ม" in command or "ใช่" in command or "ต้องการ" in command:
            playsound.playsound(correct_sound)
            add_slang_flow()
        else:
            speak_thai("ขอบคุณค่ะ แล้วพบกันใหม่")
            # break

# เริ่มระบบ
main_loop()
