import os
import django

# Initialize Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
except Exception:
    pass

from speech_engine import speak, listen
from command_handler import process_command


def run_cli():
    speak("Hello! I am Shifra, your voice assistant. How can I help you?")

    while True:
        command = listen()
        should_continue = process_command(command)
        if not should_continue:
            break


def main():
    run_cli()


if __name__ == "__main__":
    main()
