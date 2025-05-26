# input_slang_kiosk.py

import sys
import json
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import playsound
from datetime import datetime

from input_slang_utils import speak_thai, detect_motion
from slang_pdf_generator import printpdf

greeting_word = [
    "สวัสดีจ้า ต้องการเพิ่มคำศัพท์ไหม",
    "Hi มาเพิ่มคำศัพท์กันไหม",
    "ลองเพิ่มคำศัพท์กันดีมะ",
    "ช่วยกันเพิ่มคำศัพท์กันได้ไหม",
    "มาเพิ่มศัพท์ไปด้วยกันไหม",
]

correct_sound = "correct sound/correct-6033.mp3"
systemstart_sound = "systemstart sound/game-start-6104.mp3"
start_sound = "beep sound/point-smooth-beep-230573.mp3"
end_sound = "beep sound/short-beep-tone-47916.mp3"

ideal_warning = 30 * 1000 # mil.second to announce warning before reset
reset_warning = 60 * 1000 # mil.second to go to reset

class CustomLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.kiosk = parent

    def keyPressEvent(self, event):
        self.kiosk.reset_idle_timer()
        if event.key() == Qt.Key_Escape and self.kiosk.step in [1, 2, 3, 4, 5]:
            self.kiosk.label.setText("❌ ยกเลิก กำลังกลับเริ่มโปรแกรมใหม่...")
            playsound.playsound(end_sound)
            QTimer.singleShot(1000, self.kiosk.show_standby)
        elif self.kiosk.step == -1:
            self.kiosk.go_to_greeting()
        else:
            super().keyPressEvent(event)


