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
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from gtts import gTTS
from playsound import playsound # Correct import: playsound is now the function directly
import speech_recognition as sr
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
    "ยินดีต้อนรับสู่คลังคำสแลงทุกคน! ✨<br> Welcome, slang expert! Ready to contribute!",
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
    "ถ้าไม่รู้จะทำอะไร ลองเป็นผู้เชี่ยวชาญคำสแลงดูไหม? 🎓<br> Bored? Why not become a certified slangologist?",
    "ใส่คำเดียวโลกเปลี่ยน ใส่สองคำ ก็ยังเปลี่ยน! 🌎<br> One word can change the world. Two? Even better!",
    "ช่วยเติมคลังสแลงหน่อย เดี๋ยวมีแมวมาแย่งคีย์บอร์ดแล้วนะ 🐱⌨️<br> Add a slang before the cat takes over the keyboard!",
    "คำสแลงไม่เคยพอ เหมือนของกินแหละ 😋<br> Slang is like snacks—there’s never enough!",
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
    "คลังนี้รับคำสแลงทุกแนว ยกเว้นง่วง เพราะระบบไม่หลับ 😴<br> All slang welcome — except 'sleepy', 'cause we never snooze!",
    "พจนานุกรมนี้ไม่แซ่บพอ ถ้ายังไม่มีคำเด็ดจากเธอ 🌶️<br> This dictionary ain’t spicy enough without your word!",
    "คิดถึงคำสแลงใหม่ๆ อยู่หรือเปล่า? มาลองพิมพ์ดูสิ! 🤔<br> Thinking of new slang? Type it in!",
    "วันนี้มีศัพท์ใหม่ๆ ในหัวมั้ย? เราพร้อมรับทุกคำเลยนะ 🤩<br> Got fresh words on your mind? We're ready for them all!",
    "มาช่วยกันอัปเดตคำสแลงให้ทันยุคกัน! 🚀<br> Let's update our slang to keep up with the times!",
    "ก่อนไปทำอย่างอื่น แวะเพิ่มสีสันให้คลังคำสแลงหน่อย ✨<br> Before you go, add some sparkle to our slang collection!",
    "ถ้าคุณมีคำสแลงเจ๋งๆ เราก็มีที่ให้คุณโชว์! 🏆<br> If you have cool slang, we have the perfect stage for you!",
    "มาสร้างตำนานศัพท์สแลงไปพร้อมกัน! 📜<br> Let's create slang legends together!",
    "เพิ่มคำสแลงของคุณ เพื่อให้ภาษาไทยไม่ตกเทรนด์! 🇹🇭<br> Add your slang to keep Thai language trendy!",
    "ปล่อยพลังคำสแลงในตัวคุณออกมาเลย! 💥<br> Unleash your inner slang power!",
    "เรามาถึงยุคที่คำสแลงสำคัญกว่าคำปกติแล้ว! มาเพิ่มกันเถอะ! 😎<br> We've reached an era where slang is cooler than formal words! Let's add more!",
    "อย่ารอช้า คำสแลงดีๆ ไม่ได้อยู่ยงคงกระพันนะ! 🏃‍♀️<br> Don't delay, good slang doesn't last forever!",
    "สมองคนดีๆ ไม่ว่างเปล่าหรอก ยกเว้นคนยังไม่เพิ่มสแลง! 😅<br> A good brain isn't empty, unless you haven't added slang yet!",
    "ถ้าคำสแลงคือเงิน เราคงเป็นเศรษฐีแล้ว แค่ยังไม่มีคนใส่มาให้! 🤷‍♀️<br> If slang was money, we'd be rich, if only someone would add some!",
    "วันนี้กินข้าวกับอะไรไม่สำคัญเท่า ได้เพิ่มคำสแลงหรือยัง? ️💬<br> What you ate today isn't as important as have you added slang yet?",
    "มีคำสแลงในใจแต่ไม่ใส่ เหมือนสั่งชานมไข่มุกแล้วไม่เอาไข่มุกนะ! 💔<br> Having slang in mind but not adding it is like ordering bubble tea without the pearls!",
    "มาเพิ่มคำสแลงหน่อย เดี๋ยวบอทจะงอนจนระบบล่มนะ! 🤖💥<br> Add some slang or the bot might get so grumpy the system crashes!",
    "กลัวเป็นคนตกยุค? มาใส่คำสแลงอัปเดตชีวิตกัน! 😎<br> Afraid of being outdated? Add slang to update your life!",
    "คลังคำสแลงเราขาดคุณไม่ได้ ไม่งั้นจะเหมือนตู้เย็นไม่มีของกิน! 🍔<br> Our slang vault can't live without you otherwise, it'll be like a fridge with no food!"
]

