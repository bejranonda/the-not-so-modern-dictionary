import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import difflib
import random
import json

# โหลดฐานข้อมูลเดิม
try:
    from database_politics import database  # ใช้ถ้ามีฐานข้อมูลหลัก
except ImportError:
    database = {}

# โหลดฐานข้อมูลที่ผู้ใช้เคยเพิ่มไว้
if os.path.exists("user_added_dict.json"):
    with open("user_added_dict.json", "r", encoding="utf-8") as f:
        user_db = json.load(f)
        database.update(user_db)

# เสียงต่าง ๆ
flipping_sounds = [
    "flipping sound/pageturn-102978.mp3",
    "flipping sound/turning-book-pages-and-paper-flipping-sfx-177393.mp3",
    "flipping sound/book-page-flipping-6905.mp3"
]

invalid_sounds = [
    "error sound/error-call-to-attention-129258.mp3",
    "error sound/fail-234710.mp3",
    "error sound/pc-speaker-error-beep-104100.mp3"
]

correct_sound = "correct sound/correct-6033.mp3"

# ฟังก์ชันพูด
def speak_thai(text):
    playsound.playsound(correct_sound)
    flipping = random.choice(flipping_sounds)
    playsound.playsound(flipping)
    tts = gTTS(text=text, lang='th')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

# ฟังก์ชันรับเสียงภาษาอังกฤษ
def recognize_english():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("กำลังฟัง (EN)...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="en-US").lower()
        except:
            speak_thai("ขออภัย ฟังไม่เข้าใจ")
            return recognize_english()

# ฟังก์ชันรับเสียงภาษาไทย
def recognize_thai():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("กำลังฟัง (TH)...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="th-TH").lower()
        except:
            speak_thai("ขออภัย ฟังไม่เข้าใจ")
            return recognize_thai()

# ฟังก์ชันค้นหาคำ
def search_word_flow():
    speak_thai("กรุณาพูดคำศัพท์ภาษาอังกฤษที่คุณต้องการค้นหา")
    word = recognize_english()
    possible_keys = list(database.keys())
    close_matches = difflib.get_close_matches(word, possible_keys, n=1, cutoff=0.1)

    if close_matches:
        match = close_matches[0]
        response = database[match]
    else:
        response = "ขออภัย ไม่พบคำใกล้เคียงในพจนานุกรม"

    speak_thai(f"คำว่า {word}: {response}")

# ฟังก์ชันเพิ่มคำใหม่
def add_new_word_flow():
    speak_thai("กรุณาพูดคำศัพท์ภาษาอังกฤษที่คุณต้องการเพิ่ม")
    word = recognize_english()
    speak_thai(f"คุณพูดว่า {word} ใช่ไหมคะ ถ้าใช่พูดว่า ใช่ ถ้าไม่ใช่พูดว่า ไม่ใช่")
    confirm = recognize_thai()
    if "ไม่ใช่" in confirm:
        speak_thai("โปรดลองใหม่อีกครั้ง")
        return

    speak_thai(f"กรุณาพูดความหมายของคำว่า {word} เป็นภาษาไทย")
    meaning = recognize_thai()
    speak_thai(f"คุณหมายถึง {meaning} ใช่ไหมคะ")
    confirm_meaning = recognize_thai()
    if "ไม่ใช่" in confirm_meaning:
        speak_thai("โปรดลองใหม่อีกครั้ง")
        return

    speak_thai(f"กรุณาพูดตัวอย่างประโยคที่ใช้คำว่า {word}")
    example = recognize_thai()
    full_text = f"{meaning} ตัวอย่าง: {example}"

    # อัปเดต database และบันทึก
    database[word] = full_text

    # จัดเรียงตามตัวอักษร
    sorted_db = dict(sorted(database.items()))
    with open("user_added_dict.json", "w", encoding="utf-8") as f:
        json.dump(sorted_db, f, ensure_ascii=False, indent=2)

    # พิมพ์สรุป (จำลองการพิมพ์)
    print("\n🖨️ พิมพ์หน้าสรุป")
    print(f"คำศัพท์: {word}")
    print(f"ความหมาย: {meaning}")
    print(f"ตัวอย่าง: {example}")
    print("------------------------")

    speak_thai(f"บันทึกคำว่า {word} เรียบร้อยแล้ว ขอบคุณค่ะ")

# วนลูปรับผู้ใช้
def main_loop():
    while True:
        print("🚀 Starting AI")
        speak_thai("สวัสดีค่ะ คุณต้องการค้นหาคำศัพท์ หรือ เพิ่มคำศัพท์ใหม่ กรุณาพูดว่า ค้นหา หรือ เพิ่ม")
        command = recognize_thai()
        if "ค้นหา" in command:
            search_word_flow()
        elif "เพิ่ม" in command:
            add_new_word_flow()
        else:
            invalid = random.choice(invalid_sounds)
            playsound.playsound(invalid)
            speak_thai("ไม่เข้าใจคำสั่ง กรุณาพูดว่า ค้นหา หรือ เพิ่ม")

# เริ่มระบบ
main_loop()
