# slang_pdf_generator.py

import json
import os
import fitz  # PyMuPDF
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

# 📐 Global constants
width, height = A4
margin_left = 50
margin_right = margin_left
margin_top = height - 80
margin_bottom = 70
margin_newpage = 100
line_space = 20
usable_width = width - margin_left - margin_right

title_font_size = 28
header_font_size = 25
content_font_size = 20

def register_fonts(thai_font_path, thai_bold_font_path, emoji_font_path):
    pdfmetrics.registerFont(TTFont("THSarabun", thai_font_path))
    pdfmetrics.registerFont(TTFont("THSarabun-Bold", thai_bold_font_path))
    pdfmetrics.registerFont(TTFont("EmojiFont", emoji_font_path))

def draw_title(c, text, y):
    draw_mixed_text_centered(c, text, width / 2, y, "THSarabun", title_font_size, "EmojiFont", title_font_size)

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
       

def draw_intro_page(c, total_words, y_start):
    updated_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    text1 = f"📅 ปรับปรุงล่าสุด: {updated_date}"
    text2 = f"🧾 จำนวนคำศัพท์ทั้งหมด: {total_words:,} คำ"

    draw_title(c, "📖 รายละเอียดพจนานุกรม", y_start)
    y = y_start - line_space * 3

    y, _ = draw_mixed_text_wrapped(
        c, text1, margin_left, y,
        "THSarabun", content_font_size, "EmojiFont", content_font_size - 2)

    y -= line_space
    y, _ = draw_mixed_text_wrapped(
        c, text2, margin_left, y,
        "THSarabun", content_font_size, "EmojiFont", content_font_size - 2)

    draw_page_number(c)
    c.showPage()


def draw_entry(c, word, info, x, y, line_height, max_reach, indent=10):
    reach = info.get("reach", 1)
    stars = get_star_rating(reach, max_reach)

    # Header + stars
    y, _ = draw_mixed_text_wrapped(
        c, f"  {word}{stars}", x, y,
        "THSarabun-Bold", header_font_size, "EmojiFont", header_font_size - 15, line_height)
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
            draw_title(c, "📚 พจนานุกรมคำสแลงไทย", y)
            y -= line_height * 2

        y, _ = draw_mixed_text_wrapped(
            c, f"📝 {m}", x + indent, y,
            "THSarabun", content_font_size, "EmojiFont", content_font_size - 2, line_height)
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
            draw_title(c, "📚 พจนานุกรมคำสแลงไทย", y)
            y -= line_height * 2

        y, _ = draw_mixed_text_wrapped(
            c, f"💬 {ex}", x + indent, y,
            "THSarabun", content_font_size, "EmojiFont", content_font_size - 2, line_height)
        y -= line_height * 0.2

    # Reach number
    y += line_height * 0.5
    y, _ = draw_mixed_text_wrapped(
        c, f"📈 {reach}", x + indent, y,
        "THSarabun", content_font_size - 8, "EmojiFont", content_font_size - 12, line_height * 0.5)

    y -= line_height * 2
    return y

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
    font_size = 14
    text_width = stringWidth(text, "THSarabun", font_size)
    x = (width - text_width) / 2
    y = 25
    c.setFont("THSarabun", font_size)
    c.drawString(x, y, text)

def add_template_background(template_path, input_pdf_path, output_pdf_path):
    template_doc = fitz.open(template_path)
    input_doc = fitz.open(input_pdf_path)
    template_page = template_doc.load_page(0)
    bg_pix = template_page.get_pixmap(alpha=False)
    bg_img_rect = template_page.rect
    for page_num in range(len(input_doc)):
        page = input_doc.load_page(page_num)
        page.insert_image(bg_img_rect, pixmap=bg_pix, overlay=False)
    input_doc.save(output_pdf_path)

def make_foldable_booklet(input_path, output_path):
    doc = fitz.open(input_path)
    total_pages = len(doc)
    w, h = 842, 595
    if total_pages < 8:
        for _ in range(8 - total_pages):
            doc.new_page(width=w, height=h)
    section_w, section_h = w / 4, h / 2
    page_order = [7, 0, 1, 6, 5, 2, 3, 4]
    output_doc = fitz.open()
    new_page = output_doc.new_page(width=w, height=h)
    for i, idx in enumerate(page_order):
        if idx >= len(doc): continue
        src_page = doc.load_page(idx)
        text = src_page.get_text("text").strip()
        if not text: continue
        col, row = i % 4, 0 if i < 4 else 1
        x0, y0 = col * section_w, row * section_h
        target_rect = fitz.Rect(x0, y0, x0 + section_w, y0 + section_h)
        new_page.show_pdf_page(target_rect, doc, idx)
    output_doc.save(output_path)

def printpdf(
    json_path="user_added_slang.json",
    output_path="output/slang_dictionary.pdf",
    thai_font_path="fonts/THSarabunNew.ttf",
    thai_bold_font_path="fonts/THSarabunNew Bold.ttf",
    emoji_font_path="fonts/NotoEmoji-Regular.ttf",
    template_pdf_path="template/Cute Star Border A4 Stationery Paper Document.pdf"
):
    if not os.path.exists(json_path):
        print(f"❌ ไม่พบไฟล์ {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    register_fonts(thai_font_path, thai_bold_font_path, emoji_font_path)

    temp_output = output_path.replace(".pdf", "_temp.pdf")
    intermediate_path = output_path.replace(".pdf", "_plain.pdf")

    for path in [temp_output, intermediate_path, output_path]:
        if os.path.exists(path):
            os.remove(path)

    max_reach = max((entry.get("reach", 1) for entry in data.values()), default=1)

    c = canvas.Canvas(temp_output, pagesize=A4)
    x = margin_left
    y = margin_top

    draw_intro_page(c, total_words=len(data), y_start=margin_top)
    draw_title(c, "📚 พจนานุกรมคำสแลงไทย | Thai Slang Dictionary", margin_top)
    y = margin_top - line_space * 2

    for word, info in data.items():
        if y < margin_newpage:
            draw_page_number(c)
            c.showPage()
            y = margin_top
            draw_title(c, "📚 พจนานุกรมคำสแลงไทย", y)
            y -= line_space * 2
        y = draw_entry(c, word, info, x, y, line_space, max_reach)

    draw_page_number(c)
    c.save()
    os.rename(temp_output, intermediate_path)

    if os.path.exists(template_pdf_path):
        add_template_background(template_pdf_path, intermediate_path, output_path)
    else:
        os.rename(intermediate_path, output_path)

    output_booklet = output_path.replace(".pdf", "_booklet.pdf")
    make_foldable_booklet(input_path=output_path, output_path=output_booklet)
