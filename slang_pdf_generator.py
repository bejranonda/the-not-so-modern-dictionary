## slang_pdf_generator.py

import json
import os
import platform
import subprocess
import fitz  # PyMuPDF
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import locale
locale.setlocale(locale.LC_COLLATE, 'th_TH.UTF-8')
import random
from PyPDF2 import PdfReader, PdfWriter
import re

# 📐 Global constants
width, height = A4
margin_left = 70
margin_right = margin_left
margin_top = height - 80
margin_bottom = 70
margin_newpage = 100
line_space = 20
usable_width = width - margin_left - margin_right

title_font_size = 20
header_font_size = 17
content_font_size = 14

def get_main_thai_consonant(word):
    """
    Return the first Thai consonant character from the word.
    Skips Thai vowels like เ, แ, โ, ใ, ไ which are leading vowels.
    """
    # พยัญชนะไทยช่วง \u0E01-\u0E2E
    match = re.search(r'[\u0E01-\u0E2E]', word)
    if match:
        return match.group(0)
    return word[0] if word else ''
    
def register_fonts(thai_font_path, thai_bold_font_path, thai_italic_font_path, emoji_font_path):
    pdfmetrics.registerFont(TTFont("Kinnari", thai_font_path))
    pdfmetrics.registerFont(TTFont("Kinnari-Bold", thai_bold_font_path))
    pdfmetrics.registerFont(TTFont("Kinnari-Italic", thai_italic_font_path))
    pdfmetrics.registerFont(TTFont("EmojiFont", emoji_font_path))

def draw_title(c, text, y):
    draw_mixed_text_centered(c, text, width / 2, y, "Kinnari", title_font_size, "EmojiFont", title_font_size)

def get_star_rating(reach, max_reach):
    if max_reach == 0:
        return ""
    ratio = reach / max_reach
    if ratio > 0.8:
        return " ⭐⭐⭐"
    elif ratio > 0.5:
        return " ⭐⭐"
    elif ratio > 0.2:
        return " ⭐"
    else:
        return ""
       

def draw_intro_page(c, total_words, total_meanings, total_reach, latest_word, hottest_word, y_start, lastauthor, totalauthor):
    updated_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    text_lines = [
        f"🖨 พิมพ์ที่: Bangkok Kunsthalle",
        f"🔢 พิมพ์ครั้งที่: {total_reach:,}",
        f"📅 ปรับปรุงล่าสุด: {updated_date}",
        f"🏢 สำนักพิมพ์: ยุงลาย",
        f"📝 ผู้แต่ง: {totalauthor} คน",
        f"📝 ผู้แต่งล่าสุด: {lastauthor}",
        f"🧾 คำศัพท์ทั้งหมด: {total_words:,} คำ",
        f"🆕 คำล่าสุด: {latest_word}",
        f"📚 คลังตัวอย่าง: {total_meanings:,} ชุด",
        f"🔥 คำที่ฮิตที่สุด:",

    ]

    draw_title(c, "📖 ข้อมูลปทานุกรม", y_start)
    y = y_start - line_space * 3

    # Statistic
    for line in text_lines:
        y, _ = draw_mixed_text_wrapped(
            c, line, margin_left, y,
            "Kinnari", content_font_size*1.3, "EmojiFont", content_font_size*1.2)
        y -= line_space*1.1

    # List of hottest word
    y += line_space*0.5
    for line in hottest_word:
        y, _ = draw_mixed_text_wrapped(
            c, f"   • {line}", margin_left, y,
            "Kinnari", content_font_size*1.3, "EmojiFont", content_font_size*1.2)
        y -= line_space*1

    draw_page_number(c)
    c.showPage()

