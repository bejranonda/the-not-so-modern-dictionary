# Installation Guide

## Requirements

- Python 3.8 or higher (tested on Python 3.8-3.13)
- pip (Python package manager)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TheNotSoModernDictionary.git
cd TheNotSoModernDictionary
```

### 2. Install Dependencies

#### For Python 3.12 and below:
```bash
pip install -r requirements.txt
```

#### For Python 3.13+:
The `playsound` library has compatibility issues with Python 3.13+. We've included `pygame` as a compatible alternative.

```bash
pip install -r requirements.txt
```

If you encounter errors with `playsound`, install without it:
```bash
pip install PyQt5 gtts pygame sounddevice scipy numpy SpeechRecognition reportlab PyMuPDF opencv-python rich
```

### 3. Audio Compatibility

The project includes `audio_compat.py` which provides automatic fallback:
- **First choice**: `playsound` (if available)
- **Fallback**: `pygame` (Python 3.13+ compatible)
- **No audio**: Prints warnings instead of playing sounds

To use the compatibility layer in your code:
```python
# Instead of:
# from playsound import playsound

# Use:
from audio_compat import playsound
```

## Platform-Specific Notes

### Windows
- PyQt5 should install without issues
- Audio playback works with both playsound and pygame

### macOS
- You may need to install portaudio for PyAudio:
  ```bash
  brew install portaudio
  pip install pyaudio
  ```

### Linux
- Install system dependencies:
  ```bash
  sudo apt-get install python3-pyqt5 portaudio19-dev python3-opencv
  pip install -r requirements.txt
  ```

## Running the Application

### Refactored Version (Recommended)
```bash
# Kiosk mode (full-screen exhibition mode)
python main.py

# Normal edition
python -c "from main import run_normal_edition; run_normal_edition()"

# Last week special edition
python -c "from main import run_lastweek_edition; run_lastweek_edition()"

# Debug mode (console only, no GUI)
python -c "from main import run_debug_mode; run_debug_mode()"
```

### Legacy Exhibition Code
```bash
# Normal edition
python thai_slang_dict_main.py

# Last week edition
python thai_slang_dict_main_lastweek.py
```

## Troubleshooting

### Issue: "No module named 'PyQt5'"
**Solution**: Install PyQt5
```bash
pip install PyQt5
```

### Issue: "playsound" won't install on Python 3.13+
**Solution**: This is expected. The project will automatically use pygame instead. Make sure pygame is installed:
```bash
pip install pygame
```

### Issue: Audio doesn't play
**Solutions**:
1. Check that audio files exist in `assets/audio/`
2. Verify the audio backend loaded: `python -c "from audio_compat import playsound"`
3. Install pygame: `pip install pygame`

### Issue: Camera/motion detection not working
**Solution**: This is optional. The application will work without a camera. Install opencv-python if needed:
```bash
pip install opencv-python
```

### Issue: PDF generation fails
**Solution**: Check that fonts exist in `assets/fonts/`:
- Kinnari.ttf
- NotoEmoji-Regular.ttf

## Testing the Installation

Run the validation test:
```bash
python test_reorganization.py
```

This will check:
- Directory structure
- File paths
- Audio files
- Fonts
- Templates
- Python syntax

All tests should pass before running the application.

## Optional Dependencies

### For Speech Recognition (Whisper)
Uncomment in `requirements.txt`:
```
whisper>=1.0.0
```

Then install:
```bash
pip install openai-whisper
```

## Development Setup

For development, you may want additional tools:
```bash
pip install pytest black flake8
```

## Support

If you encounter issues:
1. Run `python test_reorganization.py` to check the setup
2. Check that all files in `assets/` exist
3. Verify Python version: `python --version`
4. Check installed packages: `pip list`

For more information, see the project README.md or contact the developers.
