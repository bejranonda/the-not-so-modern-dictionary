# The Not-So-Modern Dictionary
> *"Language is not fixed or authoritative"*

*A collaborative art installation where language becomes living, evolving, and collectively owned*

**The Not-So-Modern Dictionary** is a participatory art installation where visitors become lexicographers - contributing slang definitions that instantly print as personalized mini-dictionary booklets.

Built with Python, PyQt5, and motion detection, the kiosk system collected **534 unique slang terms from 462 contributors** during its exhibition in Bangkok Kunsthalle, proving language belongs to everyone. Watch your word join a living archive where contradictory definitions coexist and every visitor takes home a unique snapshot of collective meaning-making.


<img width="753" height="762" alt="image" src="https://github.com/user-attachments/assets/16d74ae1-58eb-4ff7-960d-5a4cec986033" />

*Visitors interact with the dictionary kiosk at Bangkok Kunsthalle.*

## 📍 Exhibition

- **Project Name:** The Not-So-Modern Dictionary (ปทานุกรมแบบสับ)
- **Medium:** Interactive installation (software interface, kiosk station, printed booklets)
- **Exhibition:** "This page is intentionally left _____" by Yoonglai Collective
- **Dates:** 13 June - 17 August 2025
- **Venue:** [Bangkok Kunsthalle](https://www.khaoyaiart.com/bangkok-kunsthalle/exhibitions/this-page-is-intentionally-left-_____.), Bangkok, Thailand
- **Type:** Participatory installation

**Exhibition Impact** During this three-month run:
- **462 visitors** contributed **534 unique slang terms**
- creating **748 complete dictionary entries**
- and taking home **544 personalized booklets**.
- The most popular word, **"จาบ" (Jaab)**, was submitted seven times with different definitions—proof that language truly belongs to everyone.

A playful critique of So Sethaputra's authoritative *New Model English-Thai Dictionary*, this installation invites visitors to become lexicographers of their own evolving language.


## 🎭 The Experience: Your Word, Your Dictionary

**Imagine this:** You approach a glowing computer station. Before you even touch it, a camera senses your presence and greets you in Thai. The screen invites you to share a word—maybe slang from your friend group, a term born on social media, or a word you've always used "wrong" but prefer anyway.

**You type it in.** The system asks what it means *to you*—no dictionaries to consult, no correct answers to find. Just your understanding. You add an example sentence showing how you'd use it. The screen reads everything back to you in a synthesized voice.

**Then comes the magic.** A printer whirs to life and outputs a personalized mini-dictionary booklet. Your word appears prominently inside, nestled among random entries from the hundreds of other visitors who came before you. No two booklets are identical. Sometimes you get lucky—a "jackpot" giving you eight pages instead of one, or the system playfully claims it's been "hacked" and shows you the entire database.

**But there's one more surprise.** On the last page of your booklet, you discover a personal fortune—like opening a fortune cookie, but with your slang word woven into the prediction. "Your fierce energy will impress everyone around you" or "Everything you do will shine effortlessly." Each fortune randomly selected from a curated collection, making your dictionary not just a linguistic record but a small moment of delight.

**You leave with a dictionary you helped create.** Your word joins 534 others in a living archive that grows with each visitor, where "จาบ" has seven different definitions and every contradiction is preserved. This is language as it really works: messy, democratic, and constantly in flux.

![Sample dictionary booklet showing user-contributed entries](https://github.com/user-attachments/assets/84312ad4-1ce3-4ec5-b464-3ec6595a4b0b)

*A personalized mini-dictionary booklet ready for visitors to take home. Photo by Sineenuch Malaisri*


## The Idea: Who Really Owns Language?

📚 **The traditional answer:** Dictionaries say experts do. Authoritative tomes like So Sethaputra's *New Model English-Thai Dictionary* tell us the "correct" meanings, printed in unchanging ink. Language is something to be mastered, standardized, and preserved by those who know better.

🌊 **The reality:** Language doesn't work that way—especially today. New slang emerges hourly on social media. Terms shift meaning across communities. "Correct" usage gets debated in comment sections, group chats, and TikTok videos. Meaning is negotiated collectively, messily, democratically.

✨ **Our response:** Make everyone a lexicographer. This installation doesn't validate or correct your entries. It simply asks what words mean to you, then preserves your definition alongside everyone else's. When seven different people define "จาบ" seven different ways, the system celebrates all of them. The result is a dictionary that reflects how meaning is actually created: collectively, contradictorily, and in constant evolution.

Language isn't owned by experts. It's co-created by all of us, every time we speak.


![The Not-So-Modern Dictionary installation at Bangkok Kunsthalle](https://github.com/user-attachments/assets/e99736a3-1984-4f89-8f80-16ca84b7d280)

*Installation of the dictionary kiosk at Bangkok Kunsthalle. Photo by Suphitchaya Khunchamni*


## The Technology: Making Language Magic

### ✨ Key Features

- 👥 **Participatory Lexicography** – Every visitor becomes a dictionary contributor, not just a reader
- 📚 **Living Database** – 534 unique slang terms collected from 462 contributors during the exhibition
- 🎁 **Personalized Booklets** – Each visitor receives a unique printout featuring their word alongside random entries, with a fortune-cookie-style prediction on the last page
- 👁️ **Motion-Activated Interface** – Camera-based presence detection automatically greets approaching visitors
- 🔊 **Bilingual Audio Experience** – Thai and English text-to-speech guides users through the process
- 🎰 **Gamified Easter Eggs** – Random jackpots, "system hacked" alerts, and AI-generated fortunes (25% combined probability)
- 🔄 **Multiple Meanings Welcome** – The system embraces contradictory definitions of the same word
- 📊 **Real-Time Statistics** – Live tracking of total words, authors, and most popular terms

### 🚶 The Journey

**The journey begins with your movement.** A camera watches in standby mode. When you approach, it detects the change and triggers a welcoming voice speaking Thai through text-to-speech. You're guided through five simple steps on a full-screen interface designed to focus your attention entirely on defining your word.

**Behind the friendly interface,** the system works hard:

1. 🔍 **Checks the database** – Does your word already exist? If so, your new definition gets added rather than replaced. Multiple truths can coexist.

2. 💾 **Saves instantly** – Every entry goes into a JSON database file, timestamped and credited to you (or kept anonymous if you prefer).

3. 🎲 **Rolls the dice** – Random probability determines if you'll get a surprise:
   - **10% chance:** Jackpot! Eight pages instead of one
   - **5% chance:** "System hacked" alert revealing the full database
   - **15% chance:** An AI-generated fortune using your word

4. 📄 **Generates your booklet** – A PDF engine combines your word with random selections from other entries, formats everything with Thai fonts, and adds live statistics.

5. 🖨️ **Prints immediately** – Your personalized dictionary emerges warm from the printer, unique in all the world.

**The participatory loop continues.** Your entry becomes part of the pool that future visitors might receive in their booklets. After 30 seconds of inactivity, the system gently asks if you're still there. After 60 seconds, it returns to standby, waiting for the next person to add their voice to this collective archive.


### 👥 What Visitors Experience

**The 7-Step Journey**

**1. 👁️ Arrival** – A motion sensor detects your presence. The screen awakens: "Touch any key to start"

**2. 👋 Greeting** – A synthesized Thai voice welcomes you warmly with random greetings ("สวัสดี", "ยินดีต้อนรับ"), making you feel like a collaborator.

**3. ✏️ Your Word** – Enter your slang word—that term only your friend group understands, or the word you've always used "wrong" but prefer your way. Maybe "จาบ", joining seven other definitions already in the system.

**4. 💭 The Meaning** – Define it in your own words. No experts to consult, no "correct" answer. Just your understanding. The system doesn't judge—it listens.

**5. 💬 Usage Example** – Show your word in action (optional). Demonstrate how it lives in real conversation and text messages.

**6. 👀 Review** – The system reads your complete entry back to you via text-to-speech. Does it capture what you meant?

**7. 📖 Take It Home** – Add your name (or stay anonymous), then the printer whirs to life.

**Your personalized booklet includes:**
- Your word as the "Latest Entry"
- Random selections from 534+ community-contributed words
- Live statistics (total words, contributors, popular terms)
- **A fortune on the last page**—drawn from a slang word in the database

**Hidden surprises (25% chance):**
- 🎰 **Jackpot** (10%) – Eight pages instead of one
- 🔓 **System Hacked** (5%) – Complete database revealed
- 🔮 **Special Fortune** (15%) – AI-generated prediction

The booklet is still warm from the printer. No two are ever identical. You leave with a tangible piece of a collaborative, ever-evolving archive.


![Visitor interacting with the kiosk](https://github.com/user-attachments/assets/165949d4-04e1-401c-8e76-724502dcea29)

*A visitor was captured and drawn in by the kiosk. Photo by Phenphan Anantacharoen*

### 🔮 The Fortune Cookie Surprise

**Every booklet ends with a prediction—powered by slang words**

Flip to the last page and discover a personal fortune, like opening a fortune cookie. But here's the twist: **each fortune is generated from a random slang word in the database**, creating thematic connections between your linguistic contribution and your prediction.

**How it works:**

Each slang word is paired with a trilingual fortune (Thai/English/Lao-Khmer). The system randomly selects one word and delivers its associated prediction.

**Examples from Standard Edition:**
- **"ปัง"** (pang - "awesome/shining") → *"Everything you do will shine effortlessly."*
- **"เข้ม"** (khem - "intense/fierce") → *"Your fierce energy will impress everyone around you."*

**Examples from Last-Week Special Edition:**
- **"วาร์ป"** (warp - "teleport") → *"You are about to warp to a new dimension full of opportunities. Be ready to step out of your comfort zone."*
- **"ปังไม่หยุด"** (pang-mai-yut - "unstoppable hit") → *"The unstoppable hit energy is flowing around you. Everything you think and do will succeed continuously."*

**Why fortunes in a dictionary?**

Traditional dictionaries end with definitions—cold, factual, authoritative. We wanted visitors to leave with something more: a moment of delight that transforms a reference document into a personal keepsake. Your fortune is literally drawn from the collective slang archive—**the words themselves speak your future**.


<img width="643" height="707" alt="image" src="https://github.com/user-attachments/assets/f5480de6-ec37-408b-9c14-9009fb5df112" />

*At the last page of their dictionary booklet, each visitor discovered a personal fortune.*

## Exhibition Results: By the Numbers

The Bangkok Kunsthalle deployment (13 June - 17 August 2025) achieved remarkable community engagement:

**📊 Overall Impact:**
- **462 Authors** – Total participants who contributed to the dictionary
- **534 Unique Words** – Distinct slang terms collected during the exhibition
- **748 Data Sets** – Complete submissions including words, meanings, and examples
- **544 Booklets** – Physical dictionaries printed and distributed to visitors

**🔥 Most Popular Slang (Hottest Words):**

1. **จาบ (Jaab)** – 7 submissions
2. **อาจจะยัง (Aat Ja Yang)** – 6 submissions
3. **โซะ (So)** – 5 submissions
4. **เกียม (Giam)** – 5 submissions
5. **เริ่ดเลอ (Roet Loe)** – 5 submissions

**📅 Final Entry (as of 11 September 2025):**
- **Latest Word:** บายบาย (Bye Bye)
- **Latest Author:** ดอปจชท (Dopjochot)

<img width="550" height="450" alt="Exhibition statistics dashboard showing 534 unique words from 462 contributors" src="https://github.com/user-attachments/assets/0681612b-a431-43f1-9166-4bc283318bf9" />

*Final exhibition statistics: A collaborative language documentation project demonstrating how interactive art installations create meaningful community engagement*

## If you need to understand more

### What It Does (Value for different audiences)

Imagine approaching a glowing computer station where you're invited not just to look up words, but to create them. The Not-So-Modern Dictionary transforms every visitor into a contributor to an ever-changing collective dictionary. You type in a slang word that exists only in your friend group, a term that's emerged from social media, or a word you've always used "wrong" but prefer your way. The system adds your word to a growing database of hundreds of other contributions, then instantly prints you a personalized mini-dictionary booklet to take home. Your booklet features your new word prominently, alongside random entries from previous visitors—creating a unique snapshot of this living language archive that's never quite the same twice. As you interact with the kiosk, the system speaks to you in Thai, detects your presence through a camera, and occasionally surprises you with "easter eggs": a jackpot that gives you eight pages instead of one, a playful "system hacked" alert that reveals the entire database, or an AI-generated fortune based on your word. Over the course of the exhibition, 462 people contributed 534 unique slang terms, creating 748 complete dictionary entries and printing 544 personalized booklets. The most popular word? "จาบ" (Jaab)—submitted seven times by different visitors who each defined it their own way. This is language as democracy: messy, contradictory, constantly negotiated, and beautifully alive.

### The Experience (What people encounter)

Traditional dictionaries present language as fixed and authoritative—words have the correct meaning, determined by experts and printed in unchanging ink. But language doesn't actually work that way, especially in our digital age where new slang emerges daily, meanings shift across communities, and "correct" usage is constantly contested in comment sections and group chats. We created this installation as a gentle rebellion against linguistic authority, inspired by So Sethaputra's influential Thai-English dictionary that shaped how generations understood "proper" language. By making every visitor a lexicographer, we ask: who really owns language? The system doesn't validate or correct your entries—it simply asks what words mean to you, then preserves your definition alongside everyone else's. The result is a dictionary that reflects how meaning is actually created: collectively, messily, and in constant flux between street language and screens, grassroots communities and algorithmic culture.



### How It Works

The installation centers on a kiosk station running custom software that guides visitors through creating their dictionary entry. When you approach, a camera detects your movement and the system greets you with a random Thai phrase spoken through text-to-speech. You then type your slang word, its meaning, and optionally an example sentence—all displayed on a full-screen interface that focuses your attention entirely on the act of definition. Behind the scenes, the system checks if your word already exists in the database. If it does, your new definition is added as an additional entry, allowing multiple interpretations to coexist. Once you confirm your submission and add your name (or choose to stay anonymous), the software generates a PDF booklet featuring your word alongside random selections from the database's hundreds of other entries. A printer immediately outputs your personalized dictionary, warm from the machine. The system includes playful surprises to reward participation: there's a 10% chance you'll hit the "jackpot" and receive an eight-page booklet instead of one, a 5% chance the system will jokingly claim it's been "hacked" and show you the complete database, and a 15% chance you'll receive an AI-generated fortune message incorporating your word. These gamified elements transform the act of linguistic documentation into something delightful and unpredictable—much like language itself.

<img width="1919" height="1079" alt="Lastweek_03" src="https://github.com/user-attachments/assets/75c70593-a8ea-4168-b2d3-190d4266c6d8" />

*Last week special edition released on the final week of the exhibition*

## 🚀 Getting Started with the source-code

### If You Want to Run It Yourself

**You'll need:**
- A computer running Windows, macOS, or Linux
- A webcam (for motion detection)
- Speakers (for audio feedback)
- A printer (for booklet output)
- Python 3.8 or newer

**Quick setup:**

```bash
# 1. Download the code
git clone https://github.com/bejranonda/the-not-so-modern-dictionary.git
cd the-not-so-modern-dictionary

# 2. Install required software components
pip install -r requirements.txt

# 3. Run the kiosk interface
python main.py
```

The system will open in full-screen kiosk mode. Press any key when you see the standby screen to begin. Your entries will be saved to `user_added_slang.json` and booklets will be generated in the `output/` folder.

**Python 3.13+ Note:** If you encounter issues with the `playsound` library, the project automatically falls back to `pygame` for audio playback. See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions and troubleshooting.

**Asset Files:** All required fonts and audio files are included in the `assets/` directory after installation.


## 🔧 For Developers

<!-- TECHNICAL DETAIL -->

### Architecture Overview

This project maintains two parallel codebases:
1. **Refactored architecture** (v2.0+, in `src/`) – Modular, maintainable code for future development
2. **Legacy code** (root level) – Original exhibition code preserved as deployment fallback

Both share the same data files, assets, and database structure.

### System Architecture

```
src/
├── app.py                    # Main application orchestrator (DictionaryApp class)
├── config/
│   └── settings.py           # Centralized constants, paths, and mode configurations
├── core/
│   ├── database.py           # SlangDatabase - JSON-based word storage and retrieval
│   └── easter_eggs.py        # EasterEggManager - probability-based surprise system
├── audio/
│   ├── speech.py             # SpeechEngine - gTTS Thai/English text-to-speech
│   └── sound_effects.py      # SoundManager - audio asset validation and playback
├── ui/
│   └── kiosk.py              # SlangKiosk - PyQt5 full-screen 7-step interface
├── pdf/
│   └── generator.py          # PDFGenerator - personalized booklet creation
└── utils/
    ├── logger.py             # Structured logging system
    └── requests.py           # Remote script injection for live updates
```

### Application Flow

**7-Step User Journey:**

1. **Standby (-1)** – Motion detection → Display logo → "Touch any key"
2. **Greeting (0)** – Random Thai greeting with text-to-speech
3. **Word Input (1)** – Enter slang word (checks for duplicates)
4. **Meaning (2)** – Define the word's meaning
5. **Example (3)** – Provide usage example (optional)
6. **Review (4)** – Confirm entry with audio read-back
7. **Attribution (5)** – Add your name → Generate PDF → Print booklet

```
Visitor Interaction (PyQt5 Kiosk Interface)
           ↓
Motion Detection (Camera)
           ↓
7-Step Data Entry Flow
           ↓
Real-time Database (SQLite)
           ↓
PDF Generation (ReportLab + Thai Fonts)
           ↓
Automatic Printing (Desktop Printer)
           ↓
Physical Mini-Dictionary
```


**Easter Egg System (in `src/core/easter_eggs.py`):**
- **Jackpot** (10%) – Receive 8 pages instead of 1
- **System Hacked** (5%) – See complete database dump
- **AI Fortune** (15%) – Get personalized prediction message

### Database Structure

**File:** `user_added_slang.json` (JSON format, auto-saved after each entry)

```json
{
  "word_lowercase": {
    "word": "Original Case",
    "meaning": "Definition text",
    "example": "Usage example sentence",
    "author": "Contributor name",
    "timestamp": "ISO8601 timestamp",
    "usage_count": 0
  }
}
```

**Key Operations:**
- `add_entry()` – Adds new word with auto-save
- `get_entry()` – Case-insensitive lookup
- `search_entries()` – Partial match search
- `get_statistics()` – Returns total words, authors, latest entry

### Hardware Integration

**Motion Detection** (`input_slang_utils.py`):
- OpenCV camera monitoring in standby mode
- Frame differencing algorithm for presence detection
- Automatic greeting sequence trigger

**Audio System:**
- **Text-to-Speech:** gTTS for Thai/English bilingual prompts
- **Sound Effects:** System startup, page flips, success/error feedback, beeps
- **Threading:** Audio plays in separate threads to avoid UI blocking

**Printer Integration:**
- Platform-specific print commands (Windows/macOS/Linux)
- Automatic PDF output after Step 5

### Running Different Modes

```bash
# Full-screen kiosk mode (default for exhibitions)
python main.py

# Normal edition (without kiosk features)
python -c "from main import run_normal_edition; run_normal_edition()"

# Last week special edition (with additional features)
python -c "from main import run_lastweek_edition; run_lastweek_edition()"

# Debug/console mode (no GUI, for testing)
python -c "from main import run_debug_mode; run_debug_mode()"
```

### PDF Generation Process

1. **Template Selection** – Load from `template/*.json` (predictions, database snapshots)
2. **Content Assembly:**
   - User's word featured prominently
   - Random selection from existing database (controlled by easter egg probability)
   - Statistics footer (total words, authors, current date)
   - **Fortune page** – Random fortune selected from prediction templates on the last page
3. **Font Handling:**
   - `fonts/Kinnari.ttf` for Thai script
   - `fonts/NotoEmoji-Regular.ttf` for emoji support
4. **Output:** `output/slang_dictionary.pdf` → Send to printer

### Fortune System

**Fortune Cookie Feature:**
Every booklet includes a personalized fortune on the last page, selected randomly from curated prediction templates.

**Template Files:**
- `template/th-en-ln_slang_predictions_99.json` – Standard edition fortunes (99 predictions)
- `template/th-en-ln_slang_predictions_lastweek.json` – Special last-week edition fortunes

**Fortune Structure (trilingual):**
```json
{
  "ปัง": {
    "th": "สิ่งที่คุณทำจะออกมาปังแบบไม่ต้องพยายามมาก",
    "en": "Everything you do will shine effortlessly.",
    "ln": "អ្វីគ្រប់យ៉ាងដែលអ្នកធ្វើនឹងចេញមកល្អឥតខ្ចោះដោយមិនចាំបាច់ប្រឹងប្រែងច្រើន។"
  }
}
```

**Implementation:**
- Fortunes are keyed by slang words, creating thematic connections
- Each fortune includes Thai (th), English (en), and Lao/Khmer (ln) translations
- Random selection during PDF generation ensures variety
- Creates a "fortune cookie" moment of delight for every visitor

### Idle Management & Timers

- **30 seconds idle** – Audio warning: "Are you still there?"
- **60 seconds idle** – Auto-return to standby
- **Reset trigger** – Any keyboard activity

### Remote Management

**Live Updates During Exhibition:**
- Place `do_request_special_routine` file to enable
- Execute Python code from `request_script.txt`
- Allows debugging and feature updates without restart

### Development Practices

**Adding New Features:**

```python
# 1. Add configuration to src/config/settings.py
AUDIO_PATHS["new_sound"] = str(SOUNDS_DIR / "folder" / "sound.mp3")

# 2. Use via SoundManager
from src.audio.sound_effects import SoundManager
sound_mgr = SoundManager()
sound_mgr.play_audio_file(AUDIO_PATHS["new_sound"])
```

**Key Technical Considerations:**
- **PyQt5 Threading** – Never call TTS/audio directly in UI thread; use `QTimer.singleShot()`
- **Font Paths** – PDF generation fails silently if Thai fonts missing
- **Process Management** – Application kills previous instances on startup
- **Cross-Platform** – Uses `pathlib.Path` for compatibility; process commands branch by OS

### Technology Stack

- **PyQt5** – GUI framework (GPL/Commercial dual license)
- **ReportLab** – PDF generation (BSD-style license)
- **gTTS** – Google Text-to-Speech (MIT license)
- **OpenCV** – Motion detection (Apache 2.0 license)
- **SpeechRecognition** – Speech input processing (BSD license)

### Version History

See [CHANGELOG.md](CHANGELOG.md) for complete release history.

**Major Releases:**
- **[v3.0.1](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/v3.0.1)** (Latest) – Exhibition final results and statistics
- **[v3.0.0](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/v3.0.0)** – Complete workflow documentation and user experience details
- **[2.0](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/2.0)** – Major refactoring with modular architecture
- **[1.0](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.0)** – Original exhibition version

### Further Reading

- [REFACTORING.md](REFACTORING.md) – Detailed migration guide from v1.x to v2.0 architecture
- [CLAUDE.md](CLAUDE.md) – Complete project documentation for AI assistance and development


## 🤝 Project Credits

### Collaboration

This installation emerged from a collaboration between:
- **Werapol Bejranonda** – Software engineering, system architecture, and technical implementation
- **[Yoonglai Collective](http://yoonglai.com/)** – Artistic concept, exhibition design, and cultural framing


### AI-Assisted Development

The software development leveraged AI assistants at different stages:
- **Gemini & ChatGPT** – Initial prototyping, code generation, and rapid feature development (2-3 weeks)
- **Claude** – Code refactoring, architecture restructuring, documentation, and quality improvement

This project demonstrates effective human-AI collaboration: what typically requires 3 months of development was accomplished in 2-3 weeks through AI-assisted rapid prototyping, then professionally refined through AI-guided refactoring.

### Exhibition Support

- **Bangkok Kunsthalle** – Exhibition venue, curatorial support, and technical facilities
- **Exhibition Visitors** – 462 contributors who created 534 unique dictionary entries, transforming the installation into a true collective work


## 📜 License & Usage

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

You are free to:
- ✅ **Share** – Copy and redistribute this software
- ✅ **Adapt** – Remix, transform, and build upon it for your own installations

Under these terms:
- **Attribution** – Credit Werapol Bejranonda and Yoonglai Collective
- **NonCommercial** – Not for commercial purposes without permission
- **ShareAlike** – Distribute modifications under the same license

**For Commercial Use:** Contact the creators for licensing arrangements.

**Copyright © 2024-2025 Werapol Bejranonda and Yoonglai Collective**

---

### 💡 Suggested Additions for Future Enhancement

To make this README even more effective, consider adding:

1. **Demo Video** – A 60-second screencast showing the complete user journey from motion detection through booklet printing
2. **Architecture Diagram** – Visual flowchart showing the 7-step process and system components
3. **Sample Booklet PDF** – Downloadable example of the generated output
4. **Cross-References** – Links to your other art-technology projects (PM2.5 Ghostbuster, Code of the Sea, Heating DJ) to show your collaborative practice
5. **Exhibition Documentation** – Additional photos showing different user interactions and the installation context