def draw_fortune_page(c, fortune_data):
    draw_page_number(c)
    c.showPage()

    y = margin_top
    draw_title(c, "🪄 ปทานุกรมทำนาย - FortuneDict 🪄", y)
    y -= line_space * 4
    indent = 10

    # สุ่มเลือกคำเดียว
    word = random.choice(list(fortune_data.keys()))
    fortune = fortune_data[word]

    # เช็คพื้นที่
    if y < margin_bottom + line_space * 4:
        draw_page_number(c)
        c.showPage()
        y = margin_top
        draw_title(c, "ศัพท์ทำนาย - FortueDict", y)
        y -= line_space * 4

    # แสดงสัญลักษณ์
    c.setFont("EmojiFont", header_font_size*3)
    c.drawCentredString(width / 2, y, "🔮")
    y -= line_space*4
    # แสดงหัวข้อคำศัพท์
    c.setFont("Kinnari-Bold", header_font_size * 2.5)
    c.drawCentredString(width / 2, y, word)
    y -= line_space*2
    
    # แสดงคำอธิบาย (wrap ข้อความ)
    c.setFont("Kinnari-Italic", header_font_size*1.5)
    c.drawCentredString(width / 2, y, "ศัพท์ทำนายสำหรับคุณ")

    y -= line_space*4

    # แสดงข้อความคำทำนาย ไทย
    y, _ = draw_mixed_text_wrapped(
        c, fortune["th"], margin_left + indent, y,
        "Kinnari", content_font_size*2,
        "EmojiFont", content_font_size*2,
        round(line_space*2.5)
    )
    y -= line_space*1

    # แสดงข้อความคำทำนาย อังกฤษ
    y, _ = draw_mixed_text_wrapped(
        c, fortune["en"], margin_left + indent, y,
        "Kinnari", content_font_size*2,
        "EmojiFont", content_font_size*2,
        round(line_space*2.5)
    )
    y -= line_space*2
    
    draw_page_number(c)
    #c.showPage()



    
def draw_entry(c, word, info, x, y, line_height, max_reach, indent=10):
    reach = info.get("reach", 1)
    stars = get_star_rating(reach, max_reach)

    # Header + stars
    y, _ = draw_mixed_text_wrapped(
        c, f" {word}{stars}", x, y,
        "Kinnari-Bold", header_font_size, "EmojiFont", round(header_font_size * 0.7), line_height)
    y -= line_height * 0.2

    # Meanings
    meanings = info.get("meaning", [])
    if isinstance(meanings, str):
        meanings = [meanings]
    for m in meanings:
        if y < margin_bottom + line_height * 3:
            draw_page_number(c)
            c.showPage()
            y = margin_top
            # หาอักษรแรกของคำศัพท์ที่จะใช้แสดงในหัวเรื่อง
            first_char_on_page = get_main_thai_consonant(word)  # ใช้ตัวอักษรแรกของคำนี้
            draw_title(c, f"📚 ปทานุกรมแบบสับ - {first_char_on_page}", y)
            #draw_title(c, "📚 ปทานุกรมแบบสับ", y)
            y -= line_height * 2

        y, _ = draw_mixed_text_wrapped(
            c, f"📝 {m}", x + indent, y,
            "Kinnari", content_font_size, "EmojiFont", content_font_size - 2, line_height)
        y -= line_height * 0.2

    # Examples
    examples = info.get("example", [])
    if isinstance(examples, str):
        examples = [examples]
    for ex in examples:
        if y < margin_bottom + line_height * 3:
            draw_page_number(c)
            c.showPage()
            y = margin_top
            first_char_on_page = get_main_thai_consonant(word)  # ใช้ตัวอักษรแรกของคำนี้
            draw_title(c, f"📚 ปทานุกรมแบบสับ - {first_char_on_page}", y)
            y -= line_height * 2

        y, _ = draw_mixed_text_wrapped(
            c, f"💬 {ex}", x + indent, y,
            "Kinnari", content_font_size, "EmojiFont", content_font_size - 2, line_height)
        y -= line_height * 0.2

    # Reach number
    y += line_height * 0.3
    y, _ = draw_mixed_text_wrapped(
        c, f" 📈 {reach}", x + indent, y,
        "Kinnari", round(content_font_size*0.9), "EmojiFont", round(content_font_size*0.8), round(line_height * 0.8))

    y -= line_height * 2
    return y


