### request_routine.py

from input_slang_utils import speak_thai, speak_both, log_request_message, print_pdf_file, make_foldable_jackpot
import subprocess
from datetime import datetime
import random
import fitz  # PyMuPDF
import time

from playsound import playsound # Correct import: playsound is now the function directly
win_sound = "correct sound/8-bit-video-game-lose-sound-version-1-145828.mp3"

def routine_request():
    """คำสั่งพิเศษในการพิมพ์ จะรันเรื่อยที่เรียก ไม่มีการลบไฟล์นี้ทิ้ง"""
    
    output_path="output/slang_dictionary.pdf"
    
    print("⚙️ Running routine request...")
    log_request_message("⚙️ Running routine request...")
    
    got_jackpot = True

    # สร้าง lucky booklet ด้วยโอกาส 1 ใน 10
    jackpot_draw = random.randint(1, 100)
    print(f"🍀 jackpot_draw: {jackpot_draw}")
    log_request_message(f"🍀 jackpot_draw {jackpot_draw}")
    if jackpot_draw > 90:
        playsound(win_sound) # Corrected call
        speak_both("ว้าว ว้าว แจ๊กพอตแตกอีกแล้ว<br>Wow Wow, someone hit the jackpot!")
        output_jackpot = output_path.replace(".pdf", "_jackpot.pdf")
        make_foldable_jackpot(input_path=output_path, output_path=output_jackpot)
        print(f"..You got jackpot: {output_jackpot}")
        log_request_message(f"..You got jackpot: {output_jackpot}")

        print(f"Printing: {output_jackpot}")
        print_pdf_file(output_jackpot)
        log_request_message(f" ⚙️ print_pdf_file: {output_jackpot}")
        #greeting_lucky = "output/GreetingJackpot.pdf"
        #print_pdf_file(greeting_lucky)
        #print(f"Printing: {greeting_lucky}")
        #log_request_message(f" ⚙️ print_pdf_file: {greeting_lucky}")
        
        show_jackpot_popup(title = "<br>🎉🎉 Congratulation 🎉🎉<br>", message = "<br>คุณคือ 1 ในทุกๆ 10 คน ที่มีโชคในวันนี้<br>ที่จะเห็นปทานุกรมมากกว่า 1 หน้า<br>.. ขอให้ใช้โชคนี้ให้คุ้มค่า!<br><br><br>You are 1 in every 10 people lucky today<br>and unlocked access to more than just one page of our Lexicon.<br>.. use this chance wisely<br><br>", timeout=10000)

    else:
        print(f"..No Lucky Printing")
        log_request_message("..No Jackpot Printing")
        got_jackpot = False
            
    ############################
    ## First Request
    if (not got_jackpot) and True :
        # สร้าง lucky request ด้วยโอกาส 1 ใน 10
        request_draw = random.randint(1, 100)
        print(f"🍀 request_draw: {request_draw}")
        log_request_message(f"🍀 request_draw: {request_draw}")
        if request_draw > 85:
            playsound(win_sound) # Corrected call
            speak_both("คุณคือผู้โชคดี<br>You're lucky here")

            print(f"..request_draw meets criteria")
            log_request_message(f"..request_draw meets criteria")
            
            examples = get_random_latest_examples("output/user_added_slang.json", count=5)
            examples_text = " , .. , ".join(examples)
            examples_len = len(examples_text)
            print(f"📝 ตัวอย่างจากคำล่าสุด: {examples_text}")
            print(f"📝 ความยาว: {examples_len}")
            log_request_message(f"📝 ตัวอย่างจากคำล่าสุด: {examples_text}")
            log_request_message(f"📝 ความยาว: {examples_len}")
            time.sleep(3)
            speak_thai(examples_text)      
            show_jackpot_popup(title = "<br>🎉 Bonus for you only 🎉<br>", message = "<br>🌀 คุณคือหนึ่งในไม่กี่คน<br>ที่ถูกเลือกให้ได้ยินคำศัพท์ล่าสุดจากเรา<br>...ที่ยังไม่เคยปรากฏต่อสาธารณะ<br><br><br>🌀 You are one of the chosen few.<br>Today, you’ll hear a word we’ve never released before.<br><br>", timeout=examples_len*100+1500)
      
            
            # cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/EverWonderBooklet.pdf']
            # print(f"⚙️ Request1a: {' '.join(cmd1)}")
            # log_request_message(f"⚙️ Request1a: {' '.join(cmd1)}")

            # try:
                # output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
                # print("✅ Request1a success")
                # log_request_message(f"✅ Request1a success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
            # except subprocess.CalledProcessError as e:
                # print(f"❌ Request1a error: {e}")
                # log_request_message(f"❌ Request1a error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            # except Exception as e:
                # print(f"❌ Unexpected error in Request1a: {e}")
                # log_request_message(f"❌ Unexpected error in Request1a: {e}")

            # cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/EverWonderBooklet.pdf']
            # print(f"⚙️ Request1b: {' '.join(cmd1)}")
            # log_request_message(f"⚙️ Request1b: {' '.join(cmd1)}")

            # try:
                # output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
                # print("✅ Request1b success")
                # log_request_message(f"✅ Request1b success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
            # except subprocess.CalledProcessError as e:
                # print(f"❌ Request1b error: {e}")
                # log_request_message(f"❌ Request1b error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            # except Exception as e:
                # print(f"❌ Unexpected error in Request1b: {e}")
                # log_request_message(f"❌ Unexpected error in Request1b: {e}")
                
            got_jackpot = True
            
        else:
            print(f"..request_draw not enough")
            log_request_message(f"..request_draw not enough")


    ############################
    ## Second Request
    if (not got_jackpot) and False :
        cmd2 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/GreetingLuckyNo3.pdf']
        print(f"Request2: {' '.join(cmd2)}")
        log_request_message(f"🔧 cmd2: {' '.join(cmd2)}")

        try:
            output = subprocess.run(cmd2, check=True, capture_output=True, text=True)
            print("✅ Request2 success")
            log_request_message(f"✅ Request2 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request2 error: {e}")
            log_request_message(f"❌ Request2 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request2: {e}")
            log_request_message(f"❌ Unexpected error in Request2: {e}")



    ############################
    ## Third Request
    if False :
        #cmd3 = ['cmd', '/c', 'dir']
        cmd3 = ['ls', '-la', 'output']
        print(f"Request3: {' '.join(cmd3)}")
        log_request_message(f"🔧 cmd3: {' '.join(cmd3)}")

        try:
            output = subprocess.run(cmd3, check=True, capture_output=True, text=True)
            print("✅ Request1 success")
            log_request_message(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request3 error: {e}")
            log_request_message(f"❌ Request3 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request3: {e}")
            log_request_message(f"❌ Unexpected error in Request3: {e}")
            
            
    return got_jackpot
    
   

from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import sys

class JackpotPopup(QDialog):
    def __init__(self, title, message, timeout=10000, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # พื้นหลังหลักพร้อม padding ใหญ่
        content_widget = QWidget(self)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(60, 60, 60, 60)  # รอบกรอบดำ
        content_layout.setSpacing(20)
        content_widget.setStyleSheet("""
            background-color: rgba(0, 0, 0, 200);
            border-radius: 25px;
        """)

        # Wrapper สำหรับ title label (มี padding ซ้ายเพิ่ม)
        title_wrapper = QWidget()
        title_wrapper_layout = QVBoxLayout(title_wrapper)
        title_wrapper_layout.setContentsMargins(50, 0, 0, 0)  # padding-left
        title_label = QLabel(title)
        title_font = QFont("Arial", 34, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        title_wrapper_layout.addWidget(title_label)

        # Wrapper สำหรับ message label (มี padding ซ้ายเพิ่ม)
        message_wrapper = QWidget()
        message_layout = QVBoxLayout(message_wrapper)
        message_layout.setContentsMargins(50, 0, 0, 0)  # padding-left
        message_label = QLabel(message)
        message_font = QFont("Arial", 28)
        message_label.setFont(message_font)
        message_label.setStyleSheet("color: white;")
        message_label.setWordWrap(True)
        message_layout.addWidget(message_label)

        content_layout.addWidget(title_wrapper)
        content_layout.addWidget(message_wrapper)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.resize(700, 400)

        # ขยับให้สูงขึ้น
        screen = QApplication.primaryScreen().availableGeometry()
        center = screen.center() - self.rect().center()
        center.setY(center.y() - 150)
        self.move(center)

        QTimer.singleShot(timeout, self.close)

def show_jackpot_popup(title="🎉 ยินดีด้วย! Congratulation", message="แจ๊กพอตแตก\nJackpot!", timeout=10000):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    popup = JackpotPopup(title, message, timeout)
    popup.exec_()


import random
from typing import List
import os
import json

def get_random_latest_examples(json_path: str, count: int = 5) -> List[str]:
    """
    ดึงตัวอย่าง (example) แบบสุ่มจาก 10 คำล่าสุด

    Args:
        json_path (str): path ไปยังไฟล์ JSON ที่เก็บข้อมูลคำศัพท์
        count (int): จำนวนตัวอย่างที่ต้องการ (default = 5)

    Returns:
        List[str]: รายการประโยคตัวอย่างที่สุ่มแล้ว
    """
    if not os.path.exists(json_path):
        print(f"❌ ไม่พบไฟล์ JSON: {json_path}")
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # เรียงคำตาม update ล่าสุด แล้วเลือก 10 คำ
    latest_entries = sorted(
        data.items(),
        key=lambda x: x[1].get("update", ""),
        reverse=True
    )[:10]

    # รวมตัวอย่างทั้งหมดจาก 10 คำนี้
    all_examples = []
    for _, info in latest_entries:
        example_field = info.get("example", [])
        if isinstance(example_field, str):
            all_examples.append(example_field)
        elif isinstance(example_field, list):
            all_examples.extend(example_field)

    # สุ่มตัวอย่างจากทั้งหมด
    return random.sample(all_examples, min(count, len(all_examples)))

