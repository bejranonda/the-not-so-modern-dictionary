"""
Configuration settings for The Not-So-Modern Dictionary application.
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
FONTS_DIR = BASE_DIR / "fonts"
TEMPLATE_DIR = BASE_DIR / "template"
OUTPUT_DIR = BASE_DIR / "output"
SOUNDS_DIR = BASE_DIR

# Audio settings
AUDIO_PATHS = {
    "flipping": [str(SOUNDS_DIR / "flipping sound" / "pageturn-102978.mp3")],
    "invalid": [str(SOUNDS_DIR / "error sound" / "error-call-to-attention-129258.mp3")],
    "correct": str(SOUNDS_DIR / "correct sound" / "correct-6033.mp3"),
    "system_start": str(SOUNDS_DIR / "systemstart sound" / "game-start-6104.mp3"),
    "start_beep": str(SOUNDS_DIR / "beep sound" / "point-smooth-beep-230573.mp3"),
    "end_beep": str(SOUNDS_DIR / "beep sound" / "short-beep-tone-47916.mp3"),
}

# Kiosk settings
KIOSK_SETTINGS = {
    "idle_warning_time": 30 * 1000,  # milliseconds
    "reset_time": 60 * 1000,  # milliseconds
    "fullscreen": True,
    "screen_flow_count": 7,
}

# Database settings
DATABASE_SETTINGS = {
    "user_slang_file": "user_added_slang.json",
    "request_log_file": "request_log.txt",
}

# PDF generation settings
PDF_SETTINGS = {
    "thai_font_path": str(FONTS_DIR / "Kinnari.ttf"),
    "emoji_font_path": str(FONTS_DIR / "NotoEmoji-Regular.ttf"),
    "output_path": str(OUTPUT_DIR / "slang_dictionary.pdf"),
    "page_size": "A4",
}

# Speech recognition settings
SPEECH_SETTINGS = {
    "language": "th-TH",
    "sample_rate": 16000,
    "recording_duration": 3,  # seconds
}

# Greeting messages
GREETING_MESSAGES = [
    "สวัสดีจ้า ต้องการเพิ่มคำศัพท์ไหม",
    "Hi มาเพิ่มคำศัพท์กันไหม",
    "ลองเพิ่มคำศัพท์กันดีมะ",
    "ช่วยกันเพิ่มคำศัพท์กันได้ไหม",
    "มาเพิ่มศัพท์ไปด้วยกันไหม",
]

NOT_UNDERSTAND_MESSAGES = [
    "ไม่เข้าใจอ่ะ ช่วยพูดอีกที",
    "ไม่เข้าใจ พูดใหม่หน่อยนะ",
    "ไม่รู้เรื่อง พูดใหม่อีกที",
    "ช่วยพูดใหม่อีกทีนะ",
    "ช่วยพูดใหม่หน่อยนะ",
]

# Khmer greetings
KHMER_GREETINGS = [
    "ពួក​ថៃ​គេ​ចាប់​ផ្ដើម​ស្អប់​ខ្មែរ​យើង​បណ្ដើរ​ៗ​ហើយ​",
    "លឺ​តែ​សង្គ្រាម​កាល​គេ​បាញ់​ខ្មែរ​ស្លាប់",
    "​​គេ​មិន​សូវ​ពេញ​ចិត្ត​យើង​គេ​យើង​ជា​ជនជាតិ​ខ្មែរ​អីចឹង​"
]

# Easter egg settings
EASTER_EGG_SETTINGS = {
    "jackpot_probability": 0.1,  # 1 in 10
    "system_hacked_probability": 0.05,  # 1 in 20
    "jackpot_pages": 8,
    "normal_pages": 1,
}

# Application modes
class AppMode:
    NORMAL = "normal"
    LAST_WEEK = "lastweek"
    KIOSK = "kiosk"
    DEBUG = "debug"