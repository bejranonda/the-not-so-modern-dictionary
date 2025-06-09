import json
import os
import platform
import subprocess
import fitz # PyMuPDF
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

# New constants for columns
column_gap = 30  # Space between columns
column_width = (usable_width - column_gap) / 2
column1_x = margin_left
column2_x = margin_left + column_width + column_gap

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
    """Register custom fonts with ReportLab."""
    pdfmetrics.registerFont(TTFont("Kinnari", thai_font_path))
    pdfmetrics.registerFont(TTFont("Kinnari-Bold", thai_bold_font_path))
    pdfmetrics.registerFont(TTFont("Kinnari-Italic", thai_italic_font_path))
    pdfmetrics.registerFont(TTFont("EmojiFont", emoji_font_path))

def draw_title(c, text, y):
    """Draw a centered title with mixed text (Thai and Emoji)."""
    draw_mixed_text_centered(c, text, width / 2, y, "Kinnari-Bold", title_font_size*0.8, "EmojiFont", title_font_size*0.8)

def get_star_rating(reach, max_reach):
    """Calculate star rating based on reach."""
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
    """Draw the introduction page with statistics."""
    updated_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    text_lines = [
            f"🏢 สำนักพิมพ์ | Publisher : ยุงลาย - Yunglai",
            f"🖨 พิมพ์ที่ | Printed at : Bangkok Kunsthalle",
            f"🔢 พิมพ์ครั้งที่ | Print Count : {total_reach:,}",
            f"📅 ปรับปรุงล่าสุด | Last Updated : {updated_date}",
            f"🧾 คำศัพท์ทั้งหมด | Total Words : {total_words:,}",
            f"🆕 คำล่าสุด | Latest Word : {latest_word}",
            f"📝 จำนวนผู้แต่ง | Total Authors : {totalauthor}",
            f"📝 ผู้แต่งล่าสุด | Latest Author : {lastauthor}",
            f"📚 คลังตัวอย่าง | Example Data : {total_meanings:,} sets",
            f"🔥 คำฮิต | Hottest Words :", # Label for the hottest words list
        ]

    draw_title(c, "📖 ปทานุกรมแบบสับ - The Not-So Modern Dictionary 📖", y_start)
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
            c, f"    • {line}", margin_left, y,
            "Kinnari", content_font_size*1.3, "EmojiFont", content_font_size*1.2)
        y -= line_space*1

    draw_page_number(c)
    c.showPage()

def draw_fortune_page(c, fortune_data):
    """Draw the fortune telling page with a random word and its prediction."""
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


    
def draw_entry(c, word, info, x, y, line_height, max_reach, column_width, indent=10): # Added column_width
    """Draw a dictionary entry (word, meaning, example, reach) within a specified column width."""
    reach = info.get("reach", 1)
    stars = get_star_rating(reach, max_reach)
    
    entry_fontsize_factor = 0.7 #factor to reduce or increase font size in word entry

    # Header + stars
    # Pass column_width to draw_mixed_text_wrapped
    y, _ = draw_mixed_text_wrapped(
        c, f" {word}{stars}", x, y,
        "Kinnari-Bold", header_font_size * entry_fontsize_factor, "EmojiFont", round(header_font_size * 0.7 * entry_fontsize_factor), line_height, max_text_width=column_width)
    y -= line_height * 0.2 * entry_fontsize_factor

    # Meanings
    meanings = info.get("meaning", [])
    if isinstance(meanings, str):
        meanings = [meanings]
    for m in meanings:
        # No new page check here, as it's handled in the main loop
        y, _ = draw_mixed_text_wrapped(
            c, f"📝 {m}", x + indent, y,
            "Kinnari", content_font_size * entry_fontsize_factor, "EmojiFont", (content_font_size - 2) * entry_fontsize_factor, line_height, max_text_width=column_width - indent)
        y -= line_height * 0.2 * entry_fontsize_factor

    # Examples
    examples = info.get("example", [])
    if isinstance(examples, str):
        examples = [examples]
    for ex in examples:
        # No new page check here, as it's handled in the main loop
        y, _ = draw_mixed_text_wrapped(
            c, f"💬 {ex}", x + indent, y,
            "Kinnari", content_font_size * entry_fontsize_factor, "EmojiFont", (content_font_size - 2) * entry_fontsize_factor, line_height, max_text_width=column_width - indent)
        y -= line_height * 0.2 * entry_fontsize_factor

    # Reach number
    y += line_height * 0.3
    y, _ = draw_mixed_text_wrapped(
        c, f" 📈 {reach}", x + indent, y, # Add English for consistency
        "Kinnari", round(content_font_size*0.9 * entry_fontsize_factor), "EmojiFont", round(content_font_size*0.8 * entry_fontsize_factor), round(line_height * 0.8), max_text_width=column_width - indent)

    y -= line_height * 2 * entry_fontsize_factor
    return y


