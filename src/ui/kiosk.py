"""
Refactored Kiosk UI module for The Not-So-Modern Dictionary.
Provides a full-screen PyQt5 interface with 7-step workflow for adding slang entries.
"""

import sys
import os
import time
import random
import cv2
import numpy as np
from datetime import datetime
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont

from ..config.settings import (
    KIOSK_SETTINGS,
    GREETING_MESSAGES,
    ASSETS_DIR,
    AppMode
)
from ..core.database import SlangDatabase
from ..core.easter_eggs import EasterEggManager
from ..audio.speech import SpeechEngine
from ..audio.sound_effects import SoundManager
from ..utils.logger import app_logger


class CustomLineEdit(QLineEdit):
    """Custom QLineEdit that resets idle timer on key press and handles Escape key."""

    def __init__(self, parent):
        super().__init__(parent)
        self.kiosk = parent

    def keyPressEvent(self, event):
        """Handle key press events with idle timer reset."""
        self.kiosk.reset_idle_timer()

        # Handle Escape key in active steps
        if event.key() == Qt.Key_Escape and self.kiosk.step in [1, 2, 3, 4, 5]:
            self.kiosk.label.setText(
                "❌ ยกเลิก กำลังกลับเริ่มโปรแกรมใหม่...<br>"
                "Cancelling. Returning to start screen."
            )
            self.kiosk.sound_manager.play_end_beep()
            QTimer.singleShot(1000, self.kiosk.show_standby)
        else:
            super().keyPressEvent(event)