correct_sound = "correct sound/correct-6033.mp3"
systemstart_sound = "systemstart sound/game-start-6104.mp3"
start_sound = "beep sound/point-smooth-beep-230573.mp3"
end_sound = "beep sound/short-beep-tone-47916.mp3"
logo_path = "template/PNGYOONGLAI.png" # Path to your image file

ideal_warning = 30 * 1000 # mil.second to announce warning before reset
reset_warning = 60 * 1000 # mil.second to go to reset

class CustomLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.kiosk = parent

    def keyPressEvent(self, event):
        self.kiosk.reset_idle_timer()
        # The keyPressEvent logic for CustomLineEdit should mostly defer to SlangKiosk's
        # keyPressEvent to centralize step-based behavior, especially for Esc.
        # This CustomLineEdit specific logic is only for step-specific behavior not covered
        # by the main keyPressEvent in SlangKiosk (e.g., direct transitions or specific input handling).
        
        # If in standby, any key press should trigger go_to_greeting via the main keyPressEvent
        # So, only handle Esc for active steps here if not handled by parent.
        if event.key() == Qt.Key_Escape and self.kiosk.step in [1, 2, 3, 4, 5]:
            self.kiosk.label.setText("❌ ยกเลิก กำลังกลับเริ่มโปรแกรมใหม่...")
            playsound(end_sound) # Corrected call
            QTimer.singleShot(1000, self.kiosk.show_standby)
        # Removed `elif self.kiosk.step == -1: self.kiosk.go_to_greeting()`
        # because the main SlangKiosk.keyPressEvent will handle any key press in standby.
        else:
            super().keyPressEvent(event)