def draw_latest_word_page(c, word, info):
    """Draw a page dedicated to the latest added word."""
    y = margin_top
    draw_title(c, "The Not-So Modern Dictionary 🤩 A New Entry", y)
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
    c, f"📝 ความหมาย | Meaning", margin_left, y, # Translated label
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
        y -= line_space*0.9
    y -= line_space
    
    # Samples
    examples = info.get("example", [])
    if isinstance(examples, str):
        examples = [examples]
    examples = examples[-4:]  # แสดง 4 ชุดล่าสุด
    
    y, _ = draw_mixed_text_wrapped(
    c, f"💬 ตัวอย่าง | Examples", margin_left, y, # Translated label
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
        y -= line_space*0.9

    # Add latest author if available
    author_list = info.get("author")
    if isinstance(author_list, list) and author_list:
        author = author_list[-1]  # last one in the list
    elif isinstance(author_list, str):
        author = author_list
    else:
        author = None

    if author:
        y -= line_space * 1.5
        y, _ = draw_mixed_text_wrapped(
            c, f"📝 ผู้แต่งล่าสุด | Latest Author: {author}", margin_left, y, # Translated label
            "Kinnari", content_font_size * 2,
            "EmojiFont", content_font_size * 2,
            line_space * 1.5)

    draw_page_number(c)
    c.showPage()


def draw_mixed_text(c, text, x, y, font1, size1, font2, size2):
    """Draw text character by character, switching fonts for emojis."""
    current_x = x
    for ch in text:
        if ord(ch) > 0x1F000 or ord(ch) == 0x2B50: # Check for common emoji ranges and specific star emoji
            c.setFont(font2, size2)
        else:
            c.setFont(font1, size1)
        c.drawString(current_x, y, ch)
        current_x += stringWidth(ch, c._fontname, c._fontsize)

def draw_mixed_text_centered(c, text, center_x, y, font1, size1, font2, size2):
    """Draw mixed text centered horizontally."""
    total_width = sum(stringWidth(ch, font2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else font1, size2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else size1) for ch in text)
    start_x = center_x - total_width / 2
    draw_mixed_text(c, text, start_x, y, font1, size1, font2, size2)

def draw_mixed_text_wrapped(c, text, x, y, font1, size1, font2, size2, line_height=line_space, max_text_width=None):
    """Draw mixed text, wrapping it to fit within a specified maximum width."""
    if max_text_width is None:
        # Default to usable_width for non-column drawing (e.g., full-width titles)
        max_text_width = usable_width - (x - margin_left)
    
    lines = []
    current_line = ''
    current_width = 0
    for ch in text:
        font = font2 if ord(ch) > 0x1F000 or ord(ch) == 0x2B50 else font1
        size = size2 if ord(ch) > 0x1F000 or ord(ch) == 0x2B50 else size1
        ch_width = stringWidth(ch, font, size)
        if current_width + ch_width > max_text_width: # Use max_text_width here
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
    """Draw the current page number at the bottom center of the page."""
    page_num = c.getPageNumber()
    text = f"- {page_num} -"
    font_size = 12
    text_width = stringWidth(text, "Kinnari", font_size)
    x = (width - text_width) / 2
    y = 25
    c.setFont("Kinnari", font_size)
    c.drawString(x, y, text)

def add_template_background(template_path, input_pdf_path, output_pdf_path):
    """Add a background template to specific pages of a PDF."""
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
    """Rearrange pages of a PDF to create a foldable booklet layout."""
    doc = fitz.open(input_path)
    total_pages = len(doc)
    w, h = 842, 595 # A4 landscape dimensions for 2-up printing
    
    # Pad with blank pages if total_pages is less than 8 for booklet format
    if total_pages < 8:
        print(f"PDF total_pages: {total_pages}, padding to 8 pages for booklet.")
        for _ in range(8 - total_pages):
            doc.new_page(width=w, height=h)
    
    # Recalculate total_pages after padding
    total_pages = len(doc)

    # Simplified page order for testing 8 pages (adjust for actual booklet pagination)
    # This is a fixed order for 8 pages on a single A4 landscape sheet.
    # For a general booklet, you'd calculate pages for each sheet.
    # Example for an 8-page booklet (2 sheets, 4 pages per sheet):
    # Sheet 1: Page 7, Page 0, Page 1, Page 6 (front side of paper)
    # Sheet 2: Page 5, Page 2, Page 3, Page 4 (back side of paper)
    # The current implementation below is for a single sheet with 8 logical "sections".
    
    # This page_order determines which original page goes into which "section" of the output page.
    # It might need adjustment based on the exact folding method.
    # The random page for index 6 might not be desired for actual booklets.
    # For a standard 8-page booklet printed on one A4 sheet (landscape, folded in half then quarters):
    # Sheet side 1 (top half): [Page 7 (back cover), Page 0 (front cover)]
    # Sheet side 2 (bottom half): [Page 1, Page 6] (inside of the paper, reversed)
    # The current code puts 8 'sections' on one page. This is for a single large sheet.
    # To create a standard booklet (e.g., A4 landscape folded into A6 booklet), you'd need to
    # combine 4 pages onto one side of an A4 sheet, and 4 more on the other side.
    
    # For simplicity and to match the existing user code's intent of placing multiple pages on one sheet:
    # We will arrange 8 virtual "sections" on one output A4 page.
    # This assumes the user wants all 8 logical "pages" to be visible on one physical A4 sheet.
    
    # The original page_order has a random element, which is unusual for a standard booklet.
    # Keeping it as is, but noting this for future improvements.
    page_order = [0, 1, 2, 3, 4, 5, random.randint(6, total_pages - 1) if total_pages > 6 else 6, total_pages - 1 if total_pages > 0 else 0]
    
    # Create a new document for the booklet output
    output_doc = fitz.open()
    new_page = output_doc.new_page(width=w, height=h) # A4 landscape size

    section_w, section_h = w / 4, h / 2 # Divide A4 landscape into 2 rows, 4 columns
    
    for i, idx in enumerate(page_order):
        if idx >= len(doc):
            continue # Skip if index is out of bounds for the original document
        
        src_page = doc.load_page(idx)
        
        col, row = i % 4, 0 if i < 4 else 1 # Determine column and row for each section
        x0, y0 = col * section_w, row * section_h
        target_rect = fitz.Rect(x0, y0, x0 + section_w, y0 + section_h)
        
        # Rotate the first 4 "sections" (logical pages) by 180 degrees
        rotation = 180 if i < 4 else 0
        new_page.show_pdf_page(target_rect, doc, idx, rotate=rotation)
        
    output_doc.save(output_path)
    doc.close()
    output_doc.close()


def merge_pdfs(append_pdf_path, base_pdf_path, output_pdf_path):
    """Merge two PDF files, appending one to the beginning of another."""
    writer = PdfWriter()

    # Add pages from the append_pdf first
    append_pdf = PdfReader(append_pdf_path)
    for page in append_pdf.pages:
        writer.add_page(page)

    # Then add pages from the base_pdf
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
    # Ensure the path uses forward slashes for consistency in PowerShell arguments
    # and to avoid issues with backslashes needing escaping.
    abs_pdf_path = os.path.abspath(pdf_path).replace("\\", "/")

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
            # Use 'Start-Process' with double quotes around file path for spaces and to handle forward slashes
            # Using os.path.normpath to ensure correct path formatting for Windows native commands
            # and then replacing backslashes with forward slashes for PowerShell compatibility.
            quoted_abs_pdf_path = f'"{os.path.normpath(abs_pdf_path)}"'
            cmd = f'PowerShell.exe -Command "Start-Process -FilePath {quoted_abs_pdf_path} -Verb PrintTo -ArgumentList \'{printer_name}\'"'
            print(f"คำสั่ง Windows (PowerShell - PrintTo): {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW) # Use CREATE_NO_WINDOW for silent process
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
            # Common paths for Adobe Reader and SumatraPDF
            program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
            program_files = os.environ.get("ProgramFiles", r"C:\Program Files")

            adobe_reader_paths = [
                os.path.join(program_files_x86, r"Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
                os.path.join(program_files, r"Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
                os.path.join(program_files_x86, r"Adobe\Reader 11.0\Reader\AcroRd32.exe"), # Older version
                os.path.join(program_files, r"Adobe\Reader 11.0\Reader\AcroRd32.exe")    # Older version
            ]
            sumatra_paths = [
                os.path.join(program_files, r"SumatraPDF\SumatraPDF.exe"),
                os.path.join(program_files_x86, r"SumatraPDF\SumatraPDF.exe")
            ]

            # Try Adobe Reader
            for adobe_path in adobe_reader_paths:
                if os.path.exists(adobe_path):
                    # Quote paths for command line using os.path.normpath for consistency
                    cmd = [f'"{os.path.normpath(adobe_path)}"', "/N", "/T", f'"{os.path.normpath(abs_pdf_path)}"', printer_name]
                    print(f"คำสั่ง Windows (Adobe Reader): {' '.join(cmd)}")
                    try:
                        subprocess.run(" ".join(cmd), shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน Adobe Reader)")
                        printed_successfully = True
                        break
                    except Exception as e:
                        print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (Adobe Reader): {e}")
                        continue
            
            if not printed_successfully:
                # Try SumatraPDF
                for sumatra_path in sumatra_paths:
                    if os.path.exists(sumatra_path):
                        # Quote paths for command line using os.path.normpath for consistency
                        cmd = [f'"{os.path.normpath(sumatra_path)}"', "-print-to", printer_name, f'"{os.path.normpath(abs_pdf_path)}"', "-silent"] # Added -silent
                        print(f"คำสั่ง Windows (SumatraPDF): {' '.join(cmd)}")
                        try:
                            subprocess.run(" ".join(cmd), shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
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
                # Ensure the path is quoted for os.startfile as well
                os.startfile(os.path.normpath(abs_pdf_path), "print") # os.startfile generally handles paths correctly without manual quoting, but normpath helps.
                print("✅ คำสั่งเปิดกล่องโต้ตอบการพิมพ์ถูกส่งแล้ว")
            except Exception as e:
                print(f"❌ ข้อผิดพลาดในการเปิดกล่องโต้ตอบการพิมพ์: {e}")
                print("   โปรดตรวจสอบการตั้งค่าโปรแกรมดู PDF เริ่มต้นและสิทธิ์การเข้าถึง")
                print("   หากปัญหายังคงอยู่: โปรดติดตั้งโปรแกรมดู PDF เช่น Adobe Reader หรือ SumatraPDF และตั้งค่าให้เป็นโปรแกรมเริ่มต้นสำหรับไฟล์ PDF")
                print("   หากปัญหายังคงอยู่: อาจจำเป็นต้องแก้ไขการเชื่อมโยงชนิดไฟล์ด้วยตนเองใน Windows หรือเรียกใช้สคริปต์ในฐานะผู้ดูแลระบบ")

    elif system == "Darwin" or system == "Linux": # Darwin คือ macOS
        try:
            # ใช้คำสั่ง lpr บน Linux/macOS (ระบบ CUPS)
            cmd = ["lpr"]
            if printer_name:
                cmd.extend(["-P", printer_name])
            cmd.append(abs_pdf_path) # lpr handles paths with spaces well
            
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
            try:
                os.remove(path)
                print(f"Removed old file: {path}")
            except OSError as e:
                print(f"Error removing file {path}: {e}")

    max_reach = max((entry.get("reach", 1) for entry in data.values()), default=1)

    c = canvas.Canvas(temp_output, pagesize=A4)
    
    total_meanings = 0
    total_reach = 0
    latest_word = ""
    latest_time = ""
    
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
            author_info = info.get("author", "ไม่ระบุ")
            if isinstance(author_info, list):
                lastauthor = author_info[-1] if author_info else "ไม่ระบุ"
            else:
                lastauthor = author_info

    # อ่านไฟล์คำทำนาย
    fortune_data = {}
    if os.path.exists(fortune_json_path):
        with open(fortune_json_path, "r", encoding="utf-8") as f:
            fortune_data = json.load(f)
    else:
        print(f"❌ ไม่พบไฟล์คำทำนาย {fortune_json_path}")

    top_words = sorted(top_words, key=lambda x: x[1], reverse=True)
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
        
    ### Content with 2 columns
    # Initial Y positions for left and right columns
    y_left_col = margin_top - line_space * 2
    y_right_col = margin_top - line_space * 2
    
    # Sort words for alphabetical order (assuming Thai collation is handled by locale)
    sorted_words = sorted(data.keys(), key=locale.strxfrm)
    
    # Draw the initial dictionary title for the content section
    first_char_on_page = get_main_thai_consonant(sorted_words[0])
    draw_title(c, f"The Not-So Modern Dictionary 📚 {first_char_on_page}", margin_top)
    c.setFont("Kinnari", content_font_size) # Set default font for content text
    
    # Reset column Y positions after title is drawn (already set above, but confirm)
    y_left_col = margin_top - line_space * 2
    y_right_col = margin_top - line_space * 2

    # Iterate through sorted words and place them in columns
    for i, word in enumerate(sorted_words):
        info = data[word]
        
        # Estimate height for the current entry (rough estimate for decision making)
        # 1 line for word, 1 for each meaning, 1 for each example, 1 for reach + some padding
        # This is a critical estimation for column layout. Adjust factor (1.5) if entries get cut off.
        estimated_entry_lines = 1 + len(info.get("meaning", [])) + len(info.get("example", [])) + 1
        estimated_entry_height = estimated_entry_lines * line_space * 1.5 

        target_x = None
        current_y_for_entry = None
        should_start_new_page = False

        # Decide which column to put the current entry into
        if y_left_col <= y_right_col: # Prefer left column if it's currently "shorter" or equal
            if y_left_col - estimated_entry_height < margin_bottom: # Left column would overflow
                if y_right_col - estimated_entry_height < margin_bottom: # Right column also would overflow -> new page
                    should_start_new_page = True
                else: # Left overflows, but right has space on current page
                    target_x = column2_x
                    current_y_for_entry = y_right_col
            else: # Left column has space
                target_x = column1_x
                current_y_for_entry = y_left_col
        else: # Prefer right column (y_right_col is shorter)
            if y_right_col - estimated_entry_height < margin_bottom: # Right column would overflow -> new page
                should_start_new_page = True
            else: # Right column has space
                target_x = column2_x
                current_y_for_entry = y_right_col

        # Handle new page if decided
        if should_start_new_page:
            draw_page_number(c) # Draw page number for current page before moving on
            c.showPage() # Start new page
            y_left_col = margin_top - line_space * 2 # Reset Y for new page
            y_right_col = margin_top - line_space * 2
            
            # For a new page, always start in the left column
            target_x = column1_x
            current_y_for_entry = y_left_col
            
            # Draw new page title
            first_char_on_page = get_main_thai_consonant(word)
            draw_title(c, f"The Not-So Modern Dictionary 📚 {first_char_on_page}", margin_top)
            c.setFont("Kinnari", content_font_size) # Reset default font for content text

        # Draw the entry at the determined (target_x, current_y_for_entry)
        new_y_after_drawing = draw_entry(c, word, info, target_x, current_y_for_entry, line_space, max_reach, column_width)
        
        # Update the y-coordinate for the column that was just filled
        if target_x == column1_x:
            y_left_col = new_y_after_drawing
        else: # target_x == column2_x
            y_right_col = new_y_after_drawing

    # After iterating through all words, draw the page number on the last page of content
    # This also ensures content is flushed before next sections.
    draw_page_number(c)
    #c.showPage() 
    
    # วาดหน้าคำทำนาย (เพิ่มหน้าสุดท้าย)
    if fortune_data:
        draw_fortune_page(c, fortune_data)
        
    draw_page_number(c)
    c.save()
    os.rename(temp_output, intermediate_path)

    # รวม PDF (เพิ่มหน้าจาก cover_append_file เข้าไปใน intermediate_path)
    base_file = intermediate_path      # ไฟล์ที่เพิ่งบันทึกเสร็จ
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
    #print_pdf_file(output_booklet, "Brother MFC-J5320DW Printer")
