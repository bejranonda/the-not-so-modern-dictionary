"""
Speech synthesis and recognition utilities.
"""
import os
import tempfile
import threading
import uuid
from typing import List, Optional

import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from gtts import gTTS
import playsound

from ..config.settings import SPEECH_SETTINGS
from ..utils.logger import app_logger


class SpeechEngine:
    """Handles text-to-speech and speech recognition functionality."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.temp_files: List[str] = []

    def speak_thai(self, text: str) -> None:
        """
        Convert Thai text to speech and play it asynchronously.

        Args:
            text: Thai text to speak
        """
        def _speak():
            filename = None
            try:
                filename = f"temp_{uuid.uuid4().hex}.mp3"
                self.temp_files.append(filename)

                tts = gTTS(text=text, lang='th')
                tts.save(filename)
                playsound.playsound(filename)

            except Exception as e:
                app_logger.error(f"Error in speak_thai: {e}")
            finally:
                self._cleanup_temp_file(filename)

        threading.Thread(target=_speak, daemon=True).start()

    def speak_both(self, text: str) -> None:
        """
        Speak text in both Thai and English.
        Text should be formatted as 'thai_text<br>english_text'

        Args:
            text: Bilingual text separated by <br>
        """
        def _speak():
            files = []
            try:
                if '<br>' in text:
                    thai_part, eng_part = text.split('<br>', 1)
                else:
                    thai_part, eng_part = text, ''

                # Generate Thai audio
                if thai_part.strip():
                    filename_th = f"temp_{uuid.uuid4().hex}_th.mp3"
                    tts_th = gTTS(text=thai_part.strip(), lang='th')
                    tts_th.save(filename_th)
                    files.append(filename_th)

                # Generate English audio
                if eng_part.strip():
                    filename_en = f"temp_{uuid.uuid4().hex}_en.mp3"
                    tts_en = gTTS(text=eng_part.strip(), lang='en')
                    tts_en.save(filename_en)
                    files.append(filename_en)

                # Play both files in sequence
                for file in files:
                    playsound.playsound(file)

            except Exception as e:
                app_logger.error(f"Error in speak_both: {e}")
            finally:
                for file in files:
                    self._cleanup_temp_file(file)

        threading.Thread(target=_speak, daemon=True).start()

    def recognize_thai_google(self) -> str:
        """
        Recognize Thai speech using Google Speech Recognition.

        Returns:
            Recognized text or "เงียบ" if recognition fails
        """
        try:
            with sr.Microphone() as source:
                app_logger.info("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

                result = self.recognizer.recognize_google(
                    audio,
                    language=SPEECH_SETTINGS["language"]
                )
                app_logger.info(f"Recognized: {result}")
                return result

        except Exception as e:
            app_logger.error(f"Speech recognition error: {e}")
            return "เงียบ"

    def recognize_thai_whisper(self, whisper_model) -> str:
        """
        Recognize Thai speech using Whisper model.

        Args:
            whisper_model: Loaded Whisper model

        Returns:
            Recognized text or error message
        """
        try:
            fs = SPEECH_SETTINGS["sample_rate"]
            seconds = SPEECH_SETTINGS["recording_duration"]

            app_logger.info("🎤 Recording audio (Whisper)...")
            audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=".") as temp_file:
                temp_filename = temp_file.name
                wavfile.write(temp_filename, fs, audio)

            app_logger.info("🧠 Processing with Whisper...")
            result = whisper_model.transcribe(temp_filename, language="th")
            text = result["text"].strip().lower()

            # Cleanup
            os.remove(temp_filename)

            app_logger.info(f"Whisper recognized: {text}")
            return text

        except Exception as e:
            app_logger.error(f"Whisper recognition error: {e}")
            return "ระบบมีปัญหา"

    def _cleanup_temp_file(self, filename: Optional[str]) -> None:
        """Clean up temporary audio files."""
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
                if filename in self.temp_files:
                    self.temp_files.remove(filename)
            except Exception as e:
                app_logger.error(f"Error cleaning up temp file {filename}: {e}")

    def cleanup_all_temp_files(self) -> None:
        """Clean up all temporary files."""
        for filename in self.temp_files.copy():
            self._cleanup_temp_file(filename)