class SlangKiosk(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 Your Thai Slang Dictionary - Kiosk Mode")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.data = {}
        self.step = -1 # -1 for standby, 0 for greeting, 1-5 for input/summary/print
        self.warning_shown = False
        self.logo_path = logo_path # Path to the logo image
        
        # Initialize standby_image_label and standby_instruction_label to None or empty QLabel
        # before calling init_ui to prevent AttributeError if show_standby is triggered prematurely.
        self.standby_image_label = QLabel() # Initialized here
        self.standby_instruction_label = QLabel() # Initialized here

        self.init_ui()

        self.motion_timer = QTimer()
        self.motion_timer.timeout.connect(self.check_motion)
        self.motion_timer.start(1000) # Check for motion every 1 second

        self.idle_timer = QTimer()
        self.idle_timer.setInterval(ideal_warning)
        self.idle_timer.timeout.connect(self.handle_idle_timeout)

        self.warning_timer = QTimer()
        self.warning_timer.setInterval(reset_warning - ideal_warning) # This should be the duration after warning to reset
        self.warning_timer.timeout.connect(self.go_to_standby)

        QTimer.singleShot(500, self.show_standby)

    def reset_idle_timer(self):
        """Resets the idle timer. Called on user interaction."""
        self.idle_timer.stop()
        self.warning_timer.stop()
        self.warning_shown = False # Reset warning flag whenever user interacts
        if self.step >= 0: # Only start timer if not in standby
            self.idle_timer.start()

    def init_ui(self):
        """Initializes the main user interface layout and widgets."""
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
                color: #ffffff; /* Set a dark color for text on white background */
            }
            QLabel#StandbyInstructionLabel {
                font-size: 36px;
                color: #ffffff;
                text-align: center; /* This is for HTML content if used, QLabel itself uses alignment property */
            }
        """)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#282c34")) # Dark background for the window
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(30)
        self.layout.setAlignment(Qt.AlignCenter)

        # --- Active UI Elements (for input steps) ---
        self.header = QLabel("ปทานุกรมแบบสับ 📘 The Not-So Modern Dictionary")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignCenter)

        self.description = QLabel("เพิ่มคำสแลง ให้กับปทานุกรมของคุณ 📝✨")
        self.description.setObjectName("DescLabel")
        self.description.setAlignment(Qt.AlignCenter)

        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #3c4048; border-radius: 30px; padding: 50px;")
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("") # Main message label within the interactive frame
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; color: white;")
        self.label.setWordWrap(True) # Ensure text wraps if too long

        self.input = CustomLineEdit(self)
        self.input.returnPressed.connect(self.next_step)
        self.input.setText("") 
        self.input.setReadOnly(True) # Initially read-only

        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.input)
        self.frame.setLayout(self.frame_layout)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.frame)
        # --- End Active UI Elements ---

        # --- Standby UI Elements ---
        # These are already initialized in __init__
        self.standby_image_label.setAlignment(Qt.AlignCenter)

        self.standby_instruction_label.setObjectName("StandbyInstructionLabel")
        self.standby_instruction_label.setAlignment(Qt.AlignCenter)
        self.standby_instruction_label.setFont(QFont("Kinnari", 28)) # Use Kinnari font for Thai
        self.standby_instruction_label.setWordWrap(False) # Ensure text wraps if too long

        self.layout.addWidget(self.standby_image_label)
        self.layout.addWidget(self.standby_instruction_label)
        # --- End Standby UI Elements ---

        self.setLayout(self.layout)
        self.input.setFocus() # Keep focus on input for global keyPressEvent

    def show_standby(self):
        """Transitions the UI to the standby screen."""
        print("show_standby")
        self.step = -1
        self.warning_shown = False # Reset warning flag
        self.input.clear()
        self.input.setReadOnly(True) # Ensure input is read-only during standby

        # Hide active UI elements
        self.header.hide()
        self.description.hide()
        self.frame.hide()

        # Show standby UI elements
        self.standby_image_label.show()
        self.standby_instruction_label.show()
        
        # Load image for standby
        image_path = self.logo_path # Use the logo_path defined in __init__
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation) # Scale image
                self.standby_image_label.setPixmap(scaled_pixmap)
                # Set background for the image to match the window for seamless look if image is smaller
                self.standby_image_label.setStyleSheet("background-color: transparent;") 
            else:
                self.standby_image_label.clear() # Clear any previous pixmap
                self.standby_image_label.setText("❌ ไม่สามารถโหลดรูปภาพได้ กรุณาตรวจสอบไฟล์.")
                self.standby_image_label.setStyleSheet("color: red; font-size: 24px;")
                print(f"⚠️ คำเตือน: ไม่สามารถโหลดรูปภาพที่ '{image_path}'")
        else:
            self.standby_image_label.clear() # Clear any previous pixmap
            self.standby_image_label.setText(f"⚠️ คำเตือน: ไม่พบไฟล์รูปภาพที่ '{image_path}'")
            self.standby_image_label.setStyleSheet("color: orange; font-size: 24px;")
            print(f"⚠️ คำเตือน: ไม่พบไฟล์รูปภาพที่ '{image_path}'")

        # Update standby instruction label with greeting and prompt
        greeting = random.choice(greeting_word)
        self.standby_instruction_label.setText(
            f"<div style='font-size:40px;'>👋 {greeting}</div><br><br>"
            "<span style='font-size:30px;'>กดคีย์ใดก็ได้เพื่อเริ่ม<br>Press any key to start</span>"
        )
        self.standby_instruction_label.setStyleSheet("color: white;") # Ensure text color is visible

        # Stop idle timers when in standby
        self.idle_timer.stop()
        self.warning_timer.stop()

    def go_to_standby(self):
        """Resets the system to the standby screen due to inactivity."""
        self.label.setText("⌛️ ไม่ได้ใช้งานนาน กำลังกลับไปหน้าเริ่มต้น...\nInactive for a while. Returning to the start screen")
        playsound(end_sound) # Corrected call
        QTimer.singleShot(2000, self.show_standby)

    def check_motion(self):
        """Checks for motion to transition from standby to greeting."""
        if self.step == -1 and detect_motion():
            # Temporarily show motion detected message on standby instruction label
            self.standby_instruction_label.setText("🏇 พบการเคลื่อนไหว กำลังเริ่มปฎิบัติการ<br><br>🚨 I found your move ... activating")
            playsound(start_sound) # Corrected call # Play a sound immediately on motion detection
            print("motion found")
            # Schedule the greeting transition. The guard in go_to_greeting will prevent double execution.
            QTimer.singleShot(3000, self.go_to_greeting) 

    def handle_idle_timeout(self):
        """Handles the idle timer timeout, issuing warnings or returning to standby."""
        if self.step == 0: # If at greeting and idle, go to standby directly
            self.go_to_standby()
        elif self.step >= 1: # If in input/summary steps and idle
            if not self.warning_shown:
                self.label.setText("⚠️ หากไม่มีการกรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที หรือกด Esc เพื่อเริ่มต้นใหม่\nIf no input is entered, the system will return to the start screen in 30 seconds, or press Esc to start over")
                speak_thai("หากไม่มีการกรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที")
                self.warning_shown = True
                self.warning_timer.start() # Start the second timer for final reset
            # If warning was already shown and idle timeout fires again, means reset_warning period is over
            # and it should go to standby. This is handled by warning_timer.timeout.connect(self.go_to_standby)

    def go_to_greeting(self):
        """Transitions the UI to the greeting screen, ready for user input."""
        # Guard to prevent multiple calls if triggered by both motion and key press
        if self.step != -1: 
            print(f"DEBUG: go_to_greeting called but step is {self.step}, not -1. Skipping.")
            return

        self.step = 0
        playsound(correct_sound) # Corrected call
        print(f"- step: {self.step}")
        
        # Hide standby UI elements
        self.standby_image_label.hide()
        self.standby_instruction_label.hide()

        # Show active UI elements
        self.header.show()
        self.description.show()
        self.frame.show()
        
        self.input.setReadOnly(False) # Enable input for user interaction
        self.input.setFocus() # Ensure input field has focus

        greeting = random.choice(greeting_word)
        self.frame.setStyleSheet("background-color: #004080; border-radius: 30px; padding: 50px;")
        self.label.setText(
            f"<div style='font-size:40px;'>👋 {greeting}</div><br><br>"
            "<span style='font-size:32px;'>ใส่คำสแลงของคุณ ความหมาย ตัวอย่าง เข้าไปในพจนานุกรมได้เลย<br>Add your slang word, meaning, and example to the dictionary</span><br><br><br>"
            "<span style='font-size:40px; color: #FFFF00;'>กด Enter เพื่อดำเนินการ<br>Press Enter to proceed</span>"
        )
        print(f"- greeting: {greeting}")
        self.input.clear()
        QTimer.singleShot(100, lambda: speak_both(greeting))
        self.reset_idle_timer()

    def go_to_word_input(self):
        """Transitions to the word input step."""
        self.step = 1
        self.input.clear()
        playsound(correct_sound) # Corrected call
        self.label.setText(
            "<div style='font-size:40px;'>🖊️ พิมพ์คำสแลง แล้วกด Enter<br>Type a slang word and press Enter<br><br>"
            "<span style='font-size:32px;'>ตัวอย่างเช่น ‘แจ่มแมว’ หรือ ‘เกียม’</span><br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์คำสแลง"))
        self.reset_idle_timer()

    def go_to_meaning_input(self):
        """Transitions to the meaning input step."""
        self.step = 2
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>📖 พิมพ์ความหมาย แล้วกด Enter<br>Type the meaning and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ความหมาย"))
        self.reset_idle_timer()

    def go_to_example_input(self):
        """Transitions to the example input step."""
        self.step = 3
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>💬 พิมพ์ตัวอย่างประโยค แล้วกด Enter<br>Type an example sentence and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_thai("พิมพ์ตัวอย่างประโยค"))
        self.reset_idle_timer()

    def go_to_summary(self):
        """Transitions to the summary step, displaying entered data for confirmation."""
        self.step = 4
        
        # Get data and truncate to first 40 characters
        word_full = self.data.get("word", "N/A")
        meaning_full = self.data.get("meaning", "N/A")
        example_full = self.data.get("example", "N/A")

        word_display = (word_full[:40] + '...') if len(word_full) > 40 else word_full
        meaning_display = (meaning_full[:40] + '...') if len(meaning_full) > 40 else meaning_full
        example_display = (example_full[:40] + '...') if len(example_full) > 40 else example_full

        # Added text-align: center; to the outer div style
        summary = f"<div style='font-size:38px; text-align: center;'><b>คำศัพท์ | Word:</b> {word_display}<br><b>📖 ความหมาย | Meaning:</b> {meaning_display}<br><b>💬 ตัวอย่าง | Example:</b> {example_display}<br><br><span style='font-size:32px;'>กด Enter เพื่อยืนยัน หรือ Esc เพื่อเริ่มใหม่<br>Press Enter to confirm or Escape to abort</span></div>"
        print(f"- summary: {summary}")
        self.label.setText(summary)
        
        # Use full text for speech, or truncated for brevity if desired
        QTimer.singleShot(300, lambda: speak_thai(f"{word_full} หมายถึง {meaning_full} เช่น {example_full}"))
        self.reset_idle_timer()
        
    def go_to_print_option(self):
        """Transitions to the print option step, allowing user to enter name for printing."""
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
        """Handles logic for transitioning between steps based on user input."""
        text = self.input.text().strip()
        print(f"- Step: {self.step}")
        if self.step == 0: # From greeting to word input
            self.go_to_word_input()
        elif self.step == 1: # From word input to meaning input
            if not text: 
                self.label.setText("<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์คำสแลง<br>Please type a slang word.</div>")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1500, self.go_to_word_input) 
                return
            self.data["word"] = text
            self.go_to_meaning_input()
        elif self.step == 2: # From meaning input to example input
            if not text: 
                self.label.setText("<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์ความหมาย<br>Please type the meaning.</div>")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1500, self.go_to_meaning_input) 
                return
            self.data["meaning"] = text
            self.go_to_example_input()
        elif self.step == 3: # From example input to summary
            if not text: 
                self.label.setText("<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์ตัวอย่างประโยค<br>Please type an example sentence.</div>")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1500, self.go_to_example_input) 
                return
            self.data["example"] = text
            self.go_to_summary()
        elif self.step == 4: # From summary to print option (confirming data)
            self.save_data() # Save data *before* going to print option
            self.go_to_print_option()

        elif self.step == 5: # From print option (user entered name or skipped)
            if text: # User provided an author name
                self.data["author"] = text  
                self.save_author_to_latest_entry(self.data["word"], text) # Update author specifically for the word just added
                printpdf(author=text) # Pass author name to printpdf
                self.label.setText(f"🖨️ กำลังพิมพ์... ขอบคุณ {text} มากนะ")
                playsound(correct_sound) # Corrected call
                QTimer.singleShot(3000, self.show_standby) # Return to standby after printing
            else: # User skipped entering author name
                self.label.setText("ขอบคุณที่ใช้บริการ! กลับสู่หน้าเริ่มต้น")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1000, self.show_standby) # Just go to standby if no author name

        self.input.clear() # Clear input after each step
        self.reset_idle_timer() # Reset timer after interaction

    def keyPressEvent(self, event):
        """Global key press event handler for the Kiosk widget."""
        self.reset_idle_timer()
        if event.key() == Qt.Key_Escape:
            if self.step in [1, 2, 3, 4, 5]: # If in any active input/summary/print step
                self.label.setText("❌ ยกเลิก กำลังกลับเริ่มโปรแกรมใหม่...\nCancelling. Returning to start screen.")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1000, self.show_standby)
            elif self.step == -1: # If in standby mode (Esc also acts as "any key")
                print("Esc also acts as any key, triggering greeting.")
                self.go_to_greeting() # This will be guarded by the new condition in go_to_greeting()
        elif self.step == -1: # Any non-Esc key press in standby also starts greeting
            print("Any non-Esc key press, triggering greeting.")
            self.go_to_greeting() # This will be guarded by the new condition in go_to_greeting()
        else:
            # For other keys, ensure the CustomLineEdit can still receive them for text input
            # If the focused widget is CustomLineEdit, pass the event to it
            if isinstance(self.focusWidget(), QLineEdit):
                super().keyPressEvent(event)
            # If focus is not on QLineEdit and it's not a global control key, do nothing or handle later.

    def save_data(self):
        """Saves the new slang entry to the JSON file."""
        json_file = "output/user_added_slang.json"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        word = self.data.get("word")
        meaning = self.data.get("meaning")
        example = self.data.get("example")
        
        # Load existing data
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
                "author": [] # Author will be added/updated by save_author_to_latest_entry
            }
        else:
            entry = slang_data[word]
            if meaning and meaning not in entry["meaning"]: # Only add if meaning is present and new
                entry["meaning"].append(meaning)
            if example and example not in entry["example"]: # Only add if example is present and new
                entry["example"].append(example)
            entry["reach"] = entry.get("reach", 0) + 1
            entry["update"] = now

        # Save back to JSON file
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(slang_data, f, ensure_ascii=False, indent=4)
            print(f"✅ บันทึกลง JSON  {json_file}")
            playsound(correct_sound) # Corrected call # Play sound for successful save

    def save_author_to_latest_entry(self, word, author_name):
        """
        Updates the author list for a specific word (usually the latest added)
        in the JSON database, moving the author to the end if already present.
        """
        json_file = "output/user_added_slang.json"
        if not os.path.exists(json_file):
            print(f"❌ ไม่พบไฟล์ JSON '{json_file}' ไม่สามารถอัปเดตผู้แต่งได้.")
            return

        with open(json_file, "r", encoding="utf-8") as f:
            slang_data = json.load(f)

        if word in slang_data:
            entry = slang_data[word]
            authors = entry.get("author", [])
            if author_name in authors:
                authors.remove(author_name) # Move existing author to end
            authors.append(author_name)
            entry["author"] = authors
            
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(slang_data, f, ensure_ascii=False, indent=4)
                print(f"✅ อัปเดตผู้แต่งสำหรับคำ '{word}' ลง JSON {json_file}")
        else:
            print(f"❌ ไม่พบคำศัพท์ '{word}' ในฐานข้อมูล ไม่สามารถอัปเดตผู้แต่งได้.")


def start_gui_and_get_entry():
    """Starts the QApplication and runs the SlangKiosk."""
    app = QApplication(sys.argv)
    kiosk = SlangKiosk()
    kiosk.show()
    sys.exit(app.exec_())
