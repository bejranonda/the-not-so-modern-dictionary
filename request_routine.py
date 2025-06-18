### request_routine.py

from input_slang_utils import speak_thai, speak_both, log_request_message, print_pdf_file, make_foldable_jackpot
import subprocess
from datetime import datetime
import random
import fitz  # PyMuPDF



def routine_request():
    """คำสั่งพิเศษในการพิมพ์ จะรันเรื่อยที่เรียก ไม่มีการลบไฟล์นี้ทิ้ง"""
    
    output_path="output/slang_dictionary.pdf"
    
    print("⚙️ Running routine request...")
    log_request_message("⚙️ Running routine request...")
    
    got_jackpot = True

    # สร้าง lucky booklet ด้วยโอกาส 1 ใน 10
    jackpot_draw = random.randint(1, 100)
    print(f"🍀 jackpot_draw: {jackpot_draw}")
    log_request_message(f"🍀 jackpot_draw {jackpot_draw}")
    if jackpot_draw > 89:
        speak_both("ว้าว แจ๊กพอตแตกอีกแล้ว<br>Wow, someone hit the jackpot!")
        output_jackpot = output_path.replace(".pdf", "_jackpot.pdf")
        make_foldable_jackpot(input_path=output_path, output_path=output_jackpot)
        print(f"..You got jackpot: {output_jackpot}")
        log_request_message(f"..You got jackpot: {output_jackpot}")

        print(f"Printing: {output_jackpot}")
        print_pdf_file(output_jackpot)
        log_request_message(f" ⚙️ print_pdf_file: {output_jackpot}")
        greeting_lucky = "output/GreetingJackpot.pdf"
        print_pdf_file(greeting_lucky)
        print(f"Printing: {greeting_lucky}")
        log_request_message(f" ⚙️ print_pdf_file: {greeting_lucky}")
    else:
        print(f"..No Lucky Printing")
        log_request_message("..No Jackpot Printing")
        got_jackpot = False
            
    ############################
    ## First Request
    if (not got_jackpot) and True :
        # สร้าง lucky request ด้วยโอกาส 1 ใน 10
        request_draw = random.randint(1, 100)
        print(f"🍀 request_draw: {request_draw}")
        log_request_message(f"🍀 request_draw: {request_draw}")
        if request_draw > 90:
            speak_both("โอ้ มีบางสิ่งอยู่ในยามค่ำคืนที่นี่<br>Oh, when no one is here at all")
            print(f"..request_draw meets criteria")
            log_request_message(f"..request_draw meets criteria")
            
            cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/EverWonderBooklet.pdf']
            print(f"⚙️ Request1a: {' '.join(cmd1)}")
            log_request_message(f"⚙️ Request1a: {' '.join(cmd1)}")

            try:
                output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
                print("✅ Request1a success")
                log_request_message(f"✅ Request1a success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Request1a error: {e}")
                log_request_message(f"❌ Request1a error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            except Exception as e:
                print(f"❌ Unexpected error in Request1a: {e}")
                log_request_message(f"❌ Unexpected error in Request1a: {e}")

            # cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/EverWonderBooklet.pdf']
            # print(f"⚙️ Request1b: {' '.join(cmd1)}")
            # log_request_message(f"⚙️ Request1b: {' '.join(cmd1)}")

            # try:
                # output = subprocess.run(cmd1, check=True, capture_output=True, text=True)
                # print("✅ Request1b success")
                # log_request_message(f"✅ Request1b success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
            # except subprocess.CalledProcessError as e:
                # print(f"❌ Request1b error: {e}")
                # log_request_message(f"❌ Request1b error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            # except Exception as e:
                # print(f"❌ Unexpected error in Request1b: {e}")
                # log_request_message(f"❌ Unexpected error in Request1b: {e}")
        else:
            print(f"..request_draw not enough")
            log_request_message(f"..request_draw not enough")


    ############################
    ## Second Request
    if (not got_jackpot) and False :
        cmd2 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/GreetingLuckyNo3.pdf']
        print(f"Request2: {' '.join(cmd2)}")
        log_request_message(f"🔧 cmd2: {' '.join(cmd2)}")

        try:
            output = subprocess.run(cmd2, check=True, capture_output=True, text=True)
            print("✅ Request2 success")
            log_request_message(f"✅ Request2 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request2 error: {e}")
            log_request_message(f"❌ Request2 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request2: {e}")
            log_request_message(f"❌ Unexpected error in Request2: {e}")



    ############################
    ## Third Request
    if False :
        #cmd3 = ['cmd', '/c', 'dir']
        cmd3 = ['ls', '-la', 'output']
        print(f"Request3: {' '.join(cmd3)}")
        log_request_message(f"🔧 cmd3: {' '.join(cmd3)}")

        try:
            output = subprocess.run(cmd3, check=True, capture_output=True, text=True)
            print("✅ Request1 success")
            log_request_message(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request3 error: {e}")
            log_request_message(f"❌ Request3 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request3: {e}")
            log_request_message(f"❌ Unexpected error in Request3: {e}")
            
            