def draw_latest_word_page(c, word, info):
    y = margin_top
    draw_title(c, "🆕 ศัพท์ใหม่ล่าสุด", y)
    y -= line_space * 3

    # แสดงคำใหญ่
    c.setFont("Kinnari-Bold", header_font_size * 2)
    c.drawCentredString(width / 2, y, word)
    y -= line_space * 3

    # Meaning
    meanings = info.get("meaning", [])
    if isinstance(meanings, str):
        meanings = [meanings]
    meanings = meanings[-4:]  # แสดง 4 ชุดล่าสุด
    
    y, _ = draw_mixed_text_wrapped(
    c, f"📝 ความหมาย:", margin_left, y,
    "Kinnari", content_font_size * 1.8,
    "EmojiFont", content_font_size * 1.8,
    line_space*1)
    y -= line_space

    for m in meanings:
        y, _ = draw_mixed_text_wrapped(
            c, f" 🔹 {m}", margin_left, y,
            "Kinnari", content_font_size * 1.5,
            "EmojiFont", content_font_size * 1.5,
            line_space*1)
        y -= line_space
    y -= line_space
    
    # Samples
    examples = info.get("example", [])
    if isinstance(examples, str):
        examples = [examples]
    examples = examples[-4:]  # แสดง 4 ชุดล่าสุด
    
    y, _ = draw_mixed_text_wrapped(
    c, f"💬 ตัวอย่าง:", margin_left, y,
    "Kinnari", content_font_size * 1.8,
    "EmojiFont", content_font_size * 1.8,
    line_space*1)
    y -= line_space
    
    for ex in examples:
        y, _ = draw_mixed_text_wrapped(
            c, f" 🔹 {ex}", margin_left, y,
            "Kinnari", content_font_size * 1.5,
            "EmojiFont", content_font_size * 1.5,
            line_space *1)
        y -= line_space

    # เพิ่มชื่อผู้แต่งล่าสุดถ้ามี
    author_list = info.get("author")
    if isinstance(author_list, list) and author_list:
        author = author_list[-1]  # คนสุดท้ายใน list
    elif isinstance(author_list, str):
        author = author_list
    else:
        author = None

    if author:
        y -= line_space * 2
        y, _ = draw_mixed_text_wrapped(
            c, f"📝 ผู้แต่งล่าสุด: {author}", margin_left, y,
            "Kinnari", content_font_size * 2,
            "EmojiFont", content_font_size * 2,
            line_space * 1.5)

    draw_page_number(c)
    c.showPage()


def draw_mixed_text(c, text, x, y, font1, size1, font2, size2):
    current_x = x
    for ch in text:
        if ord(ch) > 0x1F000 or ord(ch) == 0x2B50:
            c.setFont(font2, size2)
        else:
            c.setFont(font1, size1)
        c.drawString(current_x, y, ch)
        current_x += stringWidth(ch, c._fontname, c._fontsize)

def draw_mixed_text_centered(c, text, center_x, y, font1, size1, font2, size2):
    total_width = sum(stringWidth(ch, font2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else font1, size2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else size1) for ch in text)
    start_x = center_x - total_width / 2
    draw_mixed_text(c, text, start_x, y, font1, size1, font2, size2)

def draw_mixed_text_wrapped(c, text, x, y, font1, size1, font2, size2, line_height=line_space):
    lines = []
    current_line = ''
    current_width = 0
    for ch in text:
        font = font2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else font1
        size = size2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else size1
        ch_width = stringWidth(ch, font, size)
        if current_width + ch_width > usable_width - (x - margin_left):
            lines.append(current_line)
            current_line = ch
            current_width = ch_width
        else:
            current_line += ch
            current_width += ch_width
    if current_line:
        lines.append(current_line)

    for line in lines:
        draw_mixed_text(c, line, x, y, font1, size1, font2, size2)
        y -= line_height

    return y, len(lines)

