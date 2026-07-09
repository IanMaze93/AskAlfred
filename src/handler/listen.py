

from src.speech_recognition.recognizer import recognize_speech
from src.types.commands import Commands
from src.commands.look_up import look_up
from src.commands.music import play_pandora, play_spotify
from src.commands.goodby import say_goodbye
from src.commands.date_time import tellDay, tellTime
from src.commands.self import self
from src.commands.greeting import greeting
from src.tts.tts_engine import speak


def listen():
    greeting()

    # Continue to loop until command to shutdown
    while(True):
        try:
            query = recognize_speech()
            print(f"Recognized Query: {query}")
        except KeyboardInterrupt:
            say_goodbye()
            break

        if not query or query == "None":
            continue
        
        # Lower Case Queries work the best
        query = query.lower()
        print(f"Lower Case Query: {query}")

        if Commands.NAME.value in query:
            self()
            continue
        elif Commands.QUESTION.value in query:
            look_up()
            continue
        elif Commands.PANDORA.value in query:
            play_pandora()
            continue
        elif Commands.SPOTIFY.value in query:
            play_spotify()
            continue
        elif Commands.DATE.value in query:
            tellDay()
            continue
        elif Commands.TIME.value in query:
            tellTime()
            continue
        elif Commands.SHUTDOWN.value in query:
            say_goodbye()
            exit()

		