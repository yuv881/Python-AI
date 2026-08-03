import os
import platform
import webbrowser
import psutil
from speech_engine import speak


def is_windows_desktop():
    if os.getenv("ALLOW_SERVER_FEATURES", "false").lower() == "true":
        return True
    return platform.system() == "Windows"


def desktop_only_message(action="control apps"):
    speak(f"I can only {action} when running on a local Windows PC, not on the live server.")


def close_app(query):
    if not is_windows_desktop():
        desktop_only_message("close apps")
        return

    app_process_map = {
        "calculator": ["calculatorapp.exe", "calculator.exe", "calc.exe"],
        "calc": ["calculatorapp.exe", "calculator.exe", "calc.exe"],
        "notepad": ["notepad.exe"],
        "paint": ["mspaint.exe", "paint.exe", "pbrush.exe"],
        "cmd": ["cmd.exe"],
        "command prompt": ["cmd.exe"],
        "edge": ["msedge.exe"],
        "browser": ["msedge.exe", "chrome.exe"],
        "chrome": ["chrome.exe"]
    }

    target_procs = app_process_map.get(query, [])
    closed = False

    try:
        for proc in psutil.process_iter(['name']):
            try:
                pname = proc.info['name'].lower()
                if (target_procs and pname in target_procs) or (query and len(query) > 2 and query in pname):
                    proc.kill()
                    closed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception:
        speak("Could not access process list.")
        return

    if closed:
        speak(f"Closed {query}.")
    else:
        speak(f"{query} is not running.")


def open_app(query):
    web_sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "gmail": "https://mail.google.com",
        "github": "https://www.github.com"
    }

    if query in web_sites:
        url = web_sites[query]
        if is_windows_desktop():
            webbrowser.open(url)
            speak(f"Opened {query}.")
        else:
            speak(f"You can open {query} here: {url}")
        return

    if not is_windows_desktop():
        desktop_only_message("open desktop apps")
        return

    open_cmd_map = {
        "calculator": "calc",
        "calc": "calc",
        "notepad": "notepad",
        "paint": "mspaint",
        "cmd": "cmd",
        "command prompt": "cmd",
        "edge": "msedge",
        "browser": "msedge",
        "chrome": "chrome"
    }

    target = open_cmd_map.get(query, query)
    try:
        os.system(f"start {target}")
        speak(f"Opened {query}.")
    except Exception:
        speak(f"Could not open {query}.")


def handle_app_command(command):
    command = command.lower().strip()

    close_keywords = ["close", "clothes", "shut", "stop", "kill", "terminate"]
    open_keywords = ["open", "launch", "start", "run"]

    is_close = any(kw in command for kw in close_keywords)

    query = command
    for kw in close_keywords + open_keywords + ["the", "app", "application"]:
        query = query.replace(kw, "")
    query = query.strip()

    if not query:
        speak("Please specify an app to control.")
        return

    if is_close:
        close_app(query)
    else:
        open_app(query)

