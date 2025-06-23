## thai_slang_kiosk.py

import sys
import json
import os
import time
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

from input_slang_utils import speak_thai, speak_both, detect_motion, log_request_message, run_special_request_if_exists, run_routine_request_if_exists, speak_both_special
from slang_pdf_generator import printpdf

from greetings import greeting_word

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
        self.label.setText("!!<br>ไม่ได้ใช้งานนาน กำลังกลับไปหน้าเริ่มต้น...<br>Inactive for a while. Returning to the start screen")
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
                self.label.setText("<span style='font-size:32px;'>⚠<br>หากไม่กรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที หรือกด Esc เพื่อเริ่มต้นใหม่<br>If no input is entered, the system will return to the start screen in 30 sec, or press Esc to start over.</span>")
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
        
        # Hide input field since we won't use it here
        #self.input.hide()
        self.input.setReadOnly(True) # Ensure input is read-only during greeting
        self.input.setText("กด Enter เพื่อดำเนินการ ... Press Enter to proceed")
        self.input.setAlignment(Qt.AlignCenter)

        #self.input.setReadOnly(False) # Enable input for user interaction
        self.input.setFocus() # Ensure input field has focus

        greeting = random.choice(greeting_word)
        self.frame.setStyleSheet("background-color: #004080; border-radius: 30px; padding: 50px;")
        self.label.setText(
            f"<div style='font-size:40px;'>👋 {greeting}</div><br><br>"
            "<span style='font-size:32px;'>ใส่คำสแลงของคุณ ความหมาย ตัวอย่าง เข้าไปในพจนานุกรมได้เลย<br>Add your slang word, meaning, and example to the dictionary</span><br><br><br>"
            "<span style='font-size:40px; color: #FFFF00;'>และรับปทานุกรมของคุณ เป็นที่ระลึกตอนท้าย<br>get your dictionary as souvenir at the end</span>"
        )
        print(f"- greeting: {greeting}")
        log_request_message(f"- greeting: {greeting}") 
        #self.input.clear()
        QTimer.singleShot(100, lambda: speak_both(greeting))
        self.reset_idle_timer()

    def go_to_word_input(self):
        """Transitions to the word input step."""
        self.step = 1
        playsound(correct_sound) # Corrected call
        log_request_message("🚀 Starting word input page") 
        
        self.input.setReadOnly(False) # Enable input for user interaction
        self.input.setFocus() # Ensure input field has focus
        self.input.clear()

        self.label.setText(
            "<div style='font-size:40px;'>🖊️ พิมพ์คำสแลง แล้วกด Enter<br>Type a slang word and press Enter<br><br>"
            "<span style='font-size:32px;'>ตัวอย่างเช่น ‘แจ่มแมว’ หรือ ‘เกียม’</span><br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_both("พิมพ์คำสแลง<br>Drop your slang!"))
        self.reset_idle_timer()

    def go_to_meaning_input(self):
        """Transitions to the meaning input step."""
        self.step = 2
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>📖 พิมพ์ความหมาย แล้วกด Enter<br>Type the meaning and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_both("พิมพ์ความหมาย<br>Meaning?"))
        log_request_message("..meaning_input")
        self.reset_idle_timer()

    def go_to_example_input(self):
        """Transitions to the example input step."""
        self.step = 3
        self.input.clear()
        self.label.setText(
            "<div style='font-size:40px;'>💬 พิมพ์ตัวอย่างประโยค แล้วกด Enter<br>Type an example sentence and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>Press Escape to start over</span></div>"
        )
        QTimer.singleShot(300, lambda: speak_both("พิมพ์ตัวอย่างประโยค<br>Example sentence?"))
        log_request_message("..example_input")
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
        summary = f"<div style='font-size:38px; text-align: center;'><b>คำศัพท์ | Word:</b> {word_display}<br><b>📖 ความหมาย | Meaning:</b> {meaning_display}<br><b>💬 ตัวอย่าง | Example:</b> {example_display}<br><br><span style='font-size:40px; color: #FFFF00;'>รอการยืนยันจากคุณ<br>waiting for your confirmation</span></div>"

        print(f"- summary: {summary}")
        self.label.setText(summary)

        self.input.setReadOnly(True) # Ensure input is read-only during greeting
        self.input.setText("Enter เพื่อยืนยัน หรือ Esc เพื่อยกเลิก  ...  Press Enter to confirm or Escape to abort")
        self.input.setAlignment(Qt.AlignCenter)    

        # Use full text for speech, or truncated for brevity if desired
        QTimer.singleShot(300, lambda: speak_thai(f"{word_full} หมายถึง {meaning_full} เช่น {example_full}"))
        self.reset_idle_timer()
        
    def go_to_print_option(self):
        """Transitions to the print option step, allowing user to enter name for printing."""
        self.step = 5
        self.input.setReadOnly(False) # Enable input for user interaction
        self.input.clear()
        self.label.setText(
            "<div style='font-size:38px;'>🖨️ ต้องการพิมพ์ออกมาไหม?<br>Print your own dict?<br>"
            "<div style='font-size:42px; color: #FFFF00;'>👉 พิมพ์ชื่อของคุณเพื่อลงในหน้าผู้แต่งล่าสุด<br>Would you like to print it out? Type your name to appear as the latest author<br><br></div>"
            "<span style='font-size:32px;'>หากไม่ต้องการใส่ชื่อหรือพิมพ์ออกมา กด Escape เพื่อข้าม<br>Press Escape to skip</span>"
        )
        QTimer.singleShot(300, lambda: speak_both("พิมพ์ชื่อของคุณเพื่อลงในหน้าผู้แต่งล่าสุด<br>Your name for author?"))
        log_request_message("..Starting print option") 
        self.reset_idle_timer()
    
    def next_step(self):
        """Handles logic for transitioning between steps based on user input."""
        text = self.input.text().strip()
        print(f"- Step: {self.step}")
        if self.step == 0: # From greeting to word input
            self.go_to_word_input()
            self.input.clear() # Clear input after each step
        elif self.step == 1: # From word input to meaning input
            if not text: 
                self.label.setText("<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์คำสแลง<br>Please type a slang word.</div>")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1500, self.go_to_word_input) 
                return
            self.data["word"] = text
            self.go_to_meaning_input()
            self.input.clear() # Clear input after each step
        elif self.step == 2: # From meaning input to example input
            if not text: 
                self.label.setText("<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์ความหมาย<br>Please type the meaning.</div>")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1500, self.go_to_meaning_input) 
                return
            self.data["meaning"] = text
            self.go_to_example_input()
            self.input.clear() # Clear input after each step
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
                self.label.setText(f"🖨️ กำลังพิมพ์... ขอบคุณ {text} มากนะ<br>Printing your dictionary, thanks {text}")
                playsound(correct_sound) # Corrected call
                self.reset_idle_timer() # Reset timer after interaction      
                
                # log_request_message("##------")
                # log_request_message("🚀 Starting new request")
                # print("##-----\n🚀 Starting new request")
                # got_jackpot = run_routine_request_if_exists()
                
                # if got_jackpot: 
                    # run_special_request_if_exists()
                    # QTimer.singleShot(10000, self.show_standby) # Return to standby after printing
                # else:
                    # QTimer.singleShot(3000, self.show_standby) # Return to standby after printing

                # Delay heavy logic to let label update first
                def delayed_actions():
                    printpdf(author=text)
                    log_request_message("##------")
                    log_request_message("🚀 Starting new request")
                    print("##-----\n🚀 Starting new request")
                    self.reset_idle_timer() # Reset timer after interaction      
                    got_jackpot = run_routine_request_if_exists()
                    if got_jackpot:
                        self.reset_idle_timer() # Reset timer after interaction      
                        run_special_request_if_exists()
                        QTimer.singleShot(10000, self.show_standby)
                    else:
                        QTimer.singleShot(8500, self.show_standby)

                QTimer.singleShot(5, delayed_actions)  # Run after 100ms

                    
            else: # User skipped entering author name
                self.label.setText("ขอบคุณที่ใช้บริการ! กลับสู่หน้าเริ่มต้น")
                playsound(end_sound) # Corrected call
                QTimer.singleShot(1000, self.show_standby) # Just go to standby if no author name
                
            self.input.clear() # Clear input after each step

        #self.input.clear() # Clear input after each step

        self.reset_idle_timer() # Reset timer after interaction      

    def keyPressEvent(self, event):
        """Global key press event handler for the Kiosk widget."""
        self.reset_idle_timer()
        if event.key() == Qt.Key_Escape:
            if self.step in [1, 2, 3, 4, 5]: # If in any active input/summary/print step
                self.label.setText("❌ ยกเลิก กำลังกลับเริ่มโปรแกรมใหม่...<br>Cancelling. Returning to start screen.")
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
