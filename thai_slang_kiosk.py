## thai_slang_kiosk.py

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

from input_slang_utils import speak_thai, speak_both, detect_motion
from slang_pdf_generator import printpdf

greeting_word = [
    "หวัดดี อยากช่วยเติมคำสแลงใหม่ ๆ ไหมเอ่ย? 💬<br> Wanna help add some cool slang?",
    "ไฮจ้า มาร่วมเพิ่มคลังคำสแลงกันเถอะ! 🌟<br> Hiya! Let’s build our slang dictionary together!",
    "ลองใส่คำสแลงเก๋ ๆ สักคำดูไหมน้า? ✨<br> Wanna try adding a fun slang word?",
    "ช่วยกันเพิ่มคำสแลงให้น่าใช้ยิ่งขึ้นกันดีไหมคะ? 🤝<br> Could you help us make this slang collection even better?",
    "มาแต่งคลังศัพท์สแลงให้น่ารักไปด้วยกันเถอะ 💖<br> Come join us and make our slang library super cute!",
    "แวะมาช่วยกันเติมคำสแลงนิดนึงน้า 📝<br> Can you drop by and add a slang or two?",
    "คิดคำสแลงเด็ด ๆ ได้บ้างไหม? มาแชร์กันหน่อยน้า 😄<br> Got any cool slang? Come share it with us!",
    "มาเป็นส่วนหนึ่งของคลังคำสแลงกันเถอะ 💡<br> Be a part of our slang collection!",
    "อยากให้คลังสแลงนี้ปังๆ มั้ย? มาช่วยกันใส่คำสนุก ๆ หน่อย 🎉<br> Wanna make this dictionary awesome? Let’s add some fun words!",
    "ยินดีต้อนรับสู่คลังคำสแลงทุกคน! ✨<br> Welcome, slang expert! Ready to contribute?",
    "ฮัลโหลวว มาลองใส่คำสแลงสนุก ๆ กันดูไหม 📢<br> Hellooo Wanna add some fun slang together?",
    "มีคำสแลงในใจไหม? มาแชร์ให้โลกเห็นกันเถอะ 🌍<br> Got a slang in mind? Let the world know!",
    "พร้อมสร้างคลังคำสแลงสุดจี๊ดไปด้วยกันรึยัง? 💥<br> Ready to build the ultimate slang vault with us?",
    "เธอคือคนสำคัญที่จะทำให้คลังคำนี้สมบูรณ์นะ 💫<br> You’re the missing piece in our slang puzzle!",
    "อย่าเก็บคำสแลงไว้คนเดียว มาแบ่งให้เพื่อนรู้กันน้า 📚<br> Don’t keep that slang to yourself, Share it with everyone!",
    "วันนี้มีคำเด็ดอะไรบ้างน้า? มาช่วยกันเพิ่มเลย 🧐<br> Got a spicy word today? Add it now!",
    "อยากให้พจนานุกรมนี้มีคำของคุณด้วยจังเลย 💌<br> We’d love to have your words in our slang dictionary!",
    "คลังคำสแลงนี้จะสดใสขึ้นแน่ๆ ถ้ามีคำจากคุณ 🌈<br> This slang vault will shine brighter with your words!",
    "แวะเติมคำสแลงอีกนิดก่อนเดินต่อได้นะ 🚶‍♀️<br> Stop by and drop in a slang before you go!",
    "ใครๆ ก็เป็นผู้สร้างภาษาได้ มาเริ่มจากคำของคุณเลย! 🛠️<br> Anyone can shape the language — let’s start with your word!",
    "คำสแลงดีๆ ไม่ได้มีทุกวันนะ มาเติมไว้ก่อนหมดตู้! 🗣️<br> Good slang doesn’t grow on trees—come add some before it runs out!",
    "ใส่คำสแลงวันนี้ โลกจะจดจำคุณในฐานะผู้ริเริ่มศัพท์ใหม่! 🌍<br> Add a slang today and become a linguistic legend!",
    "ช่วยเราที สมองเราว่างเปล่าเหมือนลูกโป่งเลย 🧠💤<br> Help us out—we’re as blank as a ballon!",
    "คลังสแลงเรียกร้องหาเธอ! ได้ยินเสียงมันไหม? 🔊<br> The slang vault is calling your name! Can you hear it?",
    "อย่าปล่อยให้ช่องคำสแลงเหงา มาใส่คำฮา ๆ หน่อย 😂<br> Don’t leave the slang field lonely—drop in a funny word!",
    "ถ้าไม่รู้จะทำอะไร… ลองเป็นผู้เชี่ยวชาญคำสแลงดูไหม? 🎓<br> Bored? Why not become a certified slangologist?",
    "ใส่คำเดียวโลกเปลี่ยน ใส่สองคำ…ก็ยังเปลี่ยน! 🌎<br> One word can change the world. Two? Even better!",
    "ช่วยเติมคลังสแลงหน่อย เดี๋ยวมีแมวมาแย่งคีย์บอร์ดแล้วนะ 🐱⌨️<br> Add a slang before the cat takes over the keyboard!",
    "คำสแลงไม่เคยพอ…เหมือนของกินแหละ 😋<br> Slang is like snacks—there’s never enough!",
    "ระบบขาดคำสแลงเหมือนชานมขาดไข่มุก 🧋<br> This system without slang is like bubble tea without pearls!",
    "ใส่คำสแลงซักนิด ระบบจะได้ไม่งอนน้า~ 😤<br> Add a slang or two, or the system might give you the silent treatment!",
    "ไม่ใส่คำสแลงวันนี้ เดี๋ยวมีบอทมางอนนะ 🤖💔<br> Skip slang today and our bot might sulk all day!",
    "อย่าปล่อยให้ช่องนี้ว่าง เดี๋ยวผีนิรนามมาเขียนแทน 👻<br> Leave this empty and a ghost might fill it in!",
    "นักสร้างศัพท์เขาไม่รอใครนะ! ⏳<br> Trendy slang creators wait for no one!",
    "คิดไม่ออก? เอาคำบ้านๆ ก็ยังดูเท่ 🤘<br> Can’t think of one? Smash your keyboard and call it slang!",
    "ใส่คำสแลงไปเถอะ อย่างน้อยระบบจะคิดว่าคุณเก่งภาษา 💡<br> Add slang—it’ll make you look super linguistically gifted!",
    "คำสแลงคุณอาจไม่เปลี่ยนโลก แต่เปลี่ยนอารมณ์คนอ่านได้แน่นอน 😂<br> Your slang may not change the world, but it might change someone’s mood!",
    "ยังไม่มีคำ? งั้นขอที่ติดปากก่อนก็ยังดี 🅰️<br> No word yet? Just start with a vowel—we’ll work from there!",
    "คำสแลงดีๆ คือการลงทุนระยะยาวของภาษา! 📈<br> Good slang is like long-term language investment!",
    "อย่ามัวแต่เงียบเป็นเป๋อ มาใส่คำสแลงกันเถอะ 🫠<br> Don’t just sit there — let’s slang it up!",
    "มีคำสแลงปังๆ ไหม? มาแชร์ก่อนจะเป็นต้าวคนล้าสมัย 😎<br> Got fire slang? Share it before too late!",
    "อย่าทำตัวเป็นสายเงียบ มาปล่อยของกันเถอะ 💣<br> Don’t be a ghost — drop that slang bomb!",
    "คำสแลงวันนี้ เปรี้ยวเยี่ยวราด! มีคำแบบนี้อีกไหม? 🤯<br> Do you have today’s slang? Got anything that wild?",
    "ถ้ามีคำสแลงในใจ อย่าเก็บไว้ มันจั๊กจี้! 💓<br> Got slang in your heart? Don’t hold it in — it tickles!",
    "มาเป็นสายเกาเหลา! เก่งคำสแลง เหลาได้หมด 😋<br> Be our slang master — spill the spicy words!",
    "อย่าปล่อยให้คลังนี้แห้งเหมือนน้ำพริกไม่มีปลาทู 🐟<br> Don’t let this vault dry out like chili paste without fish!",
    "วันนี้อารมณ์ไหน? ปั้นคำสแลงให้เข้ากับฟีลเลย! 🎭<br> What’s the vibe today? Make a slang to match your mood!",
    "คลังนี้รับคำสแลงทุกแนว ยกเว้น 'ง่วง' เพราะระบบไม่หลับ 😴<br> All slang welcome — except 'sleepy', 'cause we never snooze!",
    "พจนานุกรมนี้ไม่แซ่บพอ ถ้ายังไม่มีคำเด็ดจากเธอ 🌶️<br> This dictionary ain’t spicy enough without your word!"
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

        self.header = QLabel("ปทานุกรมแบบสับ 📘 Not-So Modern Dictionary")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignCenter)

        self.description = QLabel("เพิ่มคำสแลง ให้กับปทานุกรมของคุณ 📝✨")
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
        self.label.setText("👋 " + greeting + "\n\nกดคีย์ใดก็ได้เพื่อเริ่ม\nPress any key to start")
        self.label.setText(
            "<div style='font-size:40px;'>" + "👋 " + greeting + "<br><br>"
            "<span style='font-size:40px;'>กดคีย์ใดก็ได้เพื่อเริ่ม<br>Press any key to start</span></div>"
        )
        #self.setStyleSheet("QWidget { background-color: #103366; }")
        self.frame.setStyleSheet("background-color: #20232a; border-radius: 30px; padding: 50px;")
        #QTimer.singleShot(100, lambda: speak_thai(random.choice(greeting_word)))
        self.idle_timer.stop()
        self.warning_timer.stop()

    def go_to_standby(self):
        self.label.setText("⌛️ ไม่ได้ใช้งานนาน กำลังกลับไปหน้าเริ่มต้น...\nInactive for a while. Returning to the start screen")
        playsound.playsound(end_sound)
        QTimer.singleShot(1000, self.show_standby) 

    def check_motion(self):
        if self.step == -1 and detect_motion():
            self.label.setText("🏇 พบการเคลื่อนไหว กำลังเริ่มทำงาน")
            self.go_to_greeting()

    def handle_idle_timeout(self):
        if self.step == 0:
            self.go_to_standby()
        elif self.step >= 1:
            if not self.warning_shown:
                self.label.setText("⚠️ หากไม่มีการกรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที หรือกด Esc เพื่อเริ่มต้นใหม่\nIf no input is entered, the system will return to the start screen in 30 seconds, or press Esc to start over")
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
            "<span style='font-size:32px;'>ใส่คำสแลงของคุณ ความหมาย ตัวอย่าง เข้าไปในพจนานุกรมได้เลย<br>Add your slang word, meaning, and example to the dictionary</span><br><br><br>"
            "<span style='font-size:40px;'>กด Enter เพื่อดำเนินการ<br>Press Enter to proceed</span></div>"
        )
        print(f"- greeting: {greeting}")
        self.input.clear()
        #QTimer.singleShot(100, lambda: speak_thai(greeting))
        QTimer.singleShot(100, lambda: speak_both(greeting))
        #QTimer.singleShot(2000, lambda: speak_thai("จากนี้คุณสามารถใส่คำสแลง ความหมาย และตัวอย่างได้"))
        self.reset_idle_timer()

    def go_to_word_input(self):
        self.step = 1
        self.input.clear()
        playsound.playsound(correct_sound)
        self.label.setText(
            "<div style='font-size:40px;'>🖊️ พิมพ์คำสแลง แล้วกด Enter<br>Type a slang word and press Enter<br><br>"
            "<span style='font-size:32px;'>ตัวอย่างเช่น ‘แจ่มแมว’ หรือ ‘เกียม’</span><br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์คำสแลง"))
        self.reset_idle_timer()

    def go_to_meaning_input(self):
        self.step = 2
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>📖 พิมพ์ความหมาย แล้วกด Enter<br>Type the meaning and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ความหมาย"))
        self.reset_idle_timer()

    def go_to_example_input(self):
        self.step = 3
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>💬 พิมพ์ตัวอย่างประโยค แล้วกด Enter<br>Type an example sentence and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ตัวอย่างประโยค"))
        self.reset_idle_timer()

    def go_to_summary(self):
        self.step = 4
        word = self.data["word"]
        meaning = self.data["meaning"]
        example = self.data["example"]
        summary = f"{word}\n📖 {meaning}\n💬 {example}\n\nกด Enter เพื่อยืนยัน หรือ Esc เพื่อเริ่มใหม่\nPress Enter to confirm or Escape to abort"
        print(f"- summary: {summary}")
        self.label.setText(summary)
        QTimer.singleShot(300, lambda: speak_thai(f"{word}  หมายถึง {meaning}  เช่น {example}"))
        self.reset_idle_timer()

    def go_to_print_option(self):
        self.step = 5
        self.input.clear()
        self.label.setText(
            "<div style='font-size:38px;'>🖨️ ต้องการพิมพ์ออกมาไหม?<br>Print your own dict?<br>"
            "<div style='font-size:42px;'>👉 พิมพ์ชื่อของคุณเพื่อลงในหน้าผู้แต่งล่าสุด<br>Would you like to print it out? Type your name to appear as the latest author<br><br>"
            "<span style='font-size:32px;'>หากไม่ต้องการใส่ชื่อหรือพิมพ์ออกมา กด Escape เพื่อข้าม<br>Press Escape to skip</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ชื่อของคุณเพื่อลงในหน้าผู้แต่งล่าสุด"))
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
            if text:
                self.data["author"] = text  # เพิ่ม author ลงใน self.data
                self.save_data()            # ✅ บันทึกลง JSON ก่อน
                printpdf()
                self.label.setText(f"🖨️ กำลังพิมพ์... ขอบคุณ {text} มากนะ")
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
        json_file = "output/user_added_slang.json"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        word = self.data.get("word")
        meaning = self.data.get("meaning")
        example = self.data.get("example")
        author = self.data.get("author", None)  # อาจไม่มี author ในรอบก่อนหน้า

        # โหลดข้อมูลเก่า
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                slang_data = json.load(f)
        else:
            slang_data = {}

        if word not in slang_data:
            slang_data[word] = {
                "meaning": [meaning],
                "example": [example],
                "reach": 1,
                "update": now,
                "author": [author] if author else []
            }
        else:
            entry = slang_data[word]
            # เพิ่มความหมาย ถ้ายังไม่มี
            if meaning not in entry["meaning"]:
                entry["meaning"].append(meaning)
            # เพิ่มตัวอย่าง ถ้ายังไม่มี
            if example not in entry["example"]:
                entry["example"].append(example)
            # เพิ่ม reach
            entry["reach"] = entry.get("reach", 0) + 1
            # อัพเดตเวลา
            entry["update"] = now
            
            # จัดการ author
            if author:
                authors = entry.get("author", [])
                if author in authors:
                    authors.remove(author)
                authors.append(author)  # ย้ายไปท้ายเสมอ
                entry["author"] = authors

        # บันทึกกลับไฟล์ JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(slang_data, f, ensure_ascii=False, indent=4)
            print(f"✅ บันทึกลง JSON  {json_file}")


def start_gui_and_get_entry():
    app = QApplication(sys.argv)
    kiosk = SlangKiosk()
    kiosk.show()
    sys.exit(app.exec_())
