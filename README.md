# The Not-So-Modern Dictionary
## ปทานุกรมแบบสับ

Interactive installation software for collective dictionary creation

![The Not-SO-modern dictionary](https://github.com/user-attachments/assets/e99736a3-1984-4f89-8f80-16ca84b7d280)
Photo by Suphitchaya Khunchamni

### About

This interactive installation invites visitors to become contributors to a collective, ever-evolving dictionary. Using a custom word-generation program, each visitor creates unique entries—be it slang terms, misused words, or moments of language in flux. The result is printed into a mini-dictionary that visitors can take home, alongside entries from past participants.

**Part of "This page is intentionally left _____."**
**by Yoonglai Collective**
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

- Python 3.8 or higher
- Audio files in the respective sound directories
- Thai fonts (Kinnari.ttf) for PDF generation

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure audio files are present in respective sound directories
4. Place Thai fonts in the `fonts/` directory

### Running the Application

#### Refactored Version (Recommended)
```bash
# Main application (kiosk mode)
python main.py

# Different modes
python -c "from main import run_normal_edition; run_normal_edition()"
python -c "from main import run_lastweek_edition; run_lastweek_edition()"
python -c "from main import run_debug_mode; run_debug_mode()"
```

#### Legacy Version (Original)
```bash
# Standard version
python thai_slang_dict_main.py

# Last week edition
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

**Refactored Architecture (v3.0+)**
```
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── REFACTORING.md                   # Refactoring documentation
├── src/                             # Refactored source code
│   ├── app.py                       # Main application class
│   ├── config/                      # Configuration management
│   │   └── settings.py              # Centralized settings
│   ├── core/                        # Core business logic
│   │   ├── database.py              # Database management
│   │   └── easter_eggs.py           # Easter egg functionality
│   ├── audio/                       # Audio processing
│   │   ├── speech.py                # TTS and speech recognition
│   │   └── sound_effects.py         # Sound effects management
│   └── utils/                       # Utility modules
│       └── logger.py                # Logging system
├── fonts/                           # Thai and emoji fonts
├── template/                        # PDF templates
├── *sound/                          # Audio assets directories
└── output/                          # Generated content
```

**Legacy Structure (preserved for compatibility)**
```
├── thai_slang_dict_main.py          # Original main application
├── thai_slang_dict_main_lastweek.py # Original lastweek version
├── thai_slang_kiosk.py              # Original kiosk interface
├── slang_pdf_generator.py           # Original PDF generation
├── input_slang_utils.py             # Original utilities
└── greetings.py                     # Original greeting messages
```

![332821_0](https://github.com/user-attachments/assets/165949d4-04e1-401c-8e76-724502dcea29)
Photo by Phenphan Anantacharoen

## User Workflow & Experience

### Interactive Kiosk Workflow

The application follows a carefully designed 7-step user journey:

#### **🔄 Step -1: Standby Mode**
- **Trigger**: Camera-based motion detection
- **Visual**: Yoonglai Collective logo with "Touch any key to start"
- **Audio**: Ambient standby mode
- **Interaction**: Any key press or detected motion triggers greeting

#### **👋 Step 0: Greeting & Welcome**
- **Content**: Random Thai greeting from curated collection
- **Audio**: Text-to-speech welcome message
- **Visual**: Full-screen welcome interface
- **Transition**: Automatic progression after greeting completes

#### **📝 Step 1: Word Input**
- **Prompt**: "กรุณาใส่คำสแลงที่ต้องการเพิ่ม" (Please enter the slang word to add)
- **Input**: Text field for slang word entry
- **Validation**: Checks for existing words in database
- **Audio**: Instructional prompts and confirmation sounds

#### **💭 Step 2: Meaning Definition**
- **Prompt**: "กรุณาใส่ความหมายของคำนี้" (Please enter the meaning of this word)
- **Input**: Text area for definition entry
- **Context**: Word from Step 1 displayed for reference
- **Audio**: Contextual guidance and feedback

#### **📚 Step 3: Example Usage**
- **Prompt**: "กรุณาใส่ตัวอย่างการใช้คำนี้" (Please provide usage example)
- **Input**: Text area for example sentence
- **Optional**: Users can skip this step
- **Audio**: Encouraging prompts and completion sounds

#### **📋 Step 4: Summary & Confirmation**
- **Display**: Complete entry review (word, meaning, example)
- **Validation**: Final chance to review and edit
- **Audio**: Entry read-back using text-to-speech
- **Interaction**: Confirmation to proceed to printing

#### **🖨️ Step 5: Attribution & Printing**
- **Prompt**: "กรุณาใส่ชื่อของคุณ (หรือกด Enter เพื่อไม่ระบุชื่อ)" (Enter your name or press Enter for anonymous)
- **Process**: PDF generation with user's entry
- **Easter Eggs**: Random chance for bonus content
- **Output**: Physical mini-dictionary printed and dispensed

### **🎰 Easter Egg System**

#### **Jackpot Feature (10% probability)**
- **Trigger**: Random selection during PDF generation
- **Effect**: User receives 8-page dictionary instead of standard 1-page
- **Message**: "🎰 แจ็คพอต! คุณได้รับหน้าพิเศษ 8 หน้า!" (JACKPOT! You get 8 special pages!)

#### **System Hacked Alert (5% probability)**
- **Trigger**: Random selection during session
- **Effect**: User sees full database content
- **Message**: "🔥 ระบบถูกแฮก! คุณได้เห็นพจนานุกรมทั้งหมด!" (System hacked! You see the full dictionary!)

#### **AI Fortune Messages (15% probability)**
- **Content**: Generated predictions using the user's submitted word
- **Examples**: "คำว่า 'xyz' จะนำโชคดีมาให้คุณในวันนี้" (The word 'xyz' will bring you luck today)

### **🔄 Idle State Management**

#### **Warning System**
- **30 seconds idle**: Audio warning announcement
- **60 seconds idle**: Automatic return to standby mode
- **User interaction**: Timer reset on any keyboard activity

#### **Motion Detection Integration**
- **Camera monitoring**: Continuous motion detection in standby
- **Wake-up trigger**: Movement automatically starts greeting sequence
- **Audio feedback**: Immediate sound confirmation on motion detection

### **📊 Database Integration Workflow**

#### **Real-time Processing**
1. **Input validation**: Check for duplicate entries
2. **Data merging**: Combine similar entries if word exists
3. **Statistical updates**: Increment usage counters
4. **Content formatting**: Prepare for PDF generation

#### **Content Personalization**
- **Latest entry featured**: User's word highlighted in generated PDF
- **Random selection**: Additional entries chosen from database
- **Statistical summary**: Live counts and contributors displayed

### **🎵 Audio Experience Design**

#### **Sound Design Elements**
- **System startup**: Game-style welcome sound
- **Page turning**: Realistic book flipping effects
- **Success feedback**: Pleasant confirmation chimes
- **Error handling**: Gentle correction sounds
- **Motion detection**: Immediate response beeps

#### **Text-to-Speech Integration**
- **Language support**: Thai primary, English secondary
- **Contextual prompts**: Step-specific instructions
- **Accessibility**: Audio readback of all user inputs
- **Bilingual content**: Automatic language detection and appropriate voice

### **🔧 Technical Workflow**

#### **Session Lifecycle**
1. **Initialization**: Load database, validate audio files, setup UI
2. **Motion monitoring**: Continuous camera feed analysis
3. **User session**: 7-step guided interaction
4. **PDF generation**: Real-time document creation
5. **Printing process**: Automatic document output
6. **Session cleanup**: Return to standby, log interaction

#### **Error Recovery**
- **Automatic restart**: System self-recovery on failures
- **Process isolation**: Duplicate instance prevention
- **Resource cleanup**: Temporary file management
- **Fallback modes**: Graceful degradation for missing components

This workflow creates an seamless, engaging experience that transforms language documentation from passive observation to active participation, making each visitor a contributor to the evolving dictionary.

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

## Exhibition Final Results

The "Legend Edition" deployment at Bangkok Kunsthalle (13 June - 17 August 2025) achieved remarkable community engagement:

### 📊 Overall Impact
- **462 Authors**: Total participants who contributed to the dictionary
- **534 Unique Words**: Distinct slang terms collected during the exhibition
- **748 Data Sets**: Complete submissions including words, meanings, and examples
- **544 Booklets**: Physical dictionaries printed and distributed to visitors

### 🔥 Most Popular Slang (Hottest Words)
The five most frequently submitted terms:

1. **จาบ (Jaab)** - 7 submissions
2. **อาจจะยัง (Aat Ja Yang)** - 6 submissions
3. **โซะ (So)** - 5 submissions
4. **เกียม (Giam)** - 5 submissions
5. **เริ่ดเลอ (Roet Loe)** - 5 submissions

### 📅 Final Activity (as of 11/09/2025)
- **Latest Word**: บายบาย (Bye Bye)
- **Latest Author**: ดอปจชท (Dopjochot)

This collaborative language documentation project demonstrates how interactive art installations can create meaningful community engagement and preserve evolving linguistic expressions.

## Version History & Releases

For detailed changelog, see [CHANGELOG.md](CHANGELOG.md).

### [v3.0.1](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/v3.0.1) - Latest Release
- **Exhibition Results**: Added final exhibition statistics and impact data
- **Community Metrics**: 462 authors, 534 unique words, 748 data sets, 544 booklets printed
- **Popular Terms**: Documented most frequently submitted slang words
- **Documentation**: Enhanced with real-world deployment results

### [v3.0.0](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/v3.0.0)
- **Major Feature**: Added comprehensive User Workflow & Experience documentation
- **Documentation**: Detailed 7-step interactive kiosk workflow
- **Easter Eggs**: Documented gamification system (Jackpot, System Hacked, AI Fortune)
- **Audio Experience**: Complete sound design and TTS integration details
- **Technical Workflow**: Session lifecycle and error recovery documentation
- **User Experience**: Motion detection, idle management, and accessibility features

### [2.0](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/2.0)
- **Refactoring**: Complete codebase restructure with modular architecture
- **Configuration**: Centralized settings and constants management
- **Audio System**: Dedicated speech and sound effects modules
- **Database**: Object-oriented database management with error handling
- **Logging**: Structured logging system with multiple levels
- **Dependencies**: Added comprehensive requirements.txt

### [1.4](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.4)
- **Voice Features**: Added voice to request functionality
- **Request System**: Routine and special request features
- **Code Quality**: Clean up and request function improvements

### [1.3special](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.3special)
- **Special Edition**: Special request function and enhanced menu
- **Bug Fixes**: Fixed double running script and menu display issues
- **Platform**: Updated menu for MAC compatibility

### [1.3](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.3)
- **Platform Support**: MAC printing and menu improvements
- **Code Cleanup**: Removed unnecessary libraries and components
- **UI Updates**: Menu text updates and display fixes

### [1.2](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.2)
- **Internationalization**: Local support for multiple languages
- **Templates**: Template functionality and external greeting list
- **UI Improvements**: Centered text and column debugging

### [1.1](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.1)
- **GUI Enhancements**: Added logo and 2-column layout
- **Printing**: Print to printer functionality
- **Motion Detection**: Increased motion sensitivity

### [1.0](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/1.0) - Original Exhibition Version
- **Core Features**: Template system, Intro and Fortune pages
- **Language Support**: English fortune and Thai content
- **Statistics**: Enhanced statistics and user collaboration features
- **Exhibition**: Deployed for Bangkok Kunsthalle exhibition

### Early Development Versions
- [0.4](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/0.4) - Enhanced data collection
- [0.3](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/0.3) - Basic statistics
- [0.2](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/0.2) - Core dictionary features
- [0.1](https://github.com/bejranonda/the-not-so-modern-dictionary/releases/tag/0.1) - Initial release

## License

Art installation software - Please contact creators for usage permissions.
