### request_special.py

from input_slang_utils import speak_thai, speak_both, log_request_message
import subprocess
from datetime import datetime
import fitz  # PyMuPDF

from playsound import playsound # Correct import: playsound is now the function directly
win_sound = "correct sound/8-bit-video-game-lose-sound-version-1-145828.mp3"

def special_request():
    """คำสั่งพิเศษในการพิมพ์ จะรันครั้งเดียว แล้วลบไฟล์นี้ทิ้ง"""


    print("🔧 Running special request...")
    log_request_message("🔧 Running special request...")
    
    playsound(win_sound) # Corrected call
    speak_both("โอ้ว คอมพิวเตอร์พึ่งถูกแฮกไปเมื่อครู่<br>Oh,this computer was hacked just now!")
    show_jackpot_popup(title = "<br>🎉🎉 Big Jackpot 🎉🎉<br>", message = "<br>คุณคือ 1 ใน 20 คนเท่านั้น<br>ที่โชคดีพอจะได้เห็น<br>หน้าปทานุกรมทั้งหมด<br><br><br>You are one of only 20 lucky individuals<br>granted access to view<br>the entire Lexicon interface.<br><br>", timeout=10000)
    
    ############################
    ## First Request
    if True :
        pdf_path = "output/slang_dictionary.pdf"
        partial_path = "output/slang_dictionary_partial.pdf"

        try:
            # ตรวจสอบจำนวนหน้าในไฟล์ PDF
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            doc.close()

            make_partial_pdf(
                input_pdf=pdf_path,
                output_pdf=partial_path,
                start_page=1,
                end_page=total_pages - 1  # หน้าแรกถึงก่อนสุดท้าย
            )


            if total_pages < 2:
                log_request_message("❗ Not enough pages to skip the last one.")
                return

            page_range = f"page-ranges=1-{total_pages - 1}"

            cmd1 = [
                'lp',
                '-d', 'Canon_LBP121_122',
                '-o', 'orientation-requested=4',
                '-o', 'number-up=9',
                partial_path
            ]

            print(f"Request1: {' '.join(cmd1)}")
            log_request_message(f"🔧 cmd1: {' '.join(cmd1)}")

            output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
            print("✅ Request1 success")
            log_request_message(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Request1 error: {e}")
            log_request_message(f"❌ Request1 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request1: {e}")
            log_request_message(f"❌ Unexpected error in Request1: {e}")

    ############################
    ## Second Request
    if True :
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
    if True :
        #cmd3 = ['cmd', '/c', 'dir']
        cmd3 = ['ls', '-la', 'output']
        print(f"Request3: {' '.join(cmd3)}")
        log_request_message(f"🔧 cmd3: {' '.join(cmd3)}")

        try:
            output = subprocess.run(cmd3, check=True, capture_output=True, text=True)
            print("✅ Request3 success")
            log_request_message(f"✅ Request3 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request3 error: {e}")
            log_request_message(f"❌ Request3 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request3: {e}")
            log_request_message(f"❌ Unexpected error in Request3: {e}")
            
            
from PyPDF2 import PdfReader, PdfWriter
import os

def make_partial_pdf(input_pdf, output_pdf, start_page, end_page):
    # แยกหน้า
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):  # zero-based index
        writer.add_page(reader.pages[i])

    with open(output_pdf, "wb") as f:
        writer.write(f)


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