# ➕ ฟังก์ชันใหม่: ใส่เลขหน้า
def draw_page_number(c):
    page_num = c.getPageNumber()
    text = f"- {page_num} -"
    font_size = 12
    text_width = stringWidth(text, "Kinnari", font_size)
    x = (width - text_width) / 2
    y = 25
    c.setFont("Kinnari", font_size)
    c.drawString(x, y, text)

def add_template_background(template_path, input_pdf_path, output_pdf_path):
    template_doc = fitz.open(template_path)
    input_doc = fitz.open(input_pdf_path)

    try:
        template_page = template_doc.load_page(0)
        bg_pix = template_page.get_pixmap(alpha=False)
        bg_img_rect = template_page.rect

        # ใส่ background เฉพาะหน้าที่ 5 ถึงหน้าสุดท้าย (index 4 ขึ้นไป)
        for page_num in range(4, len(input_doc)):
            page = input_doc.load_page(page_num)
            page.insert_image(bg_img_rect, pixmap=bg_pix, overlay=False)

        input_doc.save(output_pdf_path)
    finally:
        template_doc.close()
        input_doc.close()

def make_foldable_booklet(input_path, output_path):
    doc = fitz.open(input_path)
    total_pages = len(doc)
    w, h = 842, 595
    if total_pages < 8:
        print(f"PDF total_pages: {total_pages}")    
        for _ in range(8 - total_pages):
            doc.new_page(width=w, height=h)
            
    section_w, section_h = w / 4, h / 2
    page_order = [0, 1, 2, 3, 4, 5, random.randint(6, total_pages-2), total_pages-1]
    #page_order_standard = [7, 0, 1, 6, 5, 2, 3, 4]
    output_doc = fitz.open()
    new_page = output_doc.new_page(width=w, height=h)
    for i, idx in enumerate(page_order):
        if idx >= len(doc): continue
        src_page = doc.load_page(idx)
        text = src_page.get_text("text").strip()
        #if not text: continue
        col, row = i % 4, 0 if i < 4 else 1
        x0, y0 = col * section_w, row * section_h
        target_rect = fitz.Rect(x0, y0, x0 + section_w, y0 + section_h)
        
        # rotate the first 4 pages
        rotation = 180 if i < 4 else 0
        new_page.show_pdf_page(target_rect, doc, idx, rotate=rotation)
        #new_page.show_pdf_page(target_rect, doc, idx)
    output_doc.save(output_path)

def merge_pdfs(append_pdf_path, base_pdf_path, output_pdf_path):
    writer = PdfWriter()

    # เพิ่ม append ก่อน → กลายเป็นหน้า 1 เป็นต้นไป
    append_pdf = PdfReader(append_pdf_path)
    for page in append_pdf.pages:
        writer.add_page(page)

    # ตามด้วย base
    base_pdf = PdfReader(base_pdf_path)
    for page in base_pdf.pages:
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as out_f:
        writer.write(out_f)


