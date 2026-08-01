import urllib.request
import urllib.parse
import json
import webbrowser
from speech_engine import speak


def google_search(query):
    query_clean = query.replace("search google for", "").replace("google search", "").replace("search", "").strip()
    if not query_clean:
        speak("What would you like me to search for on Google?")
        return
    url = f"https://www.google.com/search?q={urllib.parse.quote(query_clean)}"
    webbrowser.open(url)
    speak(f"Searching Google for {query_clean}.")


def youtube_search(query):
    query_clean = query.replace("search youtube for", "").replace("play on youtube", "").replace("youtube", "").strip()
    if not query_clean:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
        return
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query_clean)}"
    webbrowser.open(url)
    speak(f"Searching YouTube for {query_clean}.")


def wikipedia_search(query):
    query_clean = query.replace("wikipedia", "").replace("tell me about", "").replace("who is", "").replace("what is", "").strip()
    if not query_clean:
        speak("What topic should I look up on Wikipedia?")
        return

    formatted_query = query_clean.title().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(formatted_query)}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ShifraAssistant/1.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        
        extract = data.get('extract')
        if extract:
            # Speak first two sentences
            sentences = extract.split('. ')
            summary = '. '.join(sentences[:2])
            if not summary.endswith('.'):
                summary += '.'
            speak(summary)
        else:
            speak(f"Sorry, I couldn't find details on Wikipedia for {query_clean}.")
    except Exception:
        # Fallback to Google Search if Wikipedia summary not directly found
        google_search(query_clean)


def get_joke():
    try:
        req = urllib.request.Request("https://official-joke-api.appspot.com/random_joke", headers={'User-Agent': 'ShifraAssistant/1.0'})
        res = urllib.request.urlopen(req, timeout=3)
        data = json.loads(res.read().decode('utf-8'))
        setup = data.get("setup")
        punchline = data.get("punchline")
        if setup and punchline:
            speak(setup)
            speak(punchline)
            return
    except Exception:
        pass
    
    # Offline backup joke
    speak("Why don't scientists trust atoms? Because they make up everything!")
