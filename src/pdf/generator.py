"""
PDF generation module for The Not-So-Modern Dictionary.

This module handles the creation of personalized dictionary booklets with:
- ReportLab-based PDF generation with Thai and emoji font support
- Two-column layout with alphabetical sorting
- Template PDF backgrounds using PyMuPDF
- Booklet folding layout for physical printing
- Easter egg support (jackpot pages, system hacked)
- Fortune-telling pages
- Statistics and latest word pages
"""

import json
import os
import sys
import locale
import random
import platform
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Third-party imports
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from PyPDF2 import PdfReader, PdfWriter
import re

# Local imports
from ..config.settings import (
    AppMode, FONTS_DIR, TEMPLATE_DIR, OUTPUT_DIR, BASE_DIR
)
from ..core.database import SlangDatabase
from ..core.easter_eggs import EasterEggManager
from ..utils.logger import app_logger


class PDFGenerator:
    """Generates personalized dictionary PDFs with various features."""

    def __init__(self, mode: str = AppMode.NORMAL):
        """
        Initialize PDF generator.

        Args:
            mode: Application mode (NORMAL or LAST_WEEK)
        """
        self.mode = mode
        self.db = SlangDatabase()
        self.easter_egg_manager = EasterEggManager()

        # PDF Layout Constants
        self.width, self.height = A4
        self.margin_left = 50
        self.margin_right = self.margin_left
        self.margin_top = self.height - 80
        self.margin_bottom = 60
        self.line_space = 20
        self.usable_width = self.width - self.margin_left - self.margin_right

        # Font sizes
        self.title_font_size = 20
        self.header_font_size = 17
        self.content_font_size = 14

        # Column layout
        self.column_gap = 30
        self.column_width = (self.usable_width - self.column_gap) / 2
        self.column1_x = self.margin_left
        self.column2_x = self.margin_left + self.column_width + self.column_gap

        # Font paths
        self.thai_font_path = str(FONTS_DIR / "Kinnari.ttf")
        self.thai_bold_font_path = str(FONTS_DIR / "Kinnari-Bold.ttf")
        self.thai_italic_font_path = str(FONTS_DIR / "Kinnari-Italic.ttf")
        self.emoji_font_path = str(FONTS_DIR / "NotoEmoji-Regular.ttf")
        self.ln_font_path = str(FONTS_DIR / "NotoSansKhmer-Regular.ttf")

        # Template paths
        self.template_pdf_path1 = str(TEMPLATE_DIR / "pp1.pdf")
        self.template_pdf_path2 = str(TEMPLATE_DIR / "pp2.pdf")
        self.template_pdf_path3 = str(TEMPLATE_DIR / "pp3.pdf")
        self.template_pdf_path4 = str(TEMPLATE_DIR / "pp4.pdf")
        self.cover_append_file = str(TEMPLATE_DIR / "PP1-4.pdf")

        # Fortune JSON path based on mode
        if mode == AppMode.LAST_WEEK:
            self.fortune_json_path = str(TEMPLATE_DIR / "th-en-ln_slang_predictions_lastweek.json")
        else:
            self.fortune_json_path = str(TEMPLATE_DIR / "th-en-ln_slang_predictions_99.json")

        # Output paths
        self.output_path = str(OUTPUT_DIR / "slang_dictionary.pdf")

        # Printer settings
        self.printer_active = True

        # Setup locale for Thai sorting
        self._setup_locale()

        app_logger.info(f"PDFGenerator initialized in {mode} mode")

    def _setup_locale(self) -> None:
        """Setup locale for proper Thai text collation."""
        try:
            locale.setlocale(locale.LC_COLLATE, 'th_TH.UTF-8')
            app_logger.info("Locale for collation set to 'th_TH.UTF-8'")
        except locale.Error:
            app_logger.warning("'th_TH.UTF-8' locale not supported, trying fallback")
            try:
                locale.setlocale(locale.LC_COLLATE, 'en_US.UTF-8')
                app_logger.info("Locale for collation set to 'en_US.UTF-8' as fallback")
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_COLLATE, 'C')
                    app_logger.info("Locale for collation set to 'C' as final fallback")
                except locale.Error:
                    app_logger.error("Could not set any locale for LC_COLLATE")

    def register_fonts(self) -> None:
        """Register custom fonts with ReportLab."""
        try:
            pdfmetrics.registerFont(TTFont("Kinnari", self.thai_font_path))
            pdfmetrics.registerFont(TTFont("Kinnari-Bold", self.thai_bold_font_path))
            pdfmetrics.registerFont(TTFont("Kinnari-Italic", self.thai_italic_font_path))
            pdfmetrics.registerFont(TTFont("EmojiFont", self.emoji_font_path))
            pdfmetrics.registerFont(TTFont("LN", self.ln_font_path))
            app_logger.info("Fonts registered successfully")
        except Exception as e:
            app_logger.error(f"Error registering fonts: {e}")
            raise

    @staticmethod
    def get_main_thai_consonant(word: str) -> str:
        """
        Return the first Thai consonant character from the word.
        Skips Thai vowels like เ, แ, โ, ใ, ไ which are leading vowels.

        Args:
            word: Thai word

        Returns:
            First consonant or first character
        """
        match = re.search(r'[\u0E01-\u0E2E]', word)
        if match:
            return match.group(0)
        return word[0] if word else ''

    def get_star_rating(self, reach: int, max_reach: int) -> str:
        """
        Calculate star rating based on reach.

        Args:
            reach: Current reach count
            max_reach: Maximum reach in database

        Returns:
            Star rating string
        """
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

    def draw_mixed_text(self, c: canvas.Canvas, text: str, x: float, y: float,
                       font1: str, size1: float, font2: str, size2: float) -> None:
        """Draw text character by character, switching fonts for emojis."""
        current_x = x
        for ch in text:
            if ord(ch) > 0x1F000 or ord(ch) == 0x2B50:
                c.setFont(font2, size2)
            else:
                c.setFont(font1, size1)
            c.drawString(current_x, y, ch)
            current_x += stringWidth(ch, c._fontname, c._fontsize)

    def draw_mixed_text_centered(self, c: canvas.Canvas, text: str, center_x: float,
                                 y: float, font1: str, size1: float, font2: str,
                                 size2: float) -> None:
        """Draw mixed text centered horizontally."""
        total_width = sum(
            stringWidth(ch, font2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else font1,
                       size2 if ord(ch) >= 0x1F000 or ord(ch) == 0x2B50 else size1)
            for ch in text
        )
        start_x = center_x - total_width / 2
        self.draw_mixed_text(c, text, start_x, y, font1, size1, font2, size2)

    def draw_mixed_text_wrapped(self, c: canvas.Canvas, text: str, x: float, y: float,
                               font1: str, size1: float, font2: str, size2: float,
                               line_height: float = None, max_text_width: float = None,
                               dry_run: bool = False) -> Tuple[float, int]:
        """
        Draw mixed text, wrapping it to fit within a specified maximum width.

        Args:
            c: Canvas object
            text: Text to draw
            x, y: Starting position
            font1, size1: Primary font and size
            font2, size2: Emoji font and size
            line_height: Height of each line
            max_text_width: Maximum width before wrapping
            dry_run: If True, calculates height without drawing

        Returns:
            Tuple of (new_y_position, line_count)
        """
        if line_height is None:
            line_height = self.line_space
        if max_text_width is None:
            max_text_width = self.usable_width - (x - self.margin_left)

        lines_count = 0
        current_line = ''
        current_width = 0
        start_y_for_dry_run = y

        for ch in text:
            font = font2 if ord(ch) > 0x1F000 or ord(ch) == 0x2B50 else font1
            size = size2 if ord(ch) > 0x1F000 or ord(ch) == 0x2B50 else size1
            ch_width = stringWidth(ch, font, size)

            if current_width + ch_width > max_text_width:
                lines_count += 1
                if not dry_run:
                    self.draw_mixed_text(c, current_line, x, y, font1, size1, font2, size2)
                    y -= line_height
                current_line = ch
                current_width = ch_width
            else:
                current_line += ch
                current_width += ch_width

        if current_line:
            lines_count += 1
            if not dry_run:
                self.draw_mixed_text(c, current_line, x, y, font1, size1, font2, size2)
                y -= line_height

        if dry_run:
            return start_y_for_dry_run - (lines_count * line_height), lines_count
        else:
            return y, lines_count

    def draw_mixed_text_wrapped_centered(self, c: canvas.Canvas, text: str,
                                        center_x: float, y: float, font1: str,
                                        size1: float, font2: str, size2: float,
                                        line_height: float, max_text_width: float = None,
                                        dry_run: bool = False) -> Tuple[float, int]:
        """
        Draws mixed text, wrapping and centering each line horizontally.

        Args:
            c: Canvas object
            text: Text to draw
            center_x: Center X position
            y: Starting Y position
            font1, size1: Primary font and size
            font2, size2: Emoji font and size
            line_height: Height of each line
            max_text_width: Maximum width before wrapping
            dry_run: If True, calculates height without drawing

        Returns:
            Tuple of (new_y_position, line_count)
        """
        if max_text_width is None:
            max_text_width = self.usable_width

        lines_data = []
        current_line = ''
        current_width = 0

        for ch in text:
            font = font2 if (ord(ch) > 0x1F000 and ord(ch) < 0x1F9FF) or ord(ch) == 0x2B50 else font1
            size = size2 if (ord(ch) > 0x1F000 and ord(ch) < 0x1F9FF) or ord(ch) == 0x2B50 else size1
            ch_width = stringWidth(ch, font, size)

            if current_width + ch_width > max_text_width:
                lines_data.append({'text': current_line, 'width': current_width})
                current_line = ch
                current_width = ch_width
            else:
                current_line += ch
                current_width += ch_width

        if current_line:
            lines_data.append({'text': current_line, 'width': current_width})

        start_y_for_dry_run = y
        lines_count = len(lines_data)

        if not dry_run:
            for line_info in lines_data:
                line_text = line_info['text']
                line_actual_width = line_info['width']
                centered_x = center_x - (line_actual_width / 2.0)
                self.draw_mixed_text(c, line_text, centered_x, y, font1, size1, font2, size2)
                y -= line_height
        else:
            y = start_y_for_dry_run - (lines_count * line_height)

        return y, lines_count

    def draw_title(self, c: canvas.Canvas, text: str, y: float) -> None:
        """Draw a centered title with mixed text (Thai and Emoji)."""
        self.draw_mixed_text_centered(c, text, self.width / 2, y, "Kinnari-Bold",
                                     self.title_font_size * 0.8, "EmojiFont",
                                     self.title_font_size * 0.8)

    def draw_page_number(self, c: canvas.Canvas) -> None:
        """Draw the current page number at the bottom center of the page."""
        page_num = c.getPageNumber()
        text = f"- {page_num} -"
        font_size = 12
        text_width = stringWidth(text, "Kinnari", font_size)
        x = (self.width - text_width) / 2
        y = 25
        c.setFont("Kinnari", font_size)
        c.drawString(x, y, text)

    def draw_intro_page(self, c: canvas.Canvas, total_words: int, total_meanings: int,
                       total_reach: int, latest_word: str, hottest_word: List[str],
                       y_start: float, lastauthor: str, totalauthor: int) -> None:
        """Draw the introduction page with statistics."""
        updated_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        intro_fontsize_factor = 1.6

        # Add mode-specific text
        mode_text = ""
        if self.mode == AppMode.LAST_WEEK:
            mode_text = " : Legend Edition"

        text_lines = [
            f"🏢 สำนักพิมพ์ | Publisher : ยุงลาย - Yunglai",
            f"🖨 พิมพ์ที่ | Printed at : Bangkok Kunsthalle",
            f"🔢 พิมพ์ครั้งที่ | Print Count : {total_reach:,}{' Legend Edit.' if self.mode == AppMode.LAST_WEEK else ''}",
            f"📅 ปรับปรุง | Last Updated : {updated_date}",
            f"🧾 คำศัพท์ทั้งหมด | Total Words : {total_words:,}",
            f"🆕 คำล่าสุด | Latest Word : {latest_word}",
            f"📝 จำนวนผู้แต่ง | Total Authors : {totalauthor}",
            f"📝 ผู้แต่งล่าสุด | Latest Author : {lastauthor}",
            f"📚 คลังตัวอย่าง | Example Data : {total_meanings:,} sets",
            f"🔥 คำฮิต | Hottest Words :",
        ]

        self.draw_title(c, f"📖 ปทานุกรมแบบสับ - The Not-So Modern Dictionary{mode_text} 📖", y_start)
        y = y_start - self.line_space * 3

        for line in text_lines:
            y, _ = self.draw_mixed_text_wrapped(
                c, line, self.margin_left, y,
                "Kinnari", self.content_font_size * intro_fontsize_factor,
                "EmojiFont", self.content_font_size * intro_fontsize_factor)
            y -= self.line_space * intro_fontsize_factor * 0.7

        y += self.line_space * 0.2 * intro_fontsize_factor
        for line in hottest_word:
            y, _ = self.draw_mixed_text_wrapped(
                c, f"    • {line}", self.margin_left, y,
                "Kinnari", self.content_font_size * intro_fontsize_factor,
                "EmojiFont", self.content_font_size * intro_fontsize_factor)
            y -= self.line_space * intro_fontsize_factor * 0.6

        self.draw_page_number(c)
        c.showPage()

    def draw_fortune_page(self, c: canvas.Canvas, fortune_data: Dict[str, Any]) -> None:
        """Draw the fortune telling page with a random word and its prediction."""
        fortune_fontsize_factor = 0.7
        y = self.margin_top

        # Mode-specific title
        mode_text = ""
        if self.mode == AppMode.LAST_WEEK:
            mode_text = " : Legend Edition"

        self.draw_title(c, f"🪄 ปทานุกรมทำนาย - FortuneDict{mode_text} 🪄", y)
        y -= self.line_space * 3 if self.mode == AppMode.NORMAL else self.line_space * 3
        indent = 10

        word = random.choice(list(fortune_data.keys()))
        fortune = fortune_data[word]

        c.setFont("EmojiFont", self.header_font_size * 3 * fortune_fontsize_factor)
        c.drawCentredString(self.width / 2, y, "🔮")
        y -= self.line_space * (4 if self.mode == AppMode.NORMAL else 3)

        c.setFont("Kinnari-Bold", self.header_font_size * 2.5 * fortune_fontsize_factor)
        c.drawCentredString(self.width / 2, y, word)
        y -= self.line_space * 2

        c.setFont("Kinnari-Italic", self.header_font_size * 1.5 * fortune_fontsize_factor)
        c.drawCentredString(self.width / 2, y, "ศัพท์ทำนายสำหรับคุณ")
        y -= self.line_space * (6 if self.mode == AppMode.NORMAL else 4) * fortune_fontsize_factor

        y, _ = self.draw_mixed_text_wrapped_centered(
            c, fortune["th"], self.width / 2 + indent, y,
            "Kinnari", self.content_font_size * 2 * fortune_fontsize_factor,
            "EmojiFont", self.content_font_size * 2 * fortune_fontsize_factor,
            round(self.line_space * 2.5 * fortune_fontsize_factor)
        )
        y -= self.line_space * 1.5 * fortune_fontsize_factor

        y, _ = self.draw_mixed_text_wrapped_centered(
            c, fortune["en"], self.width / 2 + indent, y,
            "Kinnari", self.content_font_size * 2 * fortune_fontsize_factor,
            "EmojiFont", self.content_font_size * 2 * fortune_fontsize_factor,
            round(self.line_space * 2.5 * fortune_fontsize_factor)
        )
        y -= self.line_space * 2 * fortune_fontsize_factor

        if "ln" in fortune:
            y, _ = self.draw_mixed_text_wrapped_centered(
                c, fortune["ln"], self.width / 2 + indent, y,
                "LN", self.content_font_size * 2 * fortune_fontsize_factor,
                "EmojiFont", self.content_font_size * 2 * fortune_fontsize_factor,
                round(self.line_space * 2.5 * fortune_fontsize_factor)
            )
            y -= self.line_space * 1.5 * fortune_fontsize_factor

        # Last week special message
        if self.mode == AppMode.LAST_WEEK:
            y -= self.line_space * 2 * fortune_fontsize_factor
            y, _ = self.draw_mixed_text_wrapped_centered(
                c, "🏆 The limited legend edition is only available to visitors on the exhibition's final weekend. 🏆 รุ่นลิมิเต็ด \"Legend\" จะเก็บไว้เพื่อผู้มาเข้างานสัปดาห์สุดท้ายของนิทรรศการเท่านั้น",
                self.width / 2 + indent, y,
                "Kinnari", self.content_font_size * 2 * fortune_fontsize_factor * 0.9,
                "EmojiFont", self.content_font_size * 2 * fortune_fontsize_factor * 0.9,
                round(self.line_space * 2.5 * fortune_fontsize_factor)
            )

        self.draw_page_number(c)

    def draw_latest_word_page(self, c: canvas.Canvas, word: str, info: Dict[str, Any]) -> None:
        """Draw a page dedicated to the latest added word."""
        latest_fontsize_factor = 0.7
        y = self.margin_top

        mode_text = ""
        if self.mode == AppMode.LAST_WEEK:
            mode_text = " : Legend Edition"

        self.draw_title(c, f"The Not-So Modern Dictionary 🤩 The New Entry{mode_text}", y)
        y -= self.line_space * 3

        c.setFont("Kinnari-Bold", self.header_font_size * 2)
        c.drawCentredString(self.width / 2, y, word)
        y -= self.line_space * 3

        meanings = info.get("meaning", [])
        if isinstance(meanings, str):
            meanings = [meanings]
        meanings = meanings[-4:]

        y, _ = self.draw_mixed_text_wrapped_centered(
            c, f"📝 ความหมาย | Meaning", self.width / 2, y,
            "Kinnari", self.content_font_size * 2 * latest_fontsize_factor,
            "EmojiFont", self.content_font_size * 2 * latest_fontsize_factor,
            self.line_space * 2 * latest_fontsize_factor)
        y -= self.line_space * latest_fontsize_factor

        for m in meanings:
            y, _ = self.draw_mixed_text_wrapped_centered(
                c, f"🔹 {m[:50]}", self.width / 2, y,
                "Kinnari", self.content_font_size * 2 * latest_fontsize_factor,
                "EmojiFont", self.content_font_size * 2 * latest_fontsize_factor,
                self.line_space * 2 * latest_fontsize_factor * 0.9)
            y -= self.line_space * 2 * latest_fontsize_factor * 0.5
        y -= self.line_space

        examples = info.get("example", [])
        if isinstance(examples, str):
            examples = [examples]
        examples = examples[-4:]

        y, _ = self.draw_mixed_text_wrapped_centered(
            c, f"💬 ตัวอย่าง | Examples", self.width / 2, y,
            "Kinnari", self.content_font_size * 2 * latest_fontsize_factor,
            "EmojiFont", self.content_font_size * 2 * latest_fontsize_factor,
            self.line_space * latest_fontsize_factor * 0.9)
        y -= self.line_space * 2 * latest_fontsize_factor

        for ex in examples:
            y, _ = self.draw_mixed_text_wrapped_centered(
                c, f"🔹 {ex[:50]}", self.width / 2, y,
                "Kinnari", self.content_font_size * 2 * latest_fontsize_factor,
                "EmojiFont", self.content_font_size * 2 * latest_fontsize_factor,
                self.line_space * 2 * latest_fontsize_factor * 0.9)
            y -= self.line_space * 2 * latest_fontsize_factor * 0.5

        author_list = info.get("author")
        if isinstance(author_list, list) and author_list:
            author = author_list[-1]
        elif isinstance(author_list, str):
            author = author_list
        else:
            author = None

        if author:
            y -= self.line_space * 2
            y, _ = self.draw_mixed_text_wrapped_centered(
                c, f"📝 ผู้แต่งล่าสุด | Latest Author", self.width / 2, y,
                "Kinnari", self.content_font_size * 2 * latest_fontsize_factor,
                "EmojiFont", self.content_font_size * 2 * latest_fontsize_factor,
                self.line_space * 2.5 * latest_fontsize_factor)
            y -= self.line_space * latest_fontsize_factor
            y, _ = self.draw_mixed_text_wrapped_centered(
                c, f" {author[:40]}", self.width / 2, y,
                "Kinnari", self.content_font_size * 2 * latest_fontsize_factor,
                "EmojiFont", self.content_font_size * 2 * latest_fontsize_factor,
                self.line_space * 2 * latest_fontsize_factor)

        self.draw_page_number(c)
        c.showPage()

    def draw_entry(self, c: canvas.Canvas, word: str, info: Dict[str, Any], x: float,
                  y_start: float, line_height: float, max_reach: int, column_width: float,
                  indent: int = 10, current_meaning_idx: int = 0,
                  current_example_idx: int = 0, draw_header: bool = True) -> Tuple[float, bool, int, int]:
        """
        Draw parts of a dictionary entry within a column.

        Returns:
            Tuple of (new_y, finished_drawing, next_meaning_idx, next_example_idx)
        """
        current_y = y_start
        entry_fontsize_factor = 0.7

        reach = info.get("reach", 1)
        stars = self.get_star_rating(reach, max_reach)

        if draw_header:
            header_text = f" {word}{stars}"

            temp_y_header, _ = self.draw_mixed_text_wrapped(
                c, header_text, x, current_y,
                "Kinnari-Bold", self.header_font_size * entry_fontsize_factor,
                "EmojiFont", round(self.header_font_size * 0.7 * entry_fontsize_factor),
                line_height, max_text_width=column_width, dry_run=True)
            estimated_header_height = current_y - temp_y_header + (line_height * 0.2 * entry_fontsize_factor)

            if current_y - estimated_header_height < self.margin_bottom:
                return y_start, False, current_meaning_idx, current_example_idx

            current_y, _ = self.draw_mixed_text_wrapped(
                c, header_text, x, current_y,
                "Kinnari-Bold", self.header_font_size * entry_fontsize_factor,
                "EmojiFont", round(self.header_font_size * 0.7 * entry_fontsize_factor),
                line_height, max_text_width=column_width)
            current_y -= line_height * 0.2 * entry_fontsize_factor

        meanings = info.get("meaning", [])
        if isinstance(meanings, str):
            meanings = [meanings]

        meaning_resume_idx = current_meaning_idx
        for idx in range(meaning_resume_idx, len(meanings)):
            m = meanings[idx]

            temp_y_meaning, _ = self.draw_mixed_text_wrapped(
                c, f"📝 {m[:50]}", x + indent, current_y,
                "Kinnari", self.content_font_size * entry_fontsize_factor,
                "EmojiFont", (self.content_font_size - 2) * entry_fontsize_factor,
                line_height, max_text_width=column_width - indent, dry_run=True)
            estimated_meaning_height = current_y - temp_y_meaning + (line_height * 0.2 * entry_fontsize_factor)

            if current_y - estimated_meaning_height < self.margin_bottom:
                return current_y, False, idx, current_example_idx

            current_y, _ = self.draw_mixed_text_wrapped(
                c, f"📝 {m}", x + indent, current_y,
                "Kinnari", self.content_font_size * entry_fontsize_factor,
                "EmojiFont", (self.content_font_size - 2) * entry_fontsize_factor,
                line_height, max_text_width=column_width - indent)
            current_y -= line_height * 0.15 * entry_fontsize_factor
            meaning_resume_idx = idx + 1

        examples = info.get("example", [])
        if isinstance(examples, str):
            examples = [examples]

        example_resume_idx = current_example_idx
        if meaning_resume_idx == len(meanings):
            for idx in range(example_resume_idx, len(examples)):
                ex = examples[idx]

                temp_y_example, _ = self.draw_mixed_text_wrapped(
                    c, f"💬 {ex[:50]}", x + indent, current_y,
                    "Kinnari", self.content_font_size * entry_fontsize_factor,
                    "EmojiFont", (self.content_font_size - 2) * entry_fontsize_factor,
                    line_height, max_text_width=column_width - indent, dry_run=True)
                estimated_example_height = current_y - temp_y_example + (line_height * 0.2 * entry_fontsize_factor)

                if current_y - estimated_example_height < self.margin_bottom:
                    return current_y, False, meaning_resume_idx, idx

                current_y, _ = self.draw_mixed_text_wrapped(
                    c, f"💬 {ex}", x + indent, current_y,
                    "Kinnari", self.content_font_size * entry_fontsize_factor,
                    "EmojiFont", (self.content_font_size - 2) * entry_fontsize_factor,
                    line_height, max_text_width=column_width - indent)
                current_y -= line_height * 0.15 * entry_fontsize_factor
                example_resume_idx = idx + 1

        if meaning_resume_idx == len(meanings) and example_resume_idx == len(examples):
            current_y += line_height * 0.3
            temp_y_reach, _ = self.draw_mixed_text_wrapped(
                c, f" 📈 {reach}", x + indent, current_y,
                "Kinnari", round(self.content_font_size * 0.9 * entry_fontsize_factor),
                "EmojiFont", round(self.content_font_size * 0.8 * entry_fontsize_factor),
                round(line_height * 0.8), max_text_width=column_width - indent, dry_run=True)
            estimated_reach_height = current_y - temp_y_reach + (line_height * 2 * entry_fontsize_factor)

            if current_y - estimated_reach_height < self.margin_bottom:
                return current_y, False, meaning_resume_idx, example_resume_idx

            current_y, _ = self.draw_mixed_text_wrapped(
                c, f" 📈 {reach}", x + indent, current_y,
                "Kinnari", round(self.content_font_size * 0.9 * entry_fontsize_factor),
                "EmojiFont", round(self.content_font_size * 0.8 * entry_fontsize_factor),
                round(line_height * 0.8), max_text_width=column_width - indent)
            current_y -= line_height * 2 * entry_fontsize_factor
            return current_y, True, 0, 0

        return current_y, False, meaning_resume_idx, example_resume_idx

    def add_template_background(self, template_path: str, input_pdf_path: str,
                               output_pdf_path: str, apply_from_page_index: Optional[int] = None,
                               apply_to_page_index: Optional[int] = None) -> None:
        """
        Add a background template to specific pages of a PDF using PyMuPDF.

        Args:
            template_path: Path to template PDF
            input_pdf_path: Input PDF path
            output_pdf_path: Output PDF path
            apply_from_page_index: Starting page index (default 4)
            apply_to_page_index: Ending page index (default last page)
        """
        if not os.path.exists(template_path):
            app_logger.error(f"Template file not found at '{template_path}'")
            try:
                fitz.open(input_pdf_path).save(output_pdf_path)
                app_logger.warning(f"Copied input to output as template was missing")
            except Exception as e:
                app_logger.error(f"Failed to copy PDF: {e}")
            return

        template_doc = fitz.open(template_path)
        input_doc = fitz.open(input_pdf_path)
        output_doc = fitz.open()

        try:
            template_page = template_doc.load_page(0)
            bg_pix = template_page.get_pixmap(alpha=False)
            bg_img_rect = template_page.rect

            start_page_idx = apply_from_page_index if apply_from_page_index is not None else 4
            end_page_idx = apply_to_page_index if apply_to_page_index is not None else len(input_doc) - 1

            start_page_idx = max(0, start_page_idx)
            end_page_idx = min(len(input_doc) - 1, end_page_idx)

            for i in range(len(input_doc)):
                page = input_doc.load_page(i)
                new_output_page = output_doc.new_page(-1, width=page.rect.width, height=page.rect.height)
                new_output_page.show_pdf_page(page.rect, input_doc, i)

                if start_page_idx <= i <= end_page_idx:
                    new_output_page.insert_image(bg_img_rect, pixmap=bg_pix, overlay=False)

            output_doc.save(output_pdf_path)

        except Exception as e:
            app_logger.error(f"Error applying template background: {e}")
            try:
                fitz.open(input_pdf_path).save(output_pdf_path)
            except Exception as e_copy:
                app_logger.error(f"Failed to copy PDF after error: {e_copy}")
        finally:
            template_doc.close()
            input_doc.close()
            output_doc.close()

    def make_foldable_booklet(self, input_path: str, output_path: str,
                             random_page: Optional[int] = None) -> None:
        """
        Rearrange pages of a PDF to create a foldable booklet layout.

        Args:
            input_path: Input PDF path
            output_path: Output PDF path
            random_page: Specific random page number (optional)
        """
        doc = fitz.open(input_path)
        total_pages = len(doc)
        w, h = 842, 595  # A4 landscape

        if total_pages < 8:
            app_logger.info(f"Padding PDF from {total_pages} to 8 pages")
            for _ in range(8 - total_pages):
                doc.new_page(width=w, height=h)

        total_pages = len(doc)

        if random_page is None:
            page_order = [0, 1, 2, 3, 4, 5,
                         random.randint(7, total_pages - 2) if total_pages > 8 else 7,
                         total_pages - 1 if total_pages > 0 else 0]
        else:
            page_order = [0, 1, 2, 3, 4, 5, random_page - 1, total_pages - 1 if total_pages > 0 else 0]

        output_doc = fitz.open()
        new_page = output_doc.new_page(width=w, height=h)

        section_w, section_h = w / 4, h / 2

        for i, idx in enumerate(page_order):
            if idx >= len(doc):
                continue

            src_page = doc.load_page(idx)
            col, row = i % 4, 0 if i < 4 else 1
            x0, y0 = col * section_w, row * section_h
            target_rect = fitz.Rect(x0, y0, x0 + section_w, y0 + section_h)

            rotation = 180 if i < 4 else 0
            new_page.show_pdf_page(target_rect, doc, idx, rotate=rotation)

        output_doc.save(output_path)
        doc.close()
        output_doc.close()

    def merge_pdfs(self, append_pdf_path: str, base_pdf_path: str, output_pdf_path: str) -> None:
        """
        Merge two PDF files, appending one to the beginning of another.

        Args:
            append_pdf_path: PDF to prepend
            base_pdf_path: Base PDF
            output_pdf_path: Output path
        """
        writer = PdfWriter()

        append_pdf = PdfReader(append_pdf_path)
        for page in append_pdf.pages:
            writer.add_page(page)

        base_pdf = PdfReader(base_pdf_path)
        for page in base_pdf.pages:
            writer.add_page(page)

        with open(output_pdf_path, 'wb') as out_f:
            writer.write(out_f)

    def print_pdf_file(self, pdf_path: str, printer_name: Optional[str] = None) -> None:
        """
        Print a PDF file to the specified printer.

        Args:
            pdf_path: Path to PDF file
            printer_name: Printer name (optional)
        """
        abs_pdf_path = os.path.abspath(pdf_path).replace("\\", "/")

        app_logger.info(f"Printing file: {abs_pdf_path}")
        if not os.path.exists(abs_pdf_path):
            app_logger.error(f"PDF file not found at {abs_pdf_path}")
            return

        system = platform.system()
        app_logger.info(f"Detected OS: {system}")

        if system == "Windows":
            try:
                if printer_name:
                    # Use PowerShell to print
                    ps_command = f'Start-Process -FilePath "{abs_pdf_path}" -Verb PrintTo -ArgumentList "{printer_name}"'
                    subprocess.run(["powershell", "-Command", ps_command], check=True)
                else:
                    # Open print dialog
                    os.startfile(abs_pdf_path, "print")
                app_logger.info("Print command sent successfully")
            except Exception as e:
                app_logger.error(f"Error printing on Windows: {e}")
        else:
            try:
                if printer_name:
                    subprocess.run(["lpr", "-P", printer_name, abs_pdf_path], check=True)
                else:
                    subprocess.run(["lpr", abs_pdf_path], check=True)
                app_logger.info("Print command sent successfully")
            except Exception as e:
                app_logger.error(f"Error printing on Unix: {e}")

    def generate_dictionary_pdf(self, author: Optional[str] = None) -> str:
        """
        Generate the complete dictionary PDF with all features.

        Args:
            author: Author name for the new entry (optional)

        Returns:
            Path to generated booklet PDF
        """
        app_logger.info(f"Starting PDF generation (mode: {self.mode})")

        # Load database
        json_path = self.db.db_file
        if not os.path.exists(json_path):
            app_logger.error(f"Database file not found: {json_path}")
            return ""

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.register_fonts()

        # Setup temp paths
        temp_output = self.output_path.replace(".pdf", "_temp.pdf")
        intermediate_path = self.output_path.replace(".pdf", "_plain.pdf")

        for path in [temp_output, intermediate_path, self.output_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError as e:
                    app_logger.warning(f"Could not remove {path}: {e}")

        max_reach = max((entry.get("reach", 1) for entry in data.values()), default=1)

        # Create canvas
        c = canvas.Canvas(temp_output, pagesize=A4)

        # Calculate statistics
        total_meanings = 0
        total_reach = 0
        latest_word = ""
        latest_time = ""
        lastauthor = author if author else "ไม่ระบุ"
        top_words = []
        authors_set = set()

        for word, info in data.items():
            meanings = info.get("meaning", [])
            if isinstance(meanings, str):
                meanings = [meanings]
            total_meanings += len(meanings)

            reach = info.get("reach", 0)
            total_reach += reach
            top_words.append((word, reach))

            author_info = info.get("author", None)
            if isinstance(author_info, list):
                authors_set.update(author_info)
            elif isinstance(author_info, str):
                authors_set.add(author_info)

            update_time = info.get("update", "")
            if update_time > latest_time:
                latest_time = update_time
                latest_word = word
                if isinstance(author_info, list):
                    lastauthor = author_info[-1] if author_info else "ไม่ระบุ"
                else:
                    lastauthor = author_info if author_info else "ไม่ระบุ"

        # Load fortune data
        fortune_data = {}
        if os.path.exists(self.fortune_json_path):
            with open(self.fortune_json_path, "r", encoding="utf-8") as f:
                fortune_data = json.load(f)
        else:
            app_logger.warning(f"Fortune file not found: {self.fortune_json_path}")

        top_words = sorted(top_words, key=lambda x: x[1], reverse=True)
        hottest_words_text = [f"{w} ({r})" for w, r in top_words[:5]]
        totalauthor = len(authors_set)

        # Draw intro page
        self.draw_intro_page(
            c, total_words=len(data), total_meanings=total_meanings,
            total_reach=total_reach, latest_word=latest_word,
            hottest_word=hottest_words_text, y_start=self.margin_top,
            lastauthor=lastauthor, totalauthor=totalauthor
        )

        # Draw latest word page
        if latest_word in data:
            self.draw_latest_word_page(c, latest_word, data[latest_word])
            app_logger.info(f"Drew latest word page: {latest_word}")
        else:
            app_logger.warning(f"Latest word not found in data: {latest_word}")

        # Draw content with 2 columns
        y_left_col = self.margin_top - self.line_space * 2
        y_right_col = self.margin_top - self.line_space * 2
        y_left_col_start_of_page = y_left_col
        y_right_col_start_of_page = y_right_col

        sorted_words = sorted(data.keys(), key=locale.strxfrm)

        first_char_on_page = self.get_main_thai_consonant(sorted_words[0]) if sorted_words else ""
        self.draw_title(c, f"The Not-So Modern Dictionary 📚 {first_char_on_page}", self.margin_top)
        c.setFont("Kinnari", self.content_font_size)

        current_word_idx = 0
        current_meaning_idx = 0
        current_example_idx = 0
        draw_header_for_current_word = True

        while current_word_idx < len(sorted_words):
            word = sorted_words[current_word_idx]
            info = data[word]

            if y_left_col > self.margin_bottom + 60:
                new_y_left, finished_in_col, meaning_idx_left, example_idx_left = \
                    self.draw_entry(c, word, info, self.column1_x, y_left_col, self.line_space,
                                  max_reach, self.column_width,
                                  current_meaning_idx=current_meaning_idx,
                                  current_example_idx=current_example_idx,
                                  draw_header=draw_header_for_current_word)
            else:
                new_y_left, finished_in_col, meaning_idx_left, example_idx_left = \
                    self.draw_entry(c, word, info, self.column1_x,
                                  y_left_col - 60 - self.margin_bottom, self.line_space,
                                  max_reach, self.column_width,
                                  current_meaning_idx=current_meaning_idx,
                                  current_example_idx=current_example_idx,
                                  draw_header=draw_header_for_current_word)

            if finished_in_col:
                y_left_col = new_y_left
                current_word_idx += 1
                current_meaning_idx = 0
                current_example_idx = 0
                draw_header_for_current_word = True
            else:
                y_left_col = new_y_left
                current_meaning_idx = meaning_idx_left
                current_example_idx = example_idx_left

                new_y_right, finished_in_col, meaning_idx_right, example_idx_right = \
                    self.draw_entry(c, word, info, self.column2_x, y_right_col, self.line_space,
                                  max_reach, self.column_width,
                                  current_meaning_idx=current_meaning_idx,
                                  current_example_idx=current_example_idx,
                                  draw_header=draw_header_for_current_word)

                if finished_in_col:
                    y_right_col = new_y_right
                    current_word_idx += 1
                    current_meaning_idx = 0
                    current_example_idx = 0
                    draw_header_for_current_word = True
                else:
                    y_right_col = new_y_right
                    current_meaning_idx = meaning_idx_right
                    current_example_idx = example_idx_right

                    self.draw_page_number(c)
                    c.showPage()
                    y_left_col = y_left_col_start_of_page
                    y_right_col = y_right_col_start_of_page

                    first_char_on_page = self.get_main_thai_consonant(word)
                    self.draw_title(c, f"The Not-So Modern Dictionary 📚 {first_char_on_page}",
                                  self.margin_top)
                    c.setFont("Kinnari", self.content_font_size)

        self.draw_page_number(c)
        c.showPage()

        # Draw fortune page
        if fortune_data:
            self.draw_fortune_page(c, fortune_data)

        self.draw_page_number(c)
        c.save()
        os.rename(temp_output, intermediate_path)

        # Merge PDFs
        base_file = intermediate_path
        output_file = base_file.replace('.pdf', '_complete.pdf')
        self.merge_pdfs(self.cover_append_file, base_file, output_file)
        app_logger.info(f"Created merged PDF: {output_file}")

        # Get total pages
        doc = fitz.open(output_file)
        total_pages = len(doc)
        doc.close()

        # Apply templates
        output_temp = self.output_path.replace(".pdf", "_temp2.pdf")

        self.add_template_background(self.template_pdf_path1, output_file, output_temp, 4, 4)
        os.remove(output_file)
        os.rename(output_temp, output_file)

        self.add_template_background(self.template_pdf_path2, output_file, output_temp, 5, 5)
        os.remove(output_file)
        os.rename(output_temp, output_file)

        random_page = random.randint(7, total_pages - 2) if total_pages > 8 else 7
        app_logger.info(f"Random page: {random_page}")
        self.add_template_background(self.template_pdf_path3, output_file, output_temp,
                                    random_page - 1, random_page - 1)
        os.remove(output_file)
        os.rename(output_temp, output_file)

        self.add_template_background(self.template_pdf_path4, output_file, self.output_path,
                                    total_pages - 1, total_pages - 1)

        # Create booklet
        output_booklet = self.output_path.replace(".pdf", "_booklet.pdf")
        app_logger.info(f"Creating booklet from: {self.output_path}")
        self.make_foldable_booklet(input_path=self.output_path, output_path=output_booklet,
                                  random_page=random_page)

        # Print if enabled
        if self.printer_active:
            app_logger.info(f"Printing: {output_booklet}")
            self.print_pdf_file(output_booklet)
        else:
            app_logger.info("Printing disabled")

        app_logger.info(f"PDF generation complete: {output_booklet}")
        return output_booklet
