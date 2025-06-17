### request_routine.py

from input_slang_utils import speak_thai, speak_both
import subprocess
from datetime import datetime
import fitz  # PyMuPDF
import random

def routine_request():
    """คำสั่งพิเศษในการพิมพ์ จะรันเรื่อยที่เรียก ไม่มีการลบไฟล์นี้ทิ้ง"""

    def log(message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("request_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")    

    print("⚙️ Running routine request...")
    log("⚙️ Running routine request...")

    ############################
    ## First Request
    if True :
        # สร้าง lucky request ด้วยโอกาส 1 ใน 10
        request_draw = random.randint(1, 100)
        print(f"🍀 request_draw: {request_draw}")
        log(f"🍀 request_draw: {request_draw}")
        if request_draw > 80:
            speak_both("โอ้ มีบางสิ่งอยู่ในยามค่ำคืนที่นี่<br>Oh, when no one is here at all")
            print(f"..request_draw meets criteria")
            log(f"..request_draw meets criteria")
            
            cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/EverWonderContent.pdf']
            print(f"⚙️ Request1a: {' '.join(cmd1)}")
            log(f"⚙️ Request1a: {' '.join(cmd1)}")

            try:
                output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
                print("✅ Request1a success")
                log(f"✅ Request1a success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Request1a error: {e}")
                log(f"❌ Request1a error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            except Exception as e:
                print(f"❌ Unexpected error in Request1a: {e}")
                log(f"❌ Unexpected error in Request1a: {e}")

            cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/EverWonderP1.pdf']
            print(f"⚙️ Request1b: {' '.join(cmd1)}")
            log(f"⚙️ Request1b: {' '.join(cmd1)}")

            try:
                output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
                print("✅ Request1b success")
                log(f"✅ Request1b success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Request1b error: {e}")
                log(f"❌ Request1b error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            except Exception as e:
                print(f"❌ Unexpected error in Request1b: {e}")
                log(f"❌ Unexpected error in Request1b: {e}")
        else:
            print(f"..request_draw not enough")
            log(f"..request_draw not enough")


    ############################
    ## Second Request
    if False :
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
    if False :
        #cmd3 = ['cmd', '/c', 'dir']
        cmd3 = ['ls', '-la', 'output']
        print(f"Request3: {' '.join(cmd3)}")
        log(f"🔧 cmd3: {' '.join(cmd3)}")

        try:
            output = subprocess.run(cmd3, check=True, capture_output=True, text=True)
            print("✅ Request1 success")
            log(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request3 error: {e}")
            log(f"❌ Request3 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request3: {e}")
            log(f"❌ Unexpected error in Request3: {e}")
            
            