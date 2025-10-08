# input_slang_gui.py

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

def start_gui_and_get_entry():
    app = QApplication([])

    # ปรับฟอนต์เริ่มต้น
    font = QFont("Tahoma", 18)
    app.setFont(font)

    result = {}

    class InputWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("🧠 เพิ่มคำสแลงใหม่")
            self.setGeometry(0, 0, 800, 600)
            self.setStyleSheet("background-color: #fefae0;")

            # จัดวาง Layout
            self.layout = QVBoxLayout()

            # Header
            header = QLabel("📚 พจนานุกรมคำสแลงไทย")
            header.setFont(QFont("Tahoma", 28, QFont.Bold))
            header.setAlignment(Qt.AlignCenter)
            header.setStyleSheet("color: #283618;")

            # Description
            description = QLabel("✍️ กรุณาเติมคำสแลง ความหมาย และตัวอย่างประโยค\nระบบจะบันทึกลงพจนานุกรมอัตโนมัติ")
            description.setFont(QFont("Tahoma", 16))
            description.setAlignment(Qt.AlignCenter)
            description.setStyleSheet("color: #606c38;")

            self.layout.addWidget(header)
            self.layout.addWidget(description)

            # Spacer
            self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # สร้างกรอบกรอกข้อมูล
            form_frame = QFrame()
            form_frame.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border-radius: 20px;
                    padding: 30px;
                    border: 2px solid #dda15e;
                }
            """)
            form_layout = QVBoxLayout()

            # 📝 คำสแลง
            self.label_word = QLabel("📝 คำสแลง:")
            self.input_word = QLineEdit()
            self.input_word.returnPressed.connect(self.goto_meaning)

            # 📖 ความหมาย
            self.label_meaning = QLabel("📖 ความหมาย:")
            self.input_meaning = QLineEdit()
            self.input_meaning.returnPressed.connect(self.goto_example)

            # 💬 ตัวอย่างประโยค
            self.label_example = QLabel("💬 ตัวอย่างประโยค:")
            self.input_example = QLineEdit()
            self.input_example.returnPressed.connect(self.finish)

            # ตั้งค่ารูปแบบ Label + Input
            label_style = "color: #bc6c25; font-weight: bold;"
            input_style = "padding: 10px; font-size: 18px;"

            for label in [self.label_word, self.label_meaning, self.label_example]:
                label.setStyleSheet(label_style)
                label.setFont(QFont("Tahoma", 18))

            for input_field in [self.input_word, self.input_meaning, self.input_example]:
                input_field.setStyleSheet(input_style)

            # ใส่ใน Layout
            form_layout.addWidget(self.label_word)
            form_layout.addWidget(self.input_word)
            form_layout.addWidget(self.label_meaning)
            form_layout.addWidget(self.input_meaning)
            form_layout.addWidget(self.label_example)
            form_layout.addWidget(self.input_example)

            form_frame.setLayout(form_layout)
            self.layout.addWidget(form_frame, alignment=Qt.AlignCenter)

            # Spacer
            self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            self.setLayout(self.layout)
            self.input_word.setFocus()

        def goto_meaning(self):
            self.input_meaning.setFocus()

        def goto_example(self):
            self.input_example.setFocus()

        def finish(self):
            result["word"] = self.input_word.text()
            result["meaning"] = self.input_meaning.text()
            result["example"] = self.input_example.text()
            self.close()

    window = InputWindow()
    window.showMaximized()
    app.exec_()

    return result if result else None