def print_pdf_file(pdf_path, printer_name=None):
    """
    Prints a PDF file to the specified printer on Windows or Linux/macOS.
    For Windows, it attempts to use PowerShell for silent printing,
    then falls back to specific PDF viewers (Adobe Reader, SumatraPDF) if needed.
    For Windows without a named printer, it opens the print dialog.
    For Linux/macOS, it uses the `lpr` command.
    """
    # Convert to absolute path
    abs_pdf_path = os.path.abspath(pdf_path)

    print(f"กำลังสั่งพิมพ์ไฟล์: {abs_pdf_path}")
    if not os.path.exists(abs_pdf_path):
        print(f"❌ ข้อผิดพลาด: ไม่พบไฟล์ PDF ที่ {abs_pdf_path} ไม่สามารถสั่งพิมพ์ได้")
        return
    
    system = platform.system()
    print(f"ระบบปฏิบัติการที่ตรวจพบ: {system}")

    if system == "Windows":
        printed_successfully = False
        
        # --- Attempt 1: Using PowerShell with PrintTo verb (relies on default app association) ---
        if printer_name:
            cmd = f'PowerShell.exe -Command "Start-Process -FilePath \'{abs_pdf_path}\' -Verb PrintTo -ArgumentList \'{printer_name}\'"'
            print(f"คำสั่ง Windows (PowerShell - PrintTo): {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True, creationflags=subprocess.SW_HIDE) # SW_HIDE to try to hide window
                print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน PowerShell PrintTo)")
                print("หากไม่เห็นงานพิมพ์ โปรดตรวจสอบคิวงานพิมพ์ของเครื่องพิมพ์และโปรแกรมดู PDF เริ่มต้น")
                printed_successfully = True
            except subprocess.CalledProcessError as e:
                print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (PowerShell PrintTo): {e.stderr.decode('utf-8') if e.stderr else 'ไม่มีรายละเอียด'}")
                print("   สาเหตุอาจเกิดจาก: ไม่มีแอปพลิเคชันเชื่อมโยงกับไฟล์ PDF หรือการเชื่อมโยงเสียหาย")
                print("   กำลังลองวิธีอื่น...")
            except FileNotFoundError:
                print(f"❌ ข้อผิดพลาด: ไม่พบ PowerShell หรือ Start-Process. กำลังลองวิธีอื่น...")
            except Exception as e:
                print(f"❌ ข้อผิดพลาดที่ไม่คาดคิดในการสั่งพิมพ์ (PowerShell PrintTo): {e}. กำลังลองวิธีอื่น...")
        
        # --- Attempt 2: Using known PDF viewers directly (if Attempt 1 fails or no printer_name) ---
        if not printed_successfully and printer_name:
            # Try Adobe Reader
            adobe_reader_paths = [
                r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
                r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"
            ]
            for adobe_path in adobe_reader_paths:
                if os.path.exists(adobe_path):
                    cmd = [adobe_path, "/N", "/T", abs_pdf_path, printer_name]
                    print(f"คำสั่ง Windows (Adobe Reader): {' '.join(cmd)}")
                    try:
                        subprocess.run(cmd, check=True, creationflags=subprocess.SW_HIDE)
                        print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน Adobe Reader)")
                        printed_successfully = True
                        break
                    except Exception as e:
                        print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (Adobe Reader): {e}")
                        continue
            
            if not printed_successfully:
                # Try SumatraPDF
                sumatra_paths = [
                    r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
                    r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe"
                ]
                for sumatra_path in sumatra_paths:
                    if os.path.exists(sumatra_path):
                        cmd = [sumatra_path, "-print-to", printer_name, abs_pdf_path]
                        print(f"คำสั่ง Windows (SumatraPDF): {' '.join(cmd)}")
                        try:
                            subprocess.run(cmd, check=True, creationflags=subprocess.SW_HIDE)
                            print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน SumatraPDF)")
                            printed_successfully = True
                            break
                        except Exception as e:
                            print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (SumatraPDF): {e}")
                            continue

        # --- Final Fallback for Windows if all silent methods fail or no printer_name ---
        if not printed_successfully:
            print(f"⚠️ ไม่สามารถสั่งพิมพ์แบบเงียบได้ หรือไม่มีชื่อเครื่องพิมพ์ที่ระบุ")
            print(f"   กำลังสั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' โดยเปิดกล่องโต้ตอบการพิมพ์ (โปรดกดพิมพ์ด้วยตนเอง)")
            try:
                os.startfile(abs_pdf_path, "print")
                print("✅ คำสั่งเปิดกล่องโต้ตอบการพิมพ์ถูกส่งแล้ว")
            except Exception as e:
                print(f"❌ ข้อผิดพลาดในการเปิดกล่องโต้ตอบการพิมพ์: {e}")
                print("   โปรดตรวจสอบการตั้งค่าโปรแกรมดู PDF เริ่มต้นและสิทธิ์การเข้าถึง")
                print("   หากปัญหายังคงอยู่: โปรดติดตั้งโปรแกรมดู PDF เช่น Adobe Reader หรือ SumatraPDF และตั้งค่าให้เป็นโปรแกรมเริ่มต้นสำหรับไฟล์ PDF")

    elif system == "Darwin" or system == "Linux": # Darwin คือ macOS
        try:
            # ใช้คำสั่ง lpr บน Linux/macOS (ระบบ CUPS)
            cmd = ["lpr"]
            if printer_name:
                cmd.extend(["-P", printer_name])
            cmd.append(abs_pdf_path)
            
            print(f"คำสั่ง Linux/macOS (lpr): {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name if printer_name else 'default'}' บน {system} เรียบร้อยแล้ว")
            print("หากไม่เห็นงานพิมพ์ โปรดตรวจสอบคิวงานพิมพ์ของเครื่องพิมพ์")
        except subprocess.CalledProcessError as e:
            print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์บน {system}: การเรียกใช้ 'lpr' ล้มเหลว. รหัสข้อผิดผิดพลาด: {e.returncode}")
            print(f"   รายละเอียด: {e.stderr.decode('utf-8') if e.stderr else 'ไม่มี'}")
            print("   โปรดตรวจสอบว่าเครื่องพิมพ์ถูกติดตั้งและกำหนดค่าอย่างถูกต้องบน CUPS")
        except FileNotFoundError:
            print(f"❌ ข้อผิดพลาด: ไม่พบคำสั่ง 'lpr'.")
            print(f"   โปรดตรวจสอบว่า CUPS ถูกติดตั้งและตั้งค่าอย่างถูกต้องบน {system} ของคุณ")
        except Exception as e:
            print(f"❌ ข้อผิดพลาดที่ไม่คาดคิดในการสั่งพิมพ์บน {system}: {e}")
            print("   โปรดตรวจสอบการตั้งค่าเครื่องพิมพ์และสิทธิ์การเข้าถึง")
    else:
        print(f"❌ ระบบปฏิบัติการ {system} ไม่รองรับคำสั่งพิมพ์อัตโนมัติในสคริปต์นี้")
        

