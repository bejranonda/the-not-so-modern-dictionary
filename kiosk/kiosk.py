from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QDialog
)
from PyQt5.QtCore import Qt
import sys

class BigMessageBox(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet("""
            background-color: black; 
            color: white; 
            font-size: 32px; 
            font-weight: bold;
        """)
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)

        btn = QPushButton("ตกลง")
        btn.setStyleSheet("font-size: 28px; padding: 12px;")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

def add_word():
    word = input_field.text().strip()
    if word:
        dlg = BigMessageBox("คำที่เพิ่ม", f"✅ คุณเพิ่มคำสแลง: {word}", window)
        dlg.exec_()
        input_field.clear()
    else:
        dlg = BigMessageBox("ข้อผิดพลาด", "⚠️ กรุณากรอกคำก่อนกดเพิ่ม", window)
        dlg.exec_()

def on_return_pressed():
    add_word()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowFlags(Qt.FramelessWindowHint)
window.showFullScreen()

layout = QVBoxLayout()

label = QLabel("📝 กรุณาพิมพ์คำสแลงที่ต้องการเพิ่ม")
label.setAlignment(Qt.AlignCenter)
label.setStyleSheet("font-size: 40px; color: white;")
layout.addWidget(label)

input_field = QLineEdit()
input_field.setPlaceholderText("พิมพ์คำที่นี่...")
input_field.setStyleSheet("font-size: 32px; padding: 12px;")
input_field.returnPressed.connect(on_return_pressed)  # กด Enter เรียกฟังก์ชัน
layout.addWidget(input_field)

button = QPushButton("➕ เพิ่มคำสแลง")
button.setStyleSheet("font-size: 32px; padding: 12px;")
button.clicked.connect(add_word)
layout.addWidget(button)

window.setStyleSheet("background-color: black; color: white;")
window.setLayout(layout)
window.show()

sys.exit(app.exec_())
