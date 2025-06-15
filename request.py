### request.py

import subprocess
from datetime import datetime

def special_request():
    """คำสั่งพิเศษในการพิมพ์"""

    def log(message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("request_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")    

    print("🔧 Running special request...")
    log("🔧 Running special request...")

    ############################
    ## First Request
    if True :
        cmd1 = ['lp', '-d', 'Canon_LBP121_122', '-o', 'orientation-requested=4', '/Users/user/Documents/DictApp/SlangLuckyNo3.pdf']
        print(f"Request1: {' '.join(cmd1)}")
        log(f"🔧 cmd1: {' '.join(cmd1)}")

        try:
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
            print("✅ Request1 success")
            log(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request1 error: {e}")
            log(f"❌ Request1 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request1: {e}")
            log(f"❌ Unexpected error in Request1: {e}")



    ############################
    ## Third Request
    if False :
        cmd3 = ['cmd', '/c', 'dir']
        #cmd3 = ['ls', '-la']
        print(f"Request3: {' '.join(cmd3)}")
        log(f"🔧 cmd3: {' '.join(cmd3)}")

        try:
            output = subprocess.run(cmd3, check=True, capture_output=True, text=True)
            print("✅ Request1 success")
            log(f"✅ Request1 success\nstdout:\n{output.stdout}\nstderr:\n{output.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Request1 error: {e}")
            log(f"❌ Request1 error: {e}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error in Request1: {e}")
            log(f"❌ Unexpected error in Request1: {e}")