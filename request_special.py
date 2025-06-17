### request_special.py

from input_slang_utils import speak_thai, speak_both
import subprocess
from datetime import datetime
import fitz  # PyMuPDF

def special_request():
    """คำสั่งพิเศษในการพิมพ์ จะรันครั้งเดียว แล้วลบไฟล์นี้ทิ้ง"""

    def log(message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("request_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")    

    print("🔧 Running special request...")
    log("🔧 Running special request...")

    speak_both("โอ้ว คอมพิวเตอร์พึ่งถูกแฮกไปเมื่อครู่<br>Oh,this computer was hacked just now!")
    
    ############################
    ## First Request
    if True :
        pdf_path = "output/slang_dictionary.pdf"
        partial_path = "output/slang_dictionary_partial.pdf"

        try:
            # ตรวจสอบจำนวนหน้าในไฟล์ PDF
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            doc.close()

            make_partial_pdf(
                input_pdf=pdf_path,
                output_pdf=partial_path,
                start_page=1,
                end_page=total_pages - 1  # หน้าแรกถึงก่อนสุดท้าย
            )


            if total_pages < 2:
                log("❗ Not enough pages to skip the last one.")
                return

            page_range = f"page-ranges=1-{total_pages - 1}"

            cmd1 = [
                'lp',
                '-d', 'Canon_LBP121_122',
                '-o', 'orientation-requested=4',
                '-o', 'number-up=9',
                partial_path
            ]

            print(f"Request1: {' '.join(cmd1)}")
            log(f"🔧 cmd1: {' '.join(cmd1)}")

            output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
            print("✅ Request1 success")
            log(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Request1 error: {e}")
            log(f"❌ Request1 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request1: {e}")
            log(f"❌ Unexpected error in Request1: {e}")

    ############################
    ## Second Request
    if True :
        cmd2 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/GreetingLuckyNo3.pdf']
        print(f"Request2: {' '.join(cmd2)}")
        log(f"🔧 cmd2: {' '.join(cmd2)}")

        try:
            output = subprocess.run(cmd2, check=True, capture_output=True, text=True)
            print("✅ Request2 success")
            log(f"✅ Request2 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request2 error: {e}")
            log(f"❌ Request2 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request2: {e}")
            log(f"❌ Unexpected error in Request2: {e}")



    ############################
    ## Third Request
    if True :
        #cmd3 = ['cmd', '/c', 'dir']
        cmd3 = ['ls', '-la', 'output']
        print(f"Request3: {' '.join(cmd3)}")
        log(f"🔧 cmd3: {' '.join(cmd3)}")

        try:
            output = subprocess.run(cmd3, check=True, capture_output=True, text=True)
            print("✅ Request3 success")
            log(f"✅ Request3 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request3 error: {e}")
            log(f"❌ Request3 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request3: {e}")
            log(f"❌ Unexpected error in Request3: {e}")
            
            
from PyPDF2 import PdfReader, PdfWriter
import os

def make_partial_pdf(input_pdf, output_pdf, start_page, end_page):
    # แยกหน้า
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):  # zero-based index
        writer.add_page(reader.pages[i])

    with open(output_pdf, "wb") as f:
        writer.write(f)