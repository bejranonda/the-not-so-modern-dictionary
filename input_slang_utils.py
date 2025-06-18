## input_slang_utils.py

from gtts import gTTS
import playsound
import os
import cv2
import numpy as np
import time
import uuid
import threading

import importlib.util
import traceback
from datetime import datetime

import platform
import subprocess
import shutil
import fitz # PyMuPDF

import random

def log_request_message(message):
    with open("request_log.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

def speak_thai(text):
    def play():
        try:
            filename = f"temp_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=text, lang='th')
            tts.save(filename)
            playsound.playsound(filename)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    threading.Thread(target=play, daemon=True).start()

def speak_both(text):
    def play():
        try:
            if '<br>' in text:
                thai_part, eng_part = text.split('<br>', 1)
            else:
                thai_part, eng_part = text, ''

            files = []

            if thai_part.strip():
                filename_th = f"temp_{uuid.uuid4().hex}_th.mp3"
                tts_th = gTTS(text=thai_part.strip(), lang='th')
                tts_th.save(filename_th)
                files.append(filename_th)

            if eng_part.strip():
                filename_en = f"temp_{uuid.uuid4().hex}_en.mp3"
                tts_en = gTTS(text=eng_part.strip(), lang='en')
                tts_en.save(filename_en)
                files.append(filename_en)

            for file in files:
                playsound.playsound(file)

        finally:
            for file in files:
                if os.path.exists(file):
                    os.remove(file)

    threading.Thread(target=play, daemon=True).start()


def detect_motion(threshold=1000000, timeout=5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ไม่สามารถเปิดกล้องได้")
        return False

    start_time = time.time()
    motion_detected = False

    while time.time() - start_time < timeout:
        ret, frame1 = cap.read()
        time.sleep(0.1)
        ret, frame2 = cap.read()
        if not ret:
            break

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        motion_score = np.sum(thresh)

        print(f"ตรวจสอบการเคลื่อนไหว (motion score): {motion_score}")
        if motion_score > threshold:
            motion_detected = True
            break

    cap.release()
    return motion_detected


def make_foldable_jackpot(input_path, output_path):
    """Create a single-sheet 8-section PDF from randomly selected 8 pages (starting from page 5 onward)."""
    doc = fitz.open(input_path)
    total_pages = len(doc)
    w, h = 842, 595  # A4 landscape

    if total_pages <= 5:
        raise ValueError("PDF must have more than 5 pages to allow random selection from page 5 onward.")
    
    # Select 8 unique pages from index 5 to end
    available_pages = list(range(5, total_pages-1))
    if len(available_pages) < 8:
        raise ValueError(f"Not enough pages (found {len(available_pages)}) after page 4 to select 8 unique pages.")
    
    selected_pages = sorted(random.sample(available_pages, 8))  # Ascending order

    output_doc = fitz.open()
    new_page = output_doc.new_page(width=w, height=h)

    section_w, section_h = w / 4, h / 2  # 4 cols × 2 rows

    for i, idx in enumerate(selected_pages):
        src_page = doc.load_page(idx)
        col, row = i % 4, 0 if i < 4 else 1
        x0, y0 = col * section_w, row * section_h
        target_rect = fitz.Rect(x0, y0, x0 + section_w, y0 + section_h)
        rotation = 180 if i < 4 else 0
        new_page.show_pdf_page(target_rect, doc, idx, rotate=rotation)

    output_doc.save(output_path)
    doc.close()
    output_doc.close()
    

def print_pdf_file(pdf_path, printer_name=None):
    """
    Prints a PDF file to the specified printer on Windows or Linux/macOS.
    For Windows, it attempts to use PowerShell for silent printing,
    then falls back to specific PDF viewers (Adobe Reader, SumatraPDF) if needed.
    For Windows without a named printer, it opens the print dialog.
    For Linux/macOS, it uses the `lpr` command.
    """
    # Convert to absolute path
    # Ensure the path uses forward slashes for consistency in PowerShell arguments
    # and to avoid issues with backslashes needing escaping.
    abs_pdf_path = os.path.abspath(pdf_path).replace("\\", "/")

    print(f"กำลังสั่งพิมพ์ไฟล์: {abs_pdf_path}")
    if not os.path.exists(abs_pdf_path):
        print(f"❌ ข้อผิดพลาด: ไม่พบไฟล์ PDF ที่ {abs_pdf_path} ไม่สามารถสั่งพิมพ์ได้")
        return
    
    system = platform.system()
    print(f"ระบบปฏิบัติการที่ตรวจพบ: {system}")

    if system == "Windows":
        printed_successfully = False
        
        # --- Attempt 1: Using PowerShell with PrintTo verb (relies on default app association) ---
        if printer_name:
            # Use 'Start-Process' with double quotes around file path for spaces and to handle forward slashes
            # Using os.path.normpath to ensure correct path formatting for Windows native commands
            # and then replacing backslashes with forward slashes for PowerShell compatibility.
            quoted_abs_pdf_path = f'"{os.path.normpath(abs_pdf_path)}"'
            cmd = f'PowerShell.exe -Command "Start-Process -FilePath {quoted_abs_pdf_path} -Verb PrintTo -ArgumentList \'{printer_name}\'"'
            print(f"คำสั่ง Windows (PowerShell - PrintTo): {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW) # Use CREATE_NO_WINDOW for silent process
                print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน PowerShell PrintTo)")
                print("หากไม่เห็นงานพิมพ์ โปรดตรวจสอบคิวงานพิมพ์ของเครื่องพิมพ์และโปรแกรมดู PDF เริ่มต้น")
                printed_successfully = True
            except subprocess.CalledProcessError as e:
                print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (PowerShell PrintTo): {e.stderr.decode('utf-8') if e.stderr else 'ไม่มีรายละเอียด'}")
                print("   สาเหตุอาจเกิดจาก: ไม่มีแอปพลิเคชันเชื่อมโยงกับไฟล์ PDF หรือการเชื่อมโยงเสียหาย")
                print("   กำลังลองวิธีอื่น...")
            except FileNotFoundError:
                print(f"❌ ข้อผิดพลาด: ไม่พบ PowerShell หรือ Start-Process. กำลังลองวิธีอื่น...")
            except Exception as e:
                print(f"❌ ข้อผิดพลาดที่ไม่คาดคิดในการสั่งพิมพ์ (PowerShell PrintTo): {e}. กำลังลองวิธีอื่น...")
        
        # --- Attempt 2: Using known PDF viewers directly (if Attempt 1 fails or no printer_name) ---
        if not printed_successfully and printer_name:
            # Common paths for Adobe Reader and SumatraPDF
            program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
            program_files = os.environ.get("ProgramFiles", r"C:\Program Files")

            adobe_reader_paths = [
                os.path.join(program_files_x86, r"Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
                os.path.join(program_files, r"Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
                os.path.join(program_files_x86, r"Adobe\Reader 11.0\Reader\AcroRd32.exe"), # Older version
                os.path.join(program_files, r"Adobe\Reader 11.0\Reader\AcroRd32.exe")    # Older version
            ]
            sumatra_paths = [
                os.path.join(program_files, r"SumatraPDF\SumatraPDF.exe"),
                os.path.join(program_files_x86, r"SumatraPDF\SumatraPDF.exe")
            ]

            # Try Adobe Reader
            for adobe_path in adobe_reader_paths:
                if os.path.exists(adobe_path):
                    # Quote paths for command line using os.path.normpath for consistency
                    cmd = [f'"{os.path.normpath(adobe_path)}"', "/N", "/T", f'"{os.path.normpath(abs_pdf_path)}"', printer_name]
                    print(f"คำสั่ง Windows (Adobe Reader): {' '.join(cmd)}")
                    try:
                        subprocess.run(" ".join(cmd), shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน Adobe Reader)")
                        printed_successfully = True
                        break
                    except Exception as e:
                        print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (Adobe Reader): {e}")
                        continue
            
            if not printed_successfully:
                # Try SumatraPDF
                for sumatra_path in sumatra_paths:
                    if os.path.exists(sumatra_path):
                        # Quote paths for command line using os.path.normpath for consistency
                        cmd = [f'"{os.path.normpath(sumatra_path)}"', "-print-to", printer_name, f'"{os.path.normpath(abs_pdf_path)}"', "-silent"] # Added -silent
                        print(f"คำสั่ง Windows (SumatraPDF): {' '.join(cmd)}")
                        try:
                            subprocess.run(" ".join(cmd), shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name}' บน Windows เรียบร้อยแล้ว (ผ่าน SumatraPDF)")
                            printed_successfully = True
                            break
                        except Exception as e:
                            print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์ (SumatraPDF): {e}")
                            continue

        # --- Final Fallback for Windows if all silent methods fail or no printer_name ---
        if not printed_successfully:
            print(f"⚠️ ไม่สามารถสั่งพิมพ์แบบเงียบได้ หรือไม่มีชื่อเครื่องพิมพ์ที่ระบุ")
            print(f"   กำลังสั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' โดยเปิดกล่องโต้ตอบการพิมพ์ (โปรดกดพิมพ์ด้วยตนเอง)")
            try:
                # Ensure the path is quoted for os.startfile as well
                os.startfile(os.path.normpath(abs_pdf_path), "print") # os.startfile generally handles paths correctly without manual quoting, but normpath helps.
                print("✅ คำสั่งเปิดกล่องโต้ตอบการพิมพ์ถูกส่งแล้ว")
            except Exception as e:
                print(f"❌ ข้อผิดพลาดในการเปิดกล่องโต้ตอบการพิมพ์: {e}")
                print("   โปรดตรวจสอบการตั้งค่าโปรแกรมดู PDF เริ่มต้นและสิทธิ์การเข้าถึง")
                print("   หากปัญหายังคงอยู่: โปรดติดตั้งโปรแกรมดู PDF เช่น Adobe Reader หรือ SumatraPDF และตั้งค่าให้เป็นโปรแกรมเริ่มต้นสำหรับไฟล์ PDF")
                print("   หากปัญหายังคงอยู่: อาจจำเป็นต้องแก้ไขการเชื่อมโยงชนิดไฟล์ด้วยตนเองใน Windows หรือเรียกใช้สคริปต์ในฐานะผู้ดูแลระบบ")

    elif system in ("Darwin", "Linux"):  # Darwin = macOS
        try:
            print(f"Darwin Linux: {system}")
            if shutil.which("lp"):  # ใช้ `lp` หากมี (เพราะ lp รองรับ option ได้ดีกว่า lpr)
                cmd = ["lp"]
                if printer_name:
                    cmd.extend(["-d", printer_name])
                # เพิ่ม orientation สำหรับแนวตั้ง
                cmd.extend(["-o", "orientation-requested=4"])
                cmd.append(abs_pdf_path)
                print(f"คำสั่ง {system} (lp): {' '.join(cmd)}")
            else:
                cmd = ["lpr"]
                if printer_name:
                    cmd.extend(["-P", printer_name])
                cmd.append(abs_pdf_path)
                print(f"คำสั่ง {system} (lpr): {' '.join(cmd)}")

            subprocess.run(cmd, check=True)
            print(f"✅ สั่งพิมพ์ไฟล์ '{os.path.basename(abs_pdf_path)}' ไปยังเครื่องพิมพ์ '{printer_name if printer_name else 'default'}' บน {system} เรียบร้อยแล้ว")
            print("หากไม่เห็นงานพิมพ์ โปรดตรวจสอบคิวงานพิมพ์ของเครื่องพิมพ์")

        except subprocess.CalledProcessError as e:
            print(f"❌ ข้อผิดพลาดในการสั่งพิมพ์บน {system}: การเรียกใช้คำสั่งล้มเหลว. รหัสข้อผิดพลาด: {e.returncode}")
            print(f"   รายละเอียด: {e.stderr.decode('utf-8') if e.stderr else 'ไม่มี'}")
        except FileNotFoundError:
            print(f"❌ ข้อผิดพลาด: ไม่พบคำสั่ง 'lp' หรือ 'lpr'")
            print(f"   โปรดตรวจสอบว่า CUPS ถูกติดตั้งและตั้งค่าอย่างถูกต้องบน {system} ของคุณ")
        except Exception as e:
            print(f"❌ ข้อผิดพลาดที่ไม่คาดคิดในการสั่งพิมพ์บน {system}: {e}")
            print("   โปรดตรวจสอบการตั้งค่าเครื่องพิมพ์และสิทธิ์การเข้าถึง")
            
def run_special_request_if_exists():
    request_path = "request_special.py"
    print(f"ℹ Checking {request_path}")
    log_request_message(f"ℹ Checking for {request_path}")
    
    if os.path.exists(request_path):
        print(f"..{request_path} found, running special_request()...")
        log_request_message(f"..{request_path} found. Attempting to run special_request()")

        spec = importlib.util.spec_from_file_location("request", request_path)
        request_module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(request_module)
            if hasattr(request_module, 'special_request'):
                try:
                    request_module.special_request()
                    log_request_message("..special_request() executed successfully.")
                except Exception as inner_e:
                    error_msg = f"❌ Error inside special_request(): {inner_e}"
                    print(error_msg)
                    log_request_message(error_msg)
                    log_request_message(traceback.format_exc())
            else:
                warning = f"⚠️  special_request() not found in {request_path}"
                print(warning)
                log_request_message(warning)
        except Exception as e:
            error_msg = f"❌ Error loading {request_path}: {e}"
            print(error_msg)
            log_request_message(error_msg)
            log_request_message(traceback.format_exc())
        finally:
            try:
                os.remove(request_path)
                print(f"..{request_path} has been deleted after execution.")
                log_request_message(f"..{request_path} has been deleted after execution.")
            except Exception as e:
                delete_error = f"⚠️  Failed to delete {request_path}: {e}"
                print(delete_error)
                log_request_message(delete_error)
    else:
        msg = f"..{request_path} not found, skipping special_request."
        print(msg)
        log_request_message(msg)


def run_routine_request_if_exists():
    request_path = "request_routine.py"
    print(f"ℹ Checking {request_path}")
    log_request_message(f"ℹ Checking for {request_path}")
    
    if os.path.exists(request_path):
        print(f"..{request_path} found, running routine_request()...")
        log_request_message(f"..{request_path} found. Attempting to run routine_request()")

        spec = importlib.util.spec_from_file_location("request", request_path)
        request_module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(request_module)
            if hasattr(request_module, 'routine_request'):
                try:
                    request_module.routine_request()
                    log_request_message("..routine_request() executed successfully.")
                except Exception as inner_e:
                    error_msg = f"❌ Error inside routine_request(): {inner_e}"
                    print(error_msg)
                    log_request_message(error_msg)
                    log_request_message(traceback.format_exc())
            else:
                warning = f"⚠️  routine_request() not found in {request_path}"
                print(warning)
                log_request_message(warning)
        except Exception as e:
            error_msg = f"❌ Error loading {request_path}: {e}"
            print(error_msg)
            log_request_message(error_msg)
            log_request_message(traceback.format_exc())

    else:
        msg = f"ℹ️  {request_path} not found, skipping routine_request."
        print(msg)
        log_request_message(msg)