def printpdf(
    json_path="output/user_added_slang.json",
    output_path="output/slang_dictionary.pdf",
    thai_font_path="fonts/Kinnari.ttf",
    thai_bold_font_path="fonts/Kinnari-Bold.ttf",
    thai_italic_font_path="fonts/Kinnari-Italic.ttf",
    emoji_font_path="fonts/NotoEmoji-Regular.ttf",
    template_pdf_path="template/Cute Star Border A4 Stationery Paper Document.pdf",
    cover_append_file="template/PP1-4.pdf",  # ไฟล์ PDF ที่จะเพิ่มหน้า
    author=None,
    fortune_json_path="template/th-en_slang_predictions_99.json"
):
    # ในฟังก์ชันถ้า author มีค่า ให้ใช้ค่า author แทน `
    lastauthor = author if author else "ไม่ระบุ"
    
    if not os.path.exists(json_path):
        print(f"❌ printpdf ไม่พบไฟล์ JSON {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    register_fonts(thai_font_path, thai_bold_font_path, thai_italic_font_path, emoji_font_path)

    temp_output = output_path.replace(".pdf", "_temp.pdf")
    intermediate_path = output_path.replace(".pdf", "_plain.pdf")

    for path in [temp_output, intermediate_path, output_path]:
        if os.path.exists(path):
            os.remove(path)

    max_reach = max((entry.get("reach", 1) for entry in data.values()), default=1)

    c = canvas.Canvas(temp_output, pagesize=A4)
    x = margin_left
    y = margin_top
    
    total_meanings = 0
    total_reach = 0
    latest_word = ""
    latest_time = ""
    hottest_word = ""
#    max_reach = 0

    ### Statistic intro
    lastauthor = "ไม่ระบุ"
    top_words = []  # กำหนดตัวแปรก่อน
    authors_set = set()  # เพิ่มบรรทัดนี้ก่อนลูป
    
    for word, info in data.items():
        meanings = info.get("meaning", [])
        if isinstance(meanings, str):
            meanings = [meanings]
        total_meanings += len(meanings)

        reach = info.get("reach", 0)
        total_reach += reach

        top_words.append((word, reach))
        
        author = info.get("author", None)
        if isinstance(author, list):
            authors_set.update(author)
        elif isinstance(author, str):
            authors_set.add(author)

        update_time = info.get("update", "")
        if update_time > latest_time:
            latest_time = update_time
            latest_word = word
            author = info.get("author", "ไม่ระบุ")
            if isinstance(author, list):
                lastauthor = author[-1] if author else "ไม่ระบุ"
            else:
                lastauthor = author

    # อ่านไฟล์คำทำนาย
    fortune_data = {}
    if os.path.exists(fortune_json_path):
        with open(fortune_json_path, "r", encoding="utf-8") as f:
            fortune_data = json.load(f)
    else:
        print(f"❌ ไม่พบไฟล์คำทำนาย {fortune_json_path}")

    top_words = sorted(top_words, key=lambda x: x[1], reverse=True)
    #top5_words = [f" {w} ({r})" for w, r in top_words[:5]]
    #hottest_words_text = " • ".join(top5_words)
    hottest_words_text = [f"{w} ({r})" for w, r in top_words[:5]]
    
    totalauthor = len(authors_set)

    ### Intro page
    draw_intro_page(
        c,
        total_words=len(data),
        total_meanings=total_meanings,
        total_reach=total_reach,
        latest_word=latest_word,
        hottest_word=hottest_words_text,
        y_start=margin_top,
        lastauthor=lastauthor,
        totalauthor=totalauthor
    )
    
    ### Latest word page
    if latest_word in data:
        draw_latest_word_page(c, latest_word, data[latest_word])
        print(f"พบ latest_word: {latest_word}")        
    else:
        print(f"❌ ไม่พบ latest_word: {latest_word}")
        
    ### Content
    draw_title(c, "📚 ปทานุกรมแบบสับ | The Not-So Modern Dictionary ", margin_top)
    y = margin_top - line_space * 2
    
    sorted_words = sorted(data.keys(), key=locale.strxfrm)
    first_char_on_page = None

    for i, word in enumerate(sorted_words):
        info = data[word]

        # ตรวจว่าควรเริ่มหน้าใหม่หรือไม่
        if y < margin_newpage:
            draw_page_number(c)
            c.showPage()
            y = margin_top

            # หาอักษรแรกของคำศัพท์ที่จะใช้แสดงในหัวเรื่อง
            first_char_on_page = get_main_thai_consonant(word)  # ใช้ตัวอักษรแรกของคำนี้
            draw_title(c, f"📚 ปทานุกรมแบบสับ - {first_char_on_page}", y)
            y -= line_space * 2

        # วาดรายการคำศัพท์
        y = draw_entry(c, word, info, x, y, line_space, max_reach)

   
    # วาดหน้าคำทำนาย (เพิ่มหน้าสุดท้าย)
    if fortune_data:
        draw_fortune_page(c, fortune_data)
    #c.save()
    
    draw_page_number(c)
    c.save()
    os.rename(temp_output, intermediate_path)

    # รวม PDF (เพิ่มหน้าจาก cover_append_file เข้าไปใน intermediate_path)
    base_file = intermediate_path            # ไฟล์ที่เพิ่งบันทึกเสร็จ
    output_file = base_file.replace('.pdf', '_complete.pdf')

    merge_pdfs(cover_append_file, base_file, output_file)
    print(f"Created merged PDF: {output_file}")

    # ถ้ามี template PDF ใช้ทำพื้นหลังบนไฟล์ output_file (ที่รวมหน้าแล้ว)
    if os.path.exists(template_pdf_path):
        add_template_background(template_pdf_path, output_file, output_path)
    else:
        os.rename(output_file, output_path)

    # สร้าง booklet จากไฟล์ output_path (ไฟล์สุดท้ายที่มีพื้นหลังแล้วหรือไฟล์ merged)
    output_booklet = output_path.replace(".pdf", "_booklet.pdf")
    print(f"Input PDF: {output_path}")
    make_foldable_booklet(input_path=output_path, output_path=output_booklet)
    
    ### พิมพ์ออกมา
    print_pdf_file(output_booklet)