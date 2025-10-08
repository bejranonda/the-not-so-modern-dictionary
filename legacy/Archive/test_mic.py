import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # ตรวจสอบจำนวนไมโครโฟนที่เชื่อมต่อ
    mic_list = sr.Microphone.list_microphone_names()
    if len(mic_list) == 0:
        print("ไม่พบไมโครโฟน")
        return

    print("ไมโครโฟนที่เชื่อมต่อ:")
    for i, mic_name in enumerate(mic_list):
        print(f"{i + 1}. {mic_name}")

    print("\nกำลังทดสอบไมโครโฟน... กรุณาพูดอะไรบางอย่าง")

    # ใช้ไมโครโฟนแรกในการทดสอบ
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("รอฟังเสียง... กรุณาพูด")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="th-TH")
            print(f"คุณพูดว่า: {text}")
        except sr.UnknownValueError:
            print("!! ฟังไม่เข้าใจเสียงที่พูด")
        except sr.RequestError as e:
            print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# เรียกใช้งานการทดสอบ
test_microphone()
