import speech_recognition as sr
import pyttsx3

import threading

_speech_buffer = []


def clear_speech_buffer():
    global _speech_buffer
    _speech_buffer = []


def get_speech_buffer():
    return list(_speech_buffer)


_tts_lock = threading.Lock()


def _play_speech_async(text):
    with _tts_lock:
        pythoncom_available = False
        try:
            import pythoncom
            import win32com.client
            pythoncom.CoInitialize()
            pythoncom_available = True
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(str(text))
        except Exception as e1:
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 150)
                engine.say(str(text))
                engine.runAndWait()
            except Exception as e2:
                # Silently catch TTS issues on headless/server hosts or concurrent calls
                pass
        finally:
            if pythoncom_available:
                try:
                    import pythoncom
                    pythoncom.CoUninitialize()
                except Exception:
                    pass


def speak(text, play_audio=True):
    print("Assistant:", text)
    _speech_buffer.append(text)
    if play_audio:
        # Run TTS in a background thread so the HTTP/API response returns instantly
        thread = threading.Thread(target=_play_speech_async, args=(text,), daemon=True)
        thread.start()




def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)

            print("You:", text)
            return text.lower()

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return ""

        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""
        except Exception:
            return ""

