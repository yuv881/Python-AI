import os
import ctypes
import platform
import psutil
from datetime import datetime
from speech_engine import speak


def is_windows_desktop():
    return platform.system() == "Windows"


def desktop_only_message(action):
    speak(f"I can only {action} on the local Windows desktop version, not from the live Render server.")


def get_time():
    now = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}.")


def get_date():
    today = datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {today}.")


def get_battery():
    if not is_windows_desktop():
        desktop_only_message("check battery status")
        return

    try:
        battery = psutil.sensors_battery()
        if battery is None:
            speak("Could not read battery information.")
            return

        percent = battery.percent
        plugged = "plugged in" if battery.power_plugged else "not plugged in"
        speak(f"Your battery is at {percent} percent and is currently {plugged}.")
    except Exception as e:
        speak("Could not retrieve battery status.")


def change_volume(action):
    if not is_windows_desktop():
        desktop_only_message("change volume")
        return

    # VK_VOLUME_MUTE = 0xAD, VK_VOLUME_DOWN = 0xAE, VK_VOLUME_UP = 0xAF
    try:
        if action == "up":
            for _ in range(5):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            speak("Volume increased.")
        elif action == "down":
            for _ in range(5):
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            speak("Volume decreased.")
        elif action == "mute" or action == "unmute":
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            speak("Volume muted or unmuted.")
    except Exception:
        speak("Could not adjust volume.")


def lock_screen():
    if not is_windows_desktop():
        desktop_only_message("lock the screen")
        return

    speak("Locking your computer.")
    try:
        ctypes.windll.user32.LockWorkStation()
    except Exception:
        speak("Could not lock the screen.")


def open_folder(folder_name):
    if not is_windows_desktop():
        desktop_only_message("open folders")
        return

    user_home = os.path.expanduser("~")
    folders = {
        "downloads": os.path.join(user_home, "Downloads"),
        "desktop": os.path.join(user_home, "Desktop"),
        "documents": os.path.join(user_home, "Documents"),
        "pictures": os.path.join(user_home, "Pictures"),
        "music": os.path.join(user_home, "Music"),
        "videos": os.path.join(user_home, "Videos")
    }

    path = folders.get(folder_name.lower())
    if path and os.path.exists(path):
        os.startfile(path)
        speak(f"Opened {folder_name} folder.")
    else:
        speak(f"Folder {folder_name} not found.")
