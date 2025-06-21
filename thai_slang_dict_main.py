## thai_slang_dict_main.py

#import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import random
import json
#import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import write
import tempfile
import subprocess
import signal
import sys
import platform



# user library
from slang_pdf_generator import printpdf
# from thai_slang_gui import start_gui_and_get_entry
from input_slang_utils import speak_thai, log_request_message, run_special_request_if_exists, run_routine_request_if_exists
from thai_slang_kiosk import SlangKiosk


# เรียก GUI kiosk
from PyQt5.QtWidgets import QApplication
import sys

# เสียงต่าง ๆ
flipping_sounds = ["flipping sound/pageturn-102978.mp3"]
invalid_sounds = ["error sound/error-call-to-attention-129258.mp3"]
correct_sound = "correct sound/correct-6033.mp3"
systemstart_sound = "systemstart sound/game-start-6104.mp3"
start_sound = "beep sound/point-smooth-beep-230573.mp3"
end_sound = "beep sound/short-beep-tone-47916.mp3"

# คำทักทาย
greeting_word  = [
    "สวัสดีจ้า ต้องการเพิ่มคำศัพท์ไหม",
    "Hi มาเพิ่มคำศัพท์กันไหม",
    "ลองเพิ่มคำศัพท์กันดีมะ",
    "ช่วยกันเพิ่มคำศัพท์กันได้ไหม",
    "มาเพิ่มศัพท์ไปด้วยกันไหม",
]

# คำบอกไม่เข้าใจ
notunderstand_word  = [
    "ไม่เข้าใจอ่ะ ช่วยพูดอีกที",
    "ไม่เข้าใจ พูดใหม่หน่อยนะ",
    "ไม่รู้เรื่อง พูดใหม่อีกที",
    "ช่วยพูดใหม่อีกทีนะ",
    "ช่วยพูดใหม่หน่อยนะ",
]

playsound.playsound(systemstart_sound)

# โหลดโมเดล Whisper
# whisper_model = whisper.load_model("small")

import shlex

def kill_previous_instance():
    current_pid = os.getpid()
    script_name = os.path.basename(__file__)
    script_path = os.path.abspath(__file__)  # ✅ เพิ่มบรรทัดนี้เพื่อใช้เปรียบเทียบ path
    system_platform = platform.system()
    print(f"Seeking double running: {system_platform}")
    print(f"current_pid: {current_pid}")
    print(f"script_name: {script_name}")
    print(f"script_name: {script_path}")
    try:
        if system_platform == "Windows":
            result = subprocess.run(["wmic", "process", "get", "ProcessId,CommandLine"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "python" in line and script_name in line and str(current_pid) not in line:
                    parts = line.strip().split()
                    if parts and parts[-1].isdigit():
                        pid = parts[-1]
                        print(f"🛑 Killing PID (Windows): {pid}")
                        subprocess.run(["taskkill", "/F", "/PID", pid])
            print("✅ No previous running (Windows)")
        else:
            # ✅ macOS: ใช้ lsof หา process ที่เปิดไฟล์ .py นี้
            result = subprocess.run(["lsof", "+D", os.path.dirname(script_path)], capture_output=True, text=True)
            found = False
            for line in result.stdout.strip().split("\n"):
                if script_path in line and f"{current_pid}" not in line:
                    try:
                        parts = line.split()
                        pid = int(parts[1])
                        print(f"🛑 Killing PID (Unix/macOS): {pid} → {line}")
                        os.kill(pid, signal.SIGKILL)
                        found = True
                    except Exception as e:
                        print(f"⚠️ Failed to parse or kill: {e}")
            if not found:
                print("✅ No previous running (Unix/macOS)")
    except Exception as e:
        print(f"❌ Error while trying to kill previous instance: {e}")

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
            playsound.playsound(random.choice(invalid_sounds))
            speak_thai(random.choice(notunderstand_word))
            return "เงียบ"

def recognize_thai_whisper():
    fs = 16000
    seconds = 3
    print("🎤 กำลังอัดเสียง (Whisper)...")
    try:
        audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        playsound.playsound(start_sound)
        sd.wait()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=".") as temp_file:
            temp_filename = temp_file.name
            playsound.playsound(end_sound)
            wavfile.write(temp_filename, fs, audio)
            print(f"- temp_filename: {temp_filename}")
        print("🧠 กำลังแปลงเสียงด้วย Whisper...")
        result = whisper_model.transcribe(temp_filename, language="th")
        text = result["text"].strip().lower()
        print(f"✅ ฟังได้ว่า: {text}")
        os.remove(temp_filename)
        return text
    except Exception as e:
        print(f"เกิดข้อผิดพลาดกับ Whisper: {e}")
        speak_thai("ระบบมีปัญหา")
        return recognize_thai_whisper()

def main_loop():
    try:
        printpdf(json_path="output/user_added_slang.json", output_path="output/slang_dictionary.pdf", thai_font_path="fonts/Kinnari.ttf", emoji_font_path="fonts/NotoEmoji-Regular.ttf")
        #exit()
        while True:
            print("🚀 Starting AI")
            play_flipping()
            kill_previous_instance()
            playsound.playsound(correct_sound)

            mode = "kiosk"
            if mode == "kiosk":
                app = QApplication(sys.argv)
                kiosk = SlangKiosk()
                kiosk.show()
                app.exec_()
            else:
                add_slang_gui_flow()

    except Exception as e:
        print(f"[ERROR] ระบบล้มเหลว: {e}")
        speak_thai("ระบบเกิดข้อผิดพลาด จะเริ่มใหม่ให้อัตโนมัติค่ะ")
        subprocess.run(["python", __file__])

# เริ่มระบบ
log_request_message("🛫")
log_request_message("🛫🛫 Starting App... 🛫🛫")
log_request_message("🛫")

run_special_request_if_exists()
got_jackpot = run_routine_request_if_exists()

main_loop()
