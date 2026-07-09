from datetime import datetime

from src.tts.tts_engine import speak


def tellDay():
    # get current datetime
    date_time = datetime.now()
    # Speak the day of the week
    speak("The day is " + date_time.strftime("%A"))


def tellTime():
    date_time = datetime.now()
    # convert time into speakable string
    print(date_time)
    currentTime = str(date_time.strftime("%I:%M %p"))
    speak("Master Wayne, the time is " + currentTime)
