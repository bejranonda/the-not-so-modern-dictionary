# input_slang_word.py

import json
import os

SLANG_FILE = "user_added_slang.json"

def load_slang_data(filepath=SLANG_FILE):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_slang_data(data, filepath=SLANG_FILE):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def prompt_slang_entry():
    word = input("🔤 คำสแลง: ").strip()
    meaning = input("📝 ความหมาย: ").strip()
    example = input("💬 ตัวอย่างประโยค: ").strip()

    return word, {
        "meaning": meaning,
        "example": example
    }

def add_new_entry():
    data = load_slang_data()
    word, entry = prompt_slang_entry()
    
    if word in data:
        print(f"⚠️ คำว่า '{word}' มีอยู่แล้ว แทนที่ข้อมูลเดิม")
    data[word] = entry
    save_slang_data(data)
    print(f"✅ เพิ่มคำสแลงใหม่เรียบร้อย: {word}")

if __name__ == "__main__":
    add_new_entry()
