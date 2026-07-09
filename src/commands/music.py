
import webbrowser

from src.tts.tts_engine import speak


def play_pandora():
    speak("Playing music, Master Wayne.")
    webbrowser.open("www.pandora.com")

def play_spotify():
    speak("Playing music, Master Wayne.")
    webbrowser.open("www.spotify.com")