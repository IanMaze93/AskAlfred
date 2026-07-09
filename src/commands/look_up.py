
import webbrowser

from src.speech_recognition.recognizer import recognize_speech
from src.tts.tts_engine import speak


def look_up():
    speak("What is your question sir")
    # ask alfred your question
    query = recognize_speech().lower()
    speak("Displaying the results on the bat computer Master Wayne")
    # displays the search results from your default internet browser
    webbrowser.open(f"https://www.google.com/search?q={str(query)}")
            