class SlangKiosk(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 Your Thai Slang Dictionary - Kiosk Mode")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.data = {}
        self.step = -1
        self.warning_shown = False
        self.init_ui()

        self.motion_timer = QTimer()
        self.motion_timer.timeout.connect(self.check_motion)
        self.motion_timer.start(1000)

        self.idle_timer = QTimer()
        self.idle_timer.setInterval(ideal_warning)
        self.idle_timer.timeout.connect(self.handle_idle_timeout)

        self.warning_timer = QTimer()
        self.warning_timer.setInterval(reset_warning)
        self.warning_timer.timeout.connect(self.go_to_standby)

        QTimer.singleShot(500, self.show_standby)

    def reset_idle_timer(self):
        if self.step >= 0:
            self.idle_timer.stop()
            self.idle_timer.start()
            # เตือนแล้ว ก็ไม่ต้องรีเซ็ต warning_timer ซ้ำ
            if not self.warning_shown:
                self.warning_timer.stop()


    def init_ui(self):
        self.setStyleSheet("""
            QLabel#HeaderLabel {
                font-size: 48px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#DescLabel {
                font-size: 24px;
                color: #dddddd;
            }
            QLineEdit {
                font-size: 36px;
                padding: 20px;
                border: 3px solid #0078d7;
                border-radius: 20px;
                background-color: #ffffff;
                color: #f5f5f5;
            }
        """)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#282c34"))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(30)
        self.layout.setAlignment(Qt.AlignCenter)

        self.header = QLabel("📘 Your Thai Slang Dictionary")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignCenter)

        self.description = QLabel("เพิ่มคำสแลง ให้กับพจนานุกรมของคุณ 📝✨")
        self.description.setObjectName("DescLabel")
        self.description.setAlignment(Qt.AlignCenter)

        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #3c4048; border-radius: 30px; padding: 50px;")
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; color: white;")

        self.input = CustomLineEdit(self)
        self.input.returnPressed.connect(self.next_step)

        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.input)
        self.frame.setLayout(self.frame_layout)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)
        self.input.setFocus()

    def show_standby(self):
        self.step = -1
        self.input.clear()
        greeting = random.choice(greeting_word)
        self.label.setText("👋 " + greeting + "\n\nกดคีย์ใดก็ได้เพื่อเริ่ม")
        #self.setStyleSheet("QWidget { background-color: #103366; }")
        self.frame.setStyleSheet("background-color: #20232a; border-radius: 30px; padding: 50px;")
        QTimer.singleShot(100, lambda: speak_thai(random.choice(greeting_word)))
        self.idle_timer.stop()
        self.warning_timer.stop()

    def go_to_standby(self):
        self.label.setText("⌛️ ไม่ได้ใช้งานนาน กำลังกลับไปหน้าเริ่มต้น...")
        playsound.playsound(end_sound)
        QTimer.singleShot(1000, self.show_standby) 

    def check_motion(self):
        if self.step == -1 and detect_motion():
            self.go_to_greeting()

    def handle_idle_timeout(self):
        if self.step == 0:
            self.go_to_standby()
        elif self.step >= 1:
            if not self.warning_shown:
                self.label.setText("⚠️ หากไม่มีการกรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที")
                speak_thai("หากไม่มีการกรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที")
                self.warning_shown = True
                self.warning_timer.start()
            else:
                # ถ้าเตือนแล้ว แต่ไม่มี input ต่อ ก็จะกลับไป standby
                self.go_to_standby()

    def go_to_greeting(self):
        self.step = 0
        playsound.playsound(correct_sound)
        greeting = random.choice(greeting_word)
        #self.setStyleSheet("QWidget { background-color: #003366; }")
        self.frame.setStyleSheet("background-color: #004080; border-radius: 30px; padding: 50px;")
        self.label.setText(
            "<div style='font-size:40px;'>" + "👋 " + greeting + "<br><br>"
            "<span style='font-size:32px;'>ใส่คำสแลงของคุณ ความหมาย ตัวอย่าง เข้าไปในพจนานุกรมได้เลย</span><br><br><br>"
            "<span style='font-size:40px;'>กด Enter เพื่อดำเนินการ</span></div>"
        )
        print(f"- greeting: {greeting}")
        self.input.clear()
        QTimer.singleShot(100, lambda: speak_thai(greeting))
        #QTimer.singleShot(2000, lambda: speak_thai("จากนี้คุณสามารถใส่คำสแลง ความหมาย และตัวอย่างได้"))
        self.reset_idle_timer()

    def go_to_word_input(self):
        self.step = 1
        self.input.clear()
        playsound.playsound(correct_sound)
        self.label.setText(
            "<div style='font-size:40px;'>🖊️ พิมพ์คำสแลง แล้วกด Enter<br><br>"
            "<span style='font-size:32px;'>ตัวอย่างเช่น ‘แจ่มแมว’ หรือ ‘เกียม’</span><br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์คำสแลง"))
        self.reset_idle_timer()

    def go_to_meaning_input(self):
        self.step = 2
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>📖 พิมพ์ความหมาย แล้วกด Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ความหมาย"))
        self.reset_idle_timer()

    def go_to_example_input(self):
        self.step = 3
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>💬 พิมพ์ตัวอย่างประโยค แล้วกด Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ตัวอย่างประโยค"))
        self.reset_idle_timer()

    def go_to_summary(self):
        self.step = 4
        word = self.data["word"]
        meaning = self.data["meaning"]
        example = self.data["example"]
        summary = f"{word}\n📖 ความหมาย: {meaning}\n💬 ตัวอย่าง: {example}\n\nกด Enter เพื่อยืนยัน หรือ Esc เพื่อเริ่มใหม่"
        print(f"- summary: {summary}")
        self.label.setText(summary)
        QTimer.singleShot(300, lambda: speak_thai(f"{word}  หมายถึง {meaning}  เช่น {example}"))
        self.reset_idle_timer()

    def go_to_print_option(self):
        self.step = 5
        self.input.clear()
        self.label.setText("🖨️ ต้องการพิมพ์ออกมาไหม? (พิมพ์ 'ใช่' หรือกด Esc เพื่อข้าม)")
        QTimer.singleShot(300, lambda: speak_thai("ต้องการพิมพ์ออกมาไหม"))
        self.reset_idle_timer()

    def next_step(self):
        text = self.input.text().strip()
        print(f"- Step: {self.step}")
        if self.step == 0:
            self.go_to_word_input()
        elif self.step == 1:
            self.data["word"] = text
            self.go_to_meaning_input()
        elif self.step == 2:
            self.data["meaning"] = text
            self.go_to_example_input()
        elif self.step == 3:
            self.data["example"] = text
            self.go_to_summary()
        elif self.step == 4:
            self.save_data()
            self.go_to_print_option()
        elif self.step == 5:
            if text == "ใช่":
                printpdf(self.data["word"], self.data["meaning"], self.data["example"])
                self.label.setText("🖨️ กำลังพิมพ์ออกมา...")
                QTimer.singleShot(3000, self.show_standby)
            else:
                self.show_standby()
        self.input.clear()
        self.reset_idle_timer()

    def keyPressEvent(self, event):
        self.reset_idle_timer()
        if self.step == 4 and event.key() == Qt.Key_Escape:
            self.label.setText("❌ ยกเลิก กำลังกลับไปเริ่มใหม่...")
            playsound.playsound(end_sound)
            QTimer.singleShot(1000, self.show_standby)
        elif self.step == 5 and event.key() == Qt.Key_Escape:
            self.show_standby()

    def save_data(self):
        filename = "output/user_added_slang.json"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                db = json.load(f)
        except:
            db = {}

        word = self.data["word"]
        meaning = self.data["meaning"]
        example = self.data["example"]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if word in db:
            entry = db[word]

            # รวมความหมาย ไม่ซ้ำ
            if isinstance(entry["meaning"], list):
                entry["meaning"] = list(set(entry["meaning"] + [meaning]))
            else:
                entry["meaning"] = list(set([entry["meaning"], meaning]))

            # รวมตัวอย่าง ไม่ซ้ำ
            if isinstance(entry["example"], list):
                entry["example"] = list(set(entry["example"] + [example]))
            else:
                entry["example"] = list(set([entry["example"], example]))

            # เพิ่ม reach และ update
            entry["reach"] = entry.get("reach", 0) + 1
            entry["update"] = now

            db[word] = entry
        else:
            db[word] = {
                "meaning": [meaning],
                "example": [example],
                "reach": 1,
                "update": now
            }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict(sorted(db.items())), f, ensure_ascii=False, indent=2)

def start_gui_and_get_entry():
    app = QApplication(sys.argv)
    kiosk = SlangKiosk()
    kiosk.show()
    sys.exit(app.exec_())
