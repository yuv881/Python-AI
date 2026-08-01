from speech_engine import speak
from app_controller import handle_app_command
from system_controller import get_time, get_date, get_battery, change_volume, lock_screen, open_folder
from web_controller import google_search, youtube_search, wikipedia_search, get_joke
from ai_controller import ask_ai


def process_command(command):
    if not command:
        return True

    command = command.lower().strip()

    if command in ["hii", "hello", "hey", "hey shifra"]:
        speak("Hello! How can I help you?")
        return True

    # Exit Intent
    if command in ["exit", "bye", "quit", "stop assistant", "goodbye"]:
        speak("Goodbye! Have a great day.")
        return False

    # AI Query Intent
    elif command.startswith("ask ai ") or command.startswith("ask shifra ") or command.startswith("ai "):
        prompt = command.replace("ask ai ", "").replace("ask shifra ", "").replace("ai ", "").strip()
        ask_ai(prompt)

    # Time & Date Intent
    elif "time" in command:
        get_time()

    elif "date" in command or "today" in command:
        get_date()

    # Battery Intent
    elif "battery" in command or "percentage" in command:
        get_battery()

    # Volume Control Intent
    elif "volume up" in command or "increase volume" in command:
        change_volume("up")

    elif "volume down" in command or "decrease volume" in command:
        change_volume("down")

    elif "mute" in command or "unmute" in command:
        change_volume("mute")

    # Screen Lock Intent
    elif "lock screen" in command or "lock pc" in command or "lock computer" in command:
        lock_screen()

    # Folder Opening Intent
    elif "open downloads" in command or "downloads folder" in command:
        open_folder("downloads")

    elif "open desktop" in command or "desktop folder" in command:
        open_folder("desktop")

    elif "open documents" in command or "documents folder" in command:
        open_folder("documents")

    elif "open pictures" in command or "pictures folder" in command:
        open_folder("pictures")

    # Joke Intent
    elif "joke" in command or "tell me a joke" in command:
        get_joke()

    # Wikipedia & Web Search Intent
    elif "wikipedia" in command:
        wikipedia_search(command)

    elif "youtube" in command:
        youtube_search(command)

    elif command.startswith("search") or "google" in command:
        google_search(command)

    elif command.startswith("who is") or command.startswith("what is") or command.startswith("explain") or command.startswith("tell me"):
        ask_ai(command)

    # General App Control or AI Fallback
    else:
        # Check if user is asking to open/close an app
        if any(kw in command for kw in ["open", "launch", "start", "run", "close", "shut", "stop", "kill"]):
            handle_app_command(command)
        else:
            ask_ai(command)

    return True