class SlangKiosk(QWidget):
    """
    Full-screen kiosk interface for the slang dictionary.

    Implements a 7-step workflow:
    - Step -1: Standby (motion detection)
    - Step 0: Greeting
    - Step 1: Word input
    - Step 2: Meaning input
    - Step 3: Example input
    - Step 4: Summary confirmation
    - Step 5: Author name and print
    """

    def __init__(self, database: SlangDatabase, easter_eggs: EasterEggManager,
                 speech_engine: SpeechEngine, sound_manager: SoundManager,
                 mode: str = AppMode.NORMAL):
        """
        Initialize the kiosk interface.

        Args:
            database: SlangDatabase instance for data management
            easter_eggs: EasterEggManager for special events
            speech_engine: SpeechEngine for text-to-speech
            sound_manager: SoundManager for audio effects
            mode: Application mode (normal, lastweek, etc.)
        """
        super().__init__()

        # Store dependencies
        self.database = database
        self.easter_eggs = easter_eggs
        self.speech_engine = speech_engine
        self.sound_manager = sound_manager
        self.mode = mode

        # State variables
        self.data = {}
        self.step = -1  # -1 for standby, 0 for greeting, 1-5 for input/summary/print
        self.warning_shown = False

        # Paths
        self.logo_path = str(ASSETS_DIR / "templates" / "PNGYOONGLAI.png")

        # Initialize UI labels
        self.standby_image_label = QLabel()
        self.standby_instruction_label = QLabel()

        # Setup window
        self.setWindowTitle("📚 Your Thai Slang Dictionary - Kiosk Mode")
        self.setWindowFlags(Qt.FramelessWindowHint)
        if KIOSK_SETTINGS["fullscreen"]:
            self.showFullScreen()

        # Initialize UI
        self.init_ui()

        # Setup timers
        self._setup_timers()

        # Start in standby mode
        QTimer.singleShot(500, self.show_standby)

        app_logger.info(f"Kiosk initialized in {mode} mode")

    def _setup_timers(self):
        """Setup motion detection and idle timers."""
        # Motion detection timer
        self.motion_timer = QTimer()
        self.motion_timer.timeout.connect(self.check_motion)
        self.motion_timer.start(1000)  # Check every second

        # Idle warning timer
        self.idle_timer = QTimer()
        self.idle_timer.setInterval(KIOSK_SETTINGS["idle_warning_time"])
        self.idle_timer.timeout.connect(self.handle_idle_timeout)

        # Reset timer (after warning)
        self.warning_timer = QTimer()
        warning_duration = (KIOSK_SETTINGS["reset_time"] -
                          KIOSK_SETTINGS["idle_warning_time"])
        self.warning_timer.setInterval(warning_duration)
        self.warning_timer.timeout.connect(self.go_to_standby)

    def reset_idle_timer(self):
        """Reset idle timer on user interaction."""
        self.idle_timer.stop()
        self.warning_timer.stop()
        self.warning_shown = False

        # Only start timer if not in standby
        if self.step >= 0:
            self.idle_timer.start()

    def init_ui(self):
        """Initialize the main user interface layout and widgets."""
        # Stylesheet
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
                color: #000000;
            }
            QLabel#StandbyInstructionLabel {
                font-size: 36px;
                color: #ffffff;
                text-align: center;
            }
        """)

        # Background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#282c34"))
        self.setPalette(palette)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(30)
        self.layout.setAlignment(Qt.AlignCenter)

        # === Active UI Elements ===
        self.header = QLabel("ปทานุกรมแบบสับ 📘 The Not-So Modern Dictionary")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignCenter)

        self.description = QLabel("เพิ่มคำสแลง ให้กับปทานุกรมของคุณ 📝✨")
        self.description.setObjectName("DescLabel")
        self.description.setAlignment(Qt.AlignCenter)

        # Frame for interactive content
        self.frame = QFrame()
        self.frame.setStyleSheet(
            "background-color: #3c4048; border-radius: 30px; padding: 50px;"
        )
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignCenter)

        # Main message label
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; color: white;")
        self.label.setWordWrap(True)

        # Input field
        self.input = CustomLineEdit(self)
        self.input.returnPressed.connect(self.next_step)
        self.input.setText("")
        self.input.setReadOnly(True)

        # Assemble frame
        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.input)
        self.frame.setLayout(self.frame_layout)

        # Add active elements to layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.frame)

        # === Standby UI Elements ===
        self.standby_image_label.setAlignment(Qt.AlignCenter)

        self.standby_instruction_label.setObjectName("StandbyInstructionLabel")
        self.standby_instruction_label.setAlignment(Qt.AlignCenter)
        self.standby_instruction_label.setFont(QFont("Kinnari", 28))
        self.standby_instruction_label.setWordWrap(False)

        self.layout.addWidget(self.standby_image_label)
        self.layout.addWidget(self.standby_instruction_label)

        # Set main layout
        self.setLayout(self.layout)
        self.input.setFocus()

    def show_standby(self):
        """Transition to standby screen."""
        app_logger.info("Entering standby mode")
        self.step = -1
        self.warning_shown = False
        self.input.clear()
        self.input.setReadOnly(True)

        # Hide active UI
        self.header.hide()
        self.description.hide()
        self.frame.hide()

        # Show standby UI
        self.standby_image_label.show()
        self.standby_instruction_label.show()

        # Load logo
        if os.path.exists(self.logo_path):
            pixmap = QPixmap(self.logo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.standby_image_label.setPixmap(scaled_pixmap)
                self.standby_image_label.setStyleSheet("background-color: transparent;")
            else:
                self.standby_image_label.clear()
                self.standby_image_label.setText(
                    "❌ ไม่สามารถโหลดรูปภาพได้ กรุณาตรวจสอบไฟล์."
                )
                self.standby_image_label.setStyleSheet("color: red; font-size: 24px;")
                app_logger.warning(f"Failed to load image at {self.logo_path}")
        else:
            self.standby_image_label.clear()
            self.standby_image_label.setText(
                f"⚠️ คำเตือน: ไม่พบไฟล์รูปภาพที่ '{self.logo_path}'"
            )
            self.standby_image_label.setStyleSheet("color: orange; font-size: 24px;")
            app_logger.warning(f"Logo file not found at {self.logo_path}")

        # Display greeting and instruction
        greeting = random.choice(GREETING_MESSAGES)
        self.standby_instruction_label.setText(
            f"<div style='font-size:40px;'>👋 {greeting}</div><br><br>"
            "<span style='font-size:30px;'>กดคีย์ใดก็ได้เพื่อเริ่ม<br>"
            "Press any key to start</span>"
        )
        self.standby_instruction_label.setStyleSheet("color: white;")

        # Stop idle timers in standby
        self.idle_timer.stop()
        self.warning_timer.stop()

    def go_to_standby(self):
        """Return to standby due to inactivity."""
        app_logger.info("Returning to standby due to inactivity")
        self.label.setText(
            "!!<br>ไม่ได้ใช้งานนาน กำลังกลับไปหน้าเริ่มต้น...<br>"
            "Inactive for a while. Returning to the start screen"
        )
        self.sound_manager.play_end_beep()
        QTimer.singleShot(2000, self.show_standby)

    def check_motion(self):
        """Check for motion to transition from standby."""
        if self.step == -1 and self._detect_motion():
            self.standby_instruction_label.setText(
                "🏇 พบการเคลื่อนไหว กำลังเริ่มปฎิบัติการ<br><br>"
                "🚨 I found your move ... activating"
            )
            self.sound_manager.play_start_beep()
            app_logger.info("Motion detected, starting greeting")

            self.showFullScreen()
            self.raise_()
            self.activateWindow()

            QTimer.singleShot(3000, self.go_to_greeting)

    def _detect_motion(self, threshold: int = 1000000, timeout: int = 5) -> bool:
        """
        Detect motion using camera.

        Args:
            threshold: Motion score threshold
            timeout: Maximum time to check for motion

        Returns:
            True if motion detected
        """
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                app_logger.warning("Cannot open camera for motion detection")
                return False

            start_time = time.time()
            motion_detected = False

            while time.time() - start_time < timeout:
                ret, frame1 = cap.read()
                time.sleep(0.1)
                ret, frame2 = cap.read()

                if not ret:
                    break

                # Calculate motion score
                diff = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                motion_score = np.sum(thresh)

                if motion_score > threshold:
                    motion_detected = True
                    break

            cap.release()
            return motion_detected

        except Exception as e:
            app_logger.error(f"Error in motion detection: {e}")
            return False

    def handle_idle_timeout(self):
        """Handle idle timer timeout."""
        if self.step == 0:  # At greeting, go to standby
            self.go_to_standby()
        elif self.step >= 1:  # In input/summary steps
            if not self.warning_shown:
                self.label.setText(
                    "<span style='font-size:32px;'>⚠<br>"
                    "หากไม่กรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที "
                    "หรือกด Esc เพื่อเริ่มต้นใหม่<br>"
                    "If no input is entered, the system will return to the start screen "
                    "in 30 sec, or press Esc to start over.</span>"
                )
                self.speech_engine.speak_thai(
                    "หากไม่มีการกรอกข้อมูล จะกลับไปยังหน้าเริ่มต้นใน 30 วินาที"
                )
                self.warning_shown = True
                self.warning_timer.start()

    def go_to_greeting(self):
        """Transition to greeting screen."""
        # Guard against multiple calls
        if self.step != -1:
            app_logger.debug(f"go_to_greeting called but step is {self.step}, skipping")
            return

        self.step = 0
        self.sound_manager.play_correct_sound()
        app_logger.info(f"Step {self.step}: Greeting")

        # Hide standby UI
        self.standby_image_label.hide()
        self.standby_instruction_label.hide()

        # Show active UI
        self.header.show()
        self.description.show()
        self.frame.show()

        # Configure input
        self.input.setReadOnly(True)
        self.input.setText("กด Enter เพื่อดำเนินการ ... Press Enter to proceed")
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setFocus()

        # Display greeting
        greeting = random.choice(GREETING_MESSAGES)
        self.frame.setStyleSheet(
            "background-color: #004080; border-radius: 30px; padding: 50px;"
        )
        self.label.setText(
            f"<div style='font-size:40px;'>👋 {greeting}</div><br><br>"
            "<span style='font-size:32px;'>ใส่คำสแลงของคุณ ความหมาย ตัวอย่าง "
            "เข้าไปในพจนานุกรมได้เลย<br>"
            "Add your slang word, meaning, and example to the dictionary</span><br><br><br>"
            "<span style='font-size:40px; color: #FFFF00;'>"
            "และรับปทานุกรมของคุณ เป็นที่ระลึกตอนท้าย<br>"
            "get your dictionary as souvenir at the end</span>"
        )

        app_logger.info(f"Greeting: {greeting}")
        QTimer.singleShot(100, lambda: self.speech_engine.speak_both(greeting))
        self.reset_idle_timer()

    def go_to_word_input(self):
        """Transition to word input step."""
        self.step = 1
        self.sound_manager.play_correct_sound()
        app_logger.info("Step 1: Word input")

        self.input.setReadOnly(False)
        self.input.setFocus()
        self.input.clear()

        self.label.setText(
            "<div style='font-size:40px;'>🖊️ พิมพ์คำสแลง แล้วกด Enter<br>"
            "Type a slang word and press Enter<br><br>"
            "<span style='font-size:32px;'>ตัวอย่างเช่น 'แจ่มแมว' หรือ 'เกียม'</span><br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>"
            "Press Escape to start over</span></div>"
        )

        QTimer.singleShot(300, lambda: self.speech_engine.speak_both(
            "พิมพ์คำสแลง<br>Drop your slang!"
        ))
        self.reset_idle_timer()

    def go_to_meaning_input(self):
        """Transition to meaning input step."""
        self.step = 2
        self.input.clear()
        app_logger.info("Step 2: Meaning input")

        self.label.setText(
            "<div style='font-size:40px;'>📖 พิมพ์ความหมาย แล้วกด Enter<br>"
            "Type the meaning and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>"
            "Press Escape to start over</span></div>"
        )

        QTimer.singleShot(300, lambda: self.speech_engine.speak_both(
            "พิมพ์ความหมาย<br>Meaning?"
        ))
        self.reset_idle_timer()

    def go_to_example_input(self):
        """Transition to example input step."""
        self.step = 3
        self.input.clear()
        app_logger.info("Step 3: Example input")

        self.label.setText(
            "<div style='font-size:40px;'>💬 พิมพ์ตัวอย่างประโยค แล้วกด Enter<br>"
            "Type an example sentence and press Enter<br><br>"
            "<span style='font-size:28px;'>กด Escape เพื่อเริ่มต้นใหม่<br>"
            "Press Escape to start over</span></div>"
        )

        QTimer.singleShot(300, lambda: self.speech_engine.speak_both(
            "พิมพ์ตัวอย่างประโยค<br>Example sentence?"
        ))
        self.reset_idle_timer()

    def go_to_summary(self):
        """Transition to summary confirmation step."""
        self.step = 4
        app_logger.info("Step 4: Summary")

        # Get data with truncation for display
        word_full = self.data.get("word", "N/A")
        meaning_full = self.data.get("meaning", "N/A")
        example_full = self.data.get("example", "N/A")

        word_display = (word_full[:40] + '...') if len(word_full) > 40 else word_full
        meaning_display = (meaning_full[:40] + '...') if len(meaning_full) > 40 else meaning_full
        example_display = (example_full[:40] + '...') if len(example_full) > 40 else example_full

        summary = (
            f"<div style='font-size:38px; text-align: center;'>"
            f"<b>คำศัพท์ | Word:</b> {word_display}<br>"
            f"<b>📖 ความหมาย | Meaning:</b> {meaning_display}<br>"
            f"<b>💬 ตัวอย่าง | Example:</b> {example_display}<br><br>"
            "<span style='font-size:40px; color: #FFFF00;'>รอการยืนยันจากคุณ<br>"
            "waiting for your confirmation</span></div>"
        )

        self.label.setText(summary)

        self.input.setReadOnly(True)
        self.input.setText(
            "Enter เพื่อยืนยัน หรือ Esc เพื่อยกเลิก  ...  "
            "Press Enter to confirm or Escape to abort"
        )
        self.input.setAlignment(Qt.AlignCenter)

        # Speak full text
        QTimer.singleShot(300, lambda: self.speech_engine.speak_thai(
            f"{word_full} หมายถึง {meaning_full} เช่น {example_full}"
        ))
        self.reset_idle_timer()

    def go_to_print_option(self):
        """Transition to print option step."""
        self.step = 5
        app_logger.info("Step 5: Print option")

        self.input.setReadOnly(False)
        self.input.clear()

        self.label.setText(
            "<div style='font-size:38px;'>🖨️ ต้องการพิมพ์ออกมาไหม?<br>Print your own dict?<br>"
            "<div style='font-size:42px; color: #FFFF00;'>"
            "👉 พิมพ์ชื่อของคุณเพื่อลงในหน้าผู้แต่งล่าสุด<br>"
            "Would you like to print it out? Type your name to appear as the latest author<br><br>"
            "</div>"
            "<span style='font-size:32px;'>หากไม่ต้องการใส่ชื่อหรือพิมพ์ออกมา กด Escape เพื่อข้าม<br>"
            "Press Escape to skip</span>"
        )

        QTimer.singleShot(300, lambda: self.speech_engine.speak_both(
            "พิมพ์ชื่อของคุณเพื่อลงในหน้าผู้แต่งล่าสุด<br>Your name for author?"
        ))
        self.reset_idle_timer()

    def next_step(self):
        """Handle logic for transitioning between steps."""
        text = self.input.text().strip()
        app_logger.info(f"Step {self.step}: Processing input")

        if self.step == 0:  # Greeting -> Word input
            self.go_to_word_input()
            self.input.clear()

        elif self.step == 1:  # Word input -> Meaning input
            if not text:
                self.label.setText(
                    "<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์คำสแลง<br>"
                    "Please type a slang word.</div>"
                )
                self.sound_manager.play_end_beep()
                QTimer.singleShot(1500, self.go_to_word_input)
                return

            self.data["word"] = text
            self.go_to_meaning_input()
            self.input.clear()

        elif self.step == 2:  # Meaning input -> Example input
            if not text:
                self.label.setText(
                    "<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์ความหมาย<br>"
                    "Please type the meaning.</div>"
                )
                self.sound_manager.play_end_beep()
                QTimer.singleShot(1500, self.go_to_meaning_input)
                return

            self.data["meaning"] = text
            self.go_to_example_input()
            self.input.clear()

        elif self.step == 3:  # Example input -> Summary
            if not text:
                self.label.setText(
                    "<div style='font-size:40px; color: red;'>⚠️ กรุณาพิมพ์ตัวอย่างประโยค<br>"
                    "Please type an example sentence.</div>"
                )
                self.sound_manager.play_end_beep()
                QTimer.singleShot(1500, self.go_to_example_input)
                return

            self.data["example"] = text
            self.go_to_summary()

        elif self.step == 4:  # Summary -> Print option (save data)
            self.save_data()
            self.go_to_print_option()

        elif self.step == 5:  # Print option (author name)
            if text:  # User provided author name
                self.data["author"] = text
                self._handle_print_with_author(text)
            else:  # User skipped
                self.label.setText(
                    "ขอบคุณที่ใช้บริการ! กลับสู่หน้าเริ่มต้น<br>"
                    "Thank you! Returning to start screen"
                )
                self.sound_manager.play_end_beep()
                QTimer.singleShot(1000, self.show_standby)

            self.input.clear()

        self.reset_idle_timer()

    def _handle_print_with_author(self, author: str):
        """Handle printing with author name."""
        # Update author in database
        self._save_author_to_latest_entry(self.data["word"], author)

        # Show printing message
        self.label.setText(
            f"🖨️ กำลังพิมพ์... ขอบคุณ {author} มากนะ<br>"
            f"Printing your dictionary, thanks {author}"
        )
        self.sound_manager.play_correct_sound()
        self.reset_idle_timer()

        # Delayed actions for PDF generation and special requests
        def delayed_actions():
            try:
                # Import and call PDF generator
                if self.mode == AppMode.LAST_WEEK:
                    from slang_pdf_generator_lastweek import printpdf
                else:
                    from slang_pdf_generator import printpdf

                printpdf(author=author)

                app_logger.info("Starting routine request check")
                self.reset_idle_timer()

                # Check for routine/special requests
                got_jackpot = self._run_routine_request_if_exists()

                if got_jackpot:
                    self.reset_idle_timer()
                    self._run_special_request_if_exists()
                    QTimer.singleShot(10000, self.show_standby)
                else:
                    QTimer.singleShot(8500, self.show_standby)

            except Exception as e:
                app_logger.error(f"Error in delayed actions: {e}")
                QTimer.singleShot(3000, self.show_standby)

        QTimer.singleShot(5, delayed_actions)

    def keyPressEvent(self, event):
        """Global key press event handler."""
        self.reset_idle_timer()

        if event.key() == Qt.Key_Escape:
            if self.step in [1, 2, 3, 4, 5]:  # Active steps
                self.label.setText(
                    "❌ ยกเลิก กำลังกลับเริ่มโปรแกรมใหม่...<br>"
                    "Cancelling. Returning to start screen."
                )
                self.sound_manager.play_end_beep()
                QTimer.singleShot(1000, self.show_standby)
            elif self.step == -1:  # Standby - Esc acts as any key
                app_logger.debug("Esc in standby, triggering greeting")
                self.go_to_greeting()
        elif self.step == -1:  # Any key in standby
            app_logger.debug("Key press in standby, triggering greeting")
            self.go_to_greeting()
        else:
            # Pass to input field if it has focus
            if isinstance(self.focusWidget(), QLineEdit):
                super().keyPressEvent(event)

    def save_data(self):
        """Save the new slang entry to database using legacy format."""
        word = self.data.get("word")
        meaning = self.data.get("meaning")
        example = self.data.get("example")

        if not word:
            app_logger.warning("Attempted to save data without word")
            return

        app_logger.info(f"Saving entry: {word}")

        # Load existing data directly (legacy format compatibility)
        json_file = self.database.db_file
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            import json

            if os.path.exists(json_file):
                with open(json_file, "r", encoding="utf-8") as f:
                    slang_data = json.load(f)
            else:
                slang_data = {}

            # Use legacy format: lists for meanings/examples
            if word not in slang_data:
                slang_data[word] = {
                    "meaning": [meaning],
                    "example": [example],
                    "reach": 1,
                    "update": now,
                    "author": []
                }
            else:
                entry = slang_data[word]
                if meaning and meaning not in entry["meaning"]:
                    entry["meaning"].append(meaning)
                if example and example not in entry["example"]:
                    entry["example"].append(example)
                entry["reach"] = entry.get("reach", 0) + 1
                entry["update"] = now

            # Save to file
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(slang_data, f, ensure_ascii=False, indent=4)

            app_logger.info(f"Saved entry to {json_file}")
            self.sound_manager.play_correct_sound()

        except Exception as e:
            app_logger.error(f"Error saving data: {e}")

    def _save_author_to_latest_entry(self, word: str, author_name: str):
        """Update author list for specific word in legacy format."""
        json_file = self.database.db_file

        try:
            import json

            if not os.path.exists(json_file):
                app_logger.warning(f"Database file not found: {json_file}")
                return

            with open(json_file, "r", encoding="utf-8") as f:
                slang_data = json.load(f)

            if word in slang_data:
                entry = slang_data[word]
                authors = entry.get("author", [])

                # Move existing author to end
                if author_name in authors:
                    authors.remove(author_name)
                authors.append(author_name)

                entry["author"] = authors

                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(slang_data, f, ensure_ascii=False, indent=4)

                app_logger.info(f"Updated author for '{word}'")
            else:
                app_logger.warning(f"Word '{word}' not found in database")

        except Exception as e:
            app_logger.error(f"Error saving author: {e}")

    def _run_routine_request_if_exists(self) -> bool:
        """Check and run routine request script."""
        import importlib.util
        import traceback

        request_path = "request_routine.py"
        app_logger.info(f"Checking for {request_path}")

        if os.path.exists(request_path):
            app_logger.info(f"{request_path} found, running routine_request()")

            spec = importlib.util.spec_from_file_location("request", request_path)
            request_module = importlib.util.module_from_spec(spec)

            try:
                spec.loader.exec_module(request_module)
                if hasattr(request_module, 'routine_request'):
                    request_module.routine_request()
                    app_logger.info("routine_request() executed successfully")
                    return True
                else:
                    app_logger.warning(f"routine_request() not found in {request_path}")
            except Exception as e:
                app_logger.error(f"Error loading {request_path}: {e}")
                app_logger.error(traceback.format_exc())
        else:
            app_logger.info(f"{request_path} not found, skipping")

        return False

    def _run_special_request_if_exists(self):
        """Check and run special request script."""
        import importlib.util
        import traceback

        request_path = "request_special.py"
        app_logger.info(f"Checking for {request_path}")

        if os.path.exists(request_path):
            app_logger.info(f"{request_path} found, checking probability")

            # 15% chance to run special request
            run_special_draw = random.randint(1, 100)
            app_logger.info(f"Special request draw: {run_special_draw}")

            if run_special_draw > 85:
                app_logger.info("Running special_request")

                spec = importlib.util.spec_from_file_location("request", request_path)
                request_module = importlib.util.module_from_spec(spec)

                try:
                    spec.loader.exec_module(request_module)
                    if hasattr(request_module, 'special_request'):
                        request_module.special_request()
                        app_logger.info("special_request() executed successfully")
                    else:
                        app_logger.warning(f"special_request() not found in {request_path}")
                except Exception as e:
                    app_logger.error(f"Error in special_request(): {e}")
                    app_logger.error(traceback.format_exc())
                finally:
                    try:
                        os.remove(request_path)
                        app_logger.info(f"{request_path} deleted after execution")
                    except Exception as e:
                        app_logger.warning(f"Failed to delete {request_path}: {e}")
        else:
            app_logger.info(f"{request_path} not found, skipping")


def start_gui_and_get_entry(database: SlangDatabase, easter_eggs: EasterEggManager,
                            speech_engine: SpeechEngine, sound_manager: SoundManager,
                            mode: str = AppMode.NORMAL):
    """
    Start the QApplication and run the SlangKiosk.

    Args:
        database: SlangDatabase instance
        easter_eggs: EasterEggManager instance
        speech_engine: SpeechEngine instance
        sound_manager: SoundManager instance
        mode: Application mode
    """
    app = QApplication(sys.argv)
    kiosk = SlangKiosk(database, easter_eggs, speech_engine, sound_manager, mode)
    kiosk.show()
    sys.exit(app.exec_())
