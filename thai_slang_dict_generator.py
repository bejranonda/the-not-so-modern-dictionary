# thai_slang_dict_generator.py

import speech_recognition as sr
from gtts import gTTS
# from pydub import AudioSegment
import playsound
import os
import random
import json
# Updated code to replace recognize_google with Whisper + microphone

import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import write 
import tempfile

from slang_pdf_generator import printpdf

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text


console = Console()


# เสียงต่าง ๆ
# flipping_sounds = [
    # "flipping sound/pageturn-102978.mp3",
    # "flipping sound/turning-book-pages-and-paper-flipping-sfx-177393.mp3",
    # "flipping sound/book-foley-turn-pages-2-189809.mp3",
    # "flipping sound/book-page-flipping-6905.mp3",
    # "flipping sound/flipping-book-101929.mp3",
    # "flipping sound/flipping-novel-80266.mp3",
    # "flipping sound/flipping-through-a-book-98901.mp3",
    # "flipping sound/one-page-book-flip-101928.mp3"
# ]
flipping_sounds = ["flipping sound/pageturn-102978.mp3"]
invalid_sounds = [
    "error sound/error-call-to-attention-129258.mp3",
]
correct_sound = "correct sound/correct-6033.mp3"
systemstart_sound = "systemstart sound/game-start-6104.mp3"
start_sound = "beep sound/point-smooth-beep-230573.mp3"
end_sound = "beep sound/short-beep-tone-47916.mp3"


## Words
greeting_word  = [
    "สวัสดีจ้า ต้องการเพิ่มคำศัพท์ไหม",
    "Hi มาเพิ่มคำศัพท์กันไหม",
    "ลองเพิ่มคำศัพท์กันดีมะ",
    "ช่วยกันเพิ่มคำศัพท์กันได้ไหม",
    "มาเพิ่มศัพท์ไปด้วยกันไหม",
]

notunderstand_word  = [
    "ไม่เข้าใจอ่ะ ช่วยพูดอีกที",
    "ไม่เข้าใจ พูดใหม่หน่อยนะ",
    "ไม่รู้เรื่อง พูดใหม่อีกที",
    "ช่วยพูดใหม่อีกทีนะ",
    "ช่วยพูดใหม่หน่อยนะ",
]

playsound.playsound(systemstart_sound)

# โหลดโมเดล Whisper หนึ่งครั้ง (เช่น 'small' หรือ 'base')
#whisper_model = whisper.load_model("small")

# โหลดฐานข้อมูลผู้ใช้
if os.path.exists("user_added_slang.json"):
    with open("user_added_slang.json", "r", encoding="utf-8") as f:
        database = json.load(f)
else:
    database = {}
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
        playsound.playsound(start_sound)
        audio = recognizer.listen(source)
        try:
            recog = recognizer.recognize_google(audio, language="th-TH")
            print(f"- ฟังได้ว่า: {recog}")
            return recog
        except:
            playsound.playsound(random.choice(invalid_sounds))  # เพิ่มเสียงผิดพลาด
            speak_thai(random.choice(notunderstand_word))
            return recognize_thai()

def recognize_thai_whisper():
    fs = 16000
    seconds = 3
    print("🎤 กำลังอัดเสียง (Whisper)...")

    try:
        audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        playsound.playsound(start_sound)
        sd.wait()

        # ใช้ tempfile เพื่อสร้างไฟล์ .wav ชั่วคราว
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=".") as temp_file:
            temp_filename = temp_file.name
            playsound.playsound(end_sound)

            wavfile.write(temp_filename, fs, audio)
            print(f"- temp_filename: {temp_filename}")

        print("🧠 กำลังแปลงเสียงด้วย Whisper...")
        result = whisper_model.transcribe(temp_filename, language="th")

        text = result["text"].strip().lower()
        print(f"✅ ฟังได้ว่า: {text}")

        os.remove(temp_filename)  # ลบไฟล์หลังใช้งาน
        return text
    except Exception as e:
        print(f"เกิดข้อผิดพลาดกับ Whisper: {e}")
        speak_thai("ระบบมีปัญหา")
        return recognize_thai_whisper()

def add_slang_flow():
    speak_thai("กรุณาพูดคำสแลงที่ต้องการเพิ่ม")
    #word = recognize_thai()
    console.clear()
    console.print(Panel.fit("📚 [bold magenta]เพิ่มคำสแลงใหม่เข้าสู่พจนานุกรม[/bold magenta]", title="🎤 Thai Slang Dictionary"))

    word = Prompt.ask("📝 [bold green]กรุณาพิมพ์คำสแลงที่ต้องการเพิ่ม[/bold green]").strip()
    # word = recognize_thai_whisper()
    speak_thai(f"พูดว่า {word} ใช่ไหม ถ้าใช่พูดว่า ใช่ ถ้าไม่ใช่พูดว่า ไม่ใช่")
    confirm = recognize_thai()
    if "ไม่" in confirm:
        speak_thai("ช่วยลองใหม่อีกครั้ง")
        return add_slang_flow()

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
    
    
    speak_thai("ต้องการพิมพ์พจนานุกรมของคุณหรือไม่")
    confirm = recognize_thai()
    if "ไม่" in confirm:
        speak_thai("ขอบคุณค่ะ แล้วพบกันใหม่")
        return
    else:
        playsound.playsound(correct_sound)
        printpdf()


def main_loop():
    # playsound.playsound(systemstart_sound)
    # speak_thai("กำลังเริ่มต้นระบบ")
    printpdf(
        json_path="user_added_slang.json",
        output_path="output/slang_dictionary.pdf",
        thai_font_path="fonts/THSarabunNew.ttf",
        emoji_font_path="fonts/NotoEmoji-Regular.ttf"
    )
    while True:
        print("🚀 Starting AI")
        play_flipping()
        greeting = random.choice(greeting_word)
        speak_thai(greeting)
        # command = recognize_thai()
        #command = recognize_thai_whisper()

        console.clear()
        title_text = Text("📚 เพิ่มคำสแลงใหม่เข้าสู่พจนานุกรม", style="bold magenta", justify="center")
        console.print(Panel(title_text, title="🎤 Thai Slang Dictionary", border_style="bright_blue"))

        console.print(Panel.fit("📚 [bold magenta]เพิ่มคำสแลงใหม่เข้าสู่พจนานุกรม[/bold magenta]", title="🎤 Thai Slang Dictionary"))

        command = Prompt.ask(f"📝 [bold green]{greeting}[/bold green]").strip()
        
        if "ไม่" in command or "no" in command or "ม่าย" in command:
            speak_thai("ขอบคุณค่ะ แล้วพบกันใหม่")
            # break
        else:
            playsound.playsound(correct_sound)
            add_slang_flow()


# เริ่มระบบ
main_loop()
