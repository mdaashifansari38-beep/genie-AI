import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import datetime
import os
import screen_brightness_control as sbc
import wikipedia
import time
import urllib.parse
import tkinter as tk
import threading
import ctypes

# ================= CONTACT LIST =================
contacts = {
    "mummy": "+916299315726",
    "aman": "+917667848976",
    "abbu": "+919111111111"
}

# ================= VOICE SETUP =================
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        print("🤖 Genie AI:", text)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Speech error:", e)

# ================= LISTEN =================
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🔊 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        speak("Sorry, I can't understand")
        return ""

# ================= WIKIPEDIA =================
def wiki_search(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Sorry, not found on Wikipedia")

# ================= SYSTEM =================
def close_app():
    pyautogui.hotkey("alt", "f4")
    return "Closed app"

# ================= NEW FEATURES =================
def shutdown_pc():
    speak("Shutting down system")
    os.system("shutdown /s /t 1")

def lock_screen():
    speak("Locking screen")
    ctypes.windll.user32.LockWorkStation()

def brightness_up():
    try:
        b = sbc.get_brightness()[0]
        sbc.set_brightness(min(b + 10, 100))
        speak("Brightness increased")
    except:
        speak("Brightness error")

def brightness_down():
    try:
        b = sbc.get_brightness()[0]
        sbc.set_brightness(max(b - 10, 0))
        speak("Brightness decreased")
    except:
        speak("Brightness error")

def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")
    speak("Volume increased")

def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")
    speak("Volume decreased")

def take_screenshot():
    try:
        filename = f"screenshot_{int(time.time())}.png"
        path = os.path.join(os.path.expanduser("~"), "Pictures", filename)
        pyautogui.screenshot(path)
        speak("Screenshot saved in Pictures folder")
    except:
        speak("Screenshot failed")

# ================= OPEN APPS =================
def open_app(command):
    if "chrome" in command:
        webbrowser.open("https://www.google.com")

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")

    elif "notepad" in command:
        os.system("notepad")

    elif "calculator" in command:
        os.system("calc")

    elif "vs code" in command:
        os.system("code")

    else:
        speak("App not found")

# ================= WHATSAPP =================
def send_whatsapp_by_name(command):
    try:
        parts = command.split("to")
        name_part = parts[1].strip()

        name = name_part.split(" ")[0]
        message = name_part.replace(name, "").strip()

        if name not in contacts:
            speak("Contact not found")
            return

        number = contacts[name]
        encoded_msg = urllib.parse.quote(message)

        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}"

        speak(f"Sending message to {name}")
        webbrowser.open(url)

        time.sleep(10)
        pyautogui.press("enter")

        speak("Message sent")

    except Exception as e:
        print(e)
        speak("Error sending message")

# ================= MAIN =================
def run_genie():
    speak("Hello sir, I am your Genie AI. Tell me what can I do for you")

    while True:
        command = listen()

        if command == "":
            continue

        time.sleep(0.5)

        if "exit" in command:
            speak("Goodbye sir, have a nice day")
            break

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak("Time is " + current_time)

        elif "what" in command or "why" in command or "how" in command or "who" in command:
            query = command.replace("what", "").replace("why", "").replace("how", "").replace("who", "").strip()
            wiki_search(query)

        elif "open" in command:
            open_app(command)

        elif "close" in command:
            speak(close_app())

        elif "send message" in command:
            send_whatsapp_by_name(command)

        elif "play" in command:
            query = command.replace("play", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            speak("Playing on YouTube")

        elif "search" in command:
            query = command.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak("Searching")

        # ===== NEW COMMANDS =====
        elif "shutdown" in command:
            shutdown_pc()

        elif "lock" in command:
            lock_screen()

        elif "brightness up" in command:
            brightness_up()

        elif "brightness down" in command:
            brightness_down()

        elif "volume up" in command:
            volume_up()

        elif "volume down" in command:
            volume_down()

        elif "screenshot" in command or "screen shot" in command:
            take_screenshot()

        elif "click" in command:
            pyautogui.click()
            speak("Click done")

        elif "type" in command:
            text = command.replace("type", "").strip()
            pyautogui.write(text)
            speak("Typing done")

        else:
            speak("Sorry, I can't understand")

# ================= GUI =================
def start_genie():
    t = threading.Thread(target=run_genie)
    t.daemon = True
    t.start()

def stop_app():
    root.destroy()

root = tk.Tk()
root.title("Genie AI")
root.geometry("300x200")

start_btn = tk.Button(root, text="Start Genie", font=("Arial", 14), bg="green", fg="white", command=start_genie)
start_btn.pack(pady=40)

stop_btn = tk.Button(root, text="Stop", font=("Arial", 12), bg="red", fg="white", command=stop_app)
stop_btn.pack()

root.mainloop()