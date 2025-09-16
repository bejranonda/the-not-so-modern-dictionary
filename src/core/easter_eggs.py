"""
Easter egg functionality for the dictionary application.
"""
import random
from typing import Dict, Any

from ..config.settings import EASTER_EGG_SETTINGS, KHMER_GREETINGS
from ..utils.logger import app_logger


class EasterEggManager:
    """Manages easter eggs and special events in the application."""

    def __init__(self):
        self.settings = EASTER_EGG_SETTINGS

    def check_jackpot(self) -> bool:
        """
        Check if user hits the jackpot (gets more pages).

        Returns:
            True if jackpot is triggered
        """
        is_jackpot = random.random() < self.settings["jackpot_probability"]
        if is_jackpot:
            app_logger.info("🎰 JACKPOT! User gets extra pages")
        return is_jackpot

    def check_system_hacked(self) -> bool:
        """
        Check if "system hacked" event is triggered.

        Returns:
            True if system hacked event is triggered
        """
        is_hacked = random.random() < self.settings["system_hacked_probability"]
        if is_hacked:
            app_logger.info("🔓 SYSTEM HACKED! User sees full dictionary")
        return is_hacked

    def get_pages_count(self) -> int:
        """
        Get the number of pages to generate based on easter eggs.

        Returns:
            Number of pages (1 normal, 8 for jackpot)
        """
        if self.check_jackpot():
            return self.settings["jackpot_pages"]
        return self.settings["normal_pages"]

    def get_special_greeting(self) -> str:
        """
        Get a special Khmer greeting message.

        Returns:
            Random Khmer greeting
        """
        return random.choice(KHMER_GREETINGS)

    def generate_fortune_message(self, word: str) -> str:
        """
        Generate a fortune cookie style message using the word.

        Args:
            word: The slang word to incorporate into the fortune

        Returns:
            Fortune message
        """
        fortune_templates = [
            f"คำว่า '{word}' จะนำโชคดีมาให้คุณในวันนี้",
            f"การใช้คำว่า '{word}' จะทำให้คุณเจอเพื่อนใหม่",
            f"'{word}' เป็นคำที่จะเปลี่ยนชีวิตคุณ",
            f"วันนี้คุณจะได้ยินคำว่า '{word}' อีกครั้ง",
            f"คำว่า '{word}' คือกุญแจสู่ความสำเร็จของคุณ",
        ]

        return random.choice(fortune_templates)

    def generate_ai_greeting(self) -> str:
        """
        Generate an AI-powered greeting message.

        Returns:
            AI-generated greeting
        """
        ai_greetings = [
            "🤖 AI พูดว่า: มาสร้างพจนานุกรมแห่งอนาคตกันเถอะ!",
            "🧠 ระบบ AI ต้อนรับคุณสู่โลกแห่งภาษาใหม่",
            "💫 AI แนะนำ: ภาษาคือการเดินทางที่ไม่มีที่สิ้นสุด",
            "🔮 AI ทำนาย: คุณจะเป็นส่วนหนึ่งของวิวัฒนาการภาษา",
            "⚡ AI เตือน: คำที่คุณจะเพิ่มจะเปลี่ยนโลก",
        ]

        return random.choice(ai_greetings)

    def should_show_special_content(self) -> Dict[str, bool]:
        """
        Determine what special content should be shown.

        Returns:
            Dictionary with boolean flags for special content
        """
        return {
            "jackpot": self.check_jackpot(),
            "system_hacked": self.check_system_hacked(),
            "special_greeting": random.random() < 0.1,  # 10% chance
            "ai_greeting": random.random() < 0.05,  # 5% chance
            "fortune_message": random.random() < 0.15,  # 15% chance
        }

    def log_easter_egg_event(self, event_type: str, details: str = "") -> None:
        """
        Log easter egg events for analytics.

        Args:
            event_type: Type of easter egg event
            details: Additional details about the event
        """
        app_logger.info(f"🥚 Easter Egg: {event_type} - {details}")

    def get_hacked_message(self) -> str:
        """
        Get the system hacked message.

        Returns:
            Hacked system message
        """
        messages = [
            "🔥 ระบบถูกแฮก! คุณได้เห็นพจนานุกรมทั้งหมด!",
            "💀 SYSTEM BREACHED! Full dictionary access granted!",
            "🚨 แฮกเกอร์เจาะระบบ! ข้อมูลทั้งหมดรั่วไหล!",
            "⚠️ UNAUTHORIZED ACCESS! All entries exposed!",
        ]

        return random.choice(messages)

    def get_jackpot_message(self) -> str:
        """
        Get the jackpot message.

        Returns:
            Jackpot celebration message
        """
        messages = [
            "🎰 แจ็คพอต! คุณได้รับหน้าพิเศษ 8 หน้า!",
            "💎 JACKPOT! You won 8 special pages!",
            "🏆 โชคดี! พจนานุกรมพิเศษสำหรับคุณ!",
            "🌟 LUCKY WIN! Extended dictionary edition!",
        ]

        return random.choice(messages)