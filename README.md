# The Not-So-Modern Dictionary
## ปทานุกรมแบบสับ

Interactive installation software for collective dictionary creation

![The Not-SO-modern dictionary](https://github.com/user-attachments/assets/e99736a3-1984-4f89-8f80-16ca84b7d280)
Photo by Suphitchaya Khunchamni

### About

This interactive installation invites visitors to become contributors to a collective, ever-evolving dictionary. Using a custom word-generation program, each visitor creates unique entries—be it slang terms, misused words, or moments of language in flux. The result is printed into a mini-dictionary that visitors can take home, alongside entries from past participants.

**Part of "This page is intentionally left _____."**
**Yoonglai Collective**
**13 June - 17 August 2025**
Exhibition at [Bangkok Kunsthalle](https://www.khaoyaiart.com/bangkok-kunsthalle/exhibitions/this-page-is-intentionally-left-_____.)

### Credits

**Interactive Installation by Collaboration:**
- **Werapol Bejranonda** (Engineer)
- **Yoonglai Collective** (Artists)
- **Mixed Media:** Software interface, desktop station, printed booklet

The program was co-developed by Yoonglai Collective and Werapol Bejranonda.
A playful nod to So Sethaputra's New-Modern Dictionary, this version resists fixed definitions. It reflects how meaning is constantly negotiated—from street language to screen, from grassroots to algorithm.

![DictionaryBooklet](https://github.com/user-attachments/assets/84312ad4-1ce3-4ec5-b464-3ec6595a4b0b)
Photo by Sineenuch Malaisri

## Getting Started

### Prerequisites

- Python 3.x
- PyQt5
- Required Python packages (see `requirements.txt` if available)
- Audio files in the respective sound directories
- Thai fonts (Kinnari.ttf) for PDF generation

### Running the Application

#### Standard Version
```bash
python thai_slang_dict_main.py
```

#### Last Week Edition (Exhibition Final Week)
```bash
python thai_slang_dict_main_lastweek.py
```

### Key Components

#### Main Scripts
- **`thai_slang_dict_main.py`** - Main application entry point
- **`thai_slang_dict_main_lastweek.py`** - Special version for exhibition's final week

#### Core Modules
- **`thai_slang_kiosk.py`** - PyQt5-based kiosk interface
- **`slang_pdf_generator.py`** - PDF generation for dictionary booklets
- **`input_slang_utils.py`** - Utilities for speech, motion detection, and logging
- **`greetings.py`** - Greeting message collections

#### Features

- **Kiosk Mode Interface:** Full-screen PyQt5 application for exhibition use
- **Speech Recognition:** Thai language speech input processing
- **Motion Detection:** Automatic user presence detection
- **PDF Generation:** Creates personalized dictionary booklets
- **Multi-language Support:** Thai and Khmer language capabilities
- **Audio Feedback:** Sound effects and TTS for user interaction
- **Logging System:** Comprehensive request and interaction logging

#### Sound Assets
- System startup sounds
- Page flipping effects
- Success/error feedback
- User interaction audio cues

#### Project Structure
```
├── thai_slang_dict_main.py          # Main application
├── thai_slang_dict_main_lastweek.py # Exhibition final week version
├── thai_slang_kiosk.py              # Kiosk interface
├── slang_pdf_generator.py           # PDF generation
├── input_slang_utils.py             # Core utilities
├── greetings.py                     # Greeting messages
├── fonts/                           # Thai and emoji fonts
├── template/                        # PDF templates
├── *sound/                          # Audio assets directories
└── output/                          # Generated content

```

## Installation & Setup

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install PyQt5 gtts playsound opencv-python numpy scipy reportlab fitz
   ```
3. Ensure audio files are present in respective sound directories
4. Place Thai fonts in the `fonts/` directory
5. Run the main script to start the application

![332821_0](https://github.com/user-attachments/assets/165949d4-04e1-401c-8e76-724502dcea29)
Photo by Phenphan Anantacharoen

## Software Components Summary

### Core System Architecture
**Programming Environment:** Python-based system designed for cross-platform compatibility (Linux, Windows, macOS) due to unknown hardware specifications until 3 days before launch

### 1. Interactive Kiosk System
**Multi-screen Interface:**
- 7-screen flow system with full-screen display for focused user experience
- Step-by-step data entry: Word → Meaning → Example → Summary → Confirmation → Print
- Text-to-speech integration for accessibility and engagement

**Input Processing:**
- Real-time slang word collection from visitors
- Database integration with existing entries
- Duplicate word detection and merging system
- Continuous statistical updates

### 2. Hardware Integration
**Standard Computer Peripherals:**
- **Camera:** Motion detection for user presence activation
- **Speakers:** Bilingual audio prompts (Thai/English) with playful language
- **Keyboard:** Text input interface
- **Printer:** Automatic booklet generation

**Smart Resource Utilization:** Maximum functionality from standard computer components without additional hardware requirements

### 3. Database Management
**Dynamic Content System:**
- User-generated content processing
- Real-time database updates
- Statistical analysis and reporting
- Content merging for duplicate entries

### 4. Booklet Generation System
**Automated Publishing:**
- Real-time PDF generation
- Personalized content with user's latest entry as featured content
- Random page selection from existing database
- Statistical summary integration
- User credited as "latest author"

### 5. AI-Powered Features
**FortuneDict System:**
- AI-generated greeting messages
- Fortune cookie-style predictions using slang words
- Systematic AI integration for user engagement

### 6. Easter Egg Mechanisms
**Gamification Elements:**
- "System Hacked" alerts (1 in 20 users see full dictionary)
- "Jackpot" system (1 in 10 users access 8 pages instead of 1)
- Remote script injection for dynamic content updates

### 7. Development Methodology
**Lean Engineering Approach:**
- Rapid development cycle (2-3 weeks for 3-month level project)
- Iterative development process
- Real-time monitoring and debugging capabilities
- Remote access for live system management

## Technical Highlights

- **Cross-platform compatibility** for unknown deployment environment
- **Motion detection** for automated user engagement
- **Real-time data processing** with live statistical updates
- **AI-powered content generation** for personalized experiences
- **Remote monitoring and logging** for real-time system evaluation and debugging

This software demonstrates sophisticated integration of user interface design, database management, hardware interaction, and AI systems to create an engaging, interactive art installation.

## Exhibition Context

The Not-So-Modern Dictionary is designed as an art installation piece that challenges traditional notions of language documentation. It creates a space where language becomes fluid, collaborative, and constantly evolving—reflecting how meaning is negotiated in our digital age.

## License

Art installation software - Please contact creators for usage permissions.
