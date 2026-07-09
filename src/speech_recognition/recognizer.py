import contextlib
import os

import speech_recognition

recognizer = speech_recognition.Recognizer()


@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        original_stderr = os.dup(2)
        try:
            os.dup2(devnull.fileno(), 2)
            yield
        finally:
            os.dup2(original_stderr, 2)
            os.close(original_stderr)


def find_microphone():
    names = speech_recognition.Microphone.list_microphone_names()

    for index, name in enumerate(names):
        if "headset" in name.lower():
            return index

    return None


def recognize_speech() -> str:
    try:
        with suppress_stderr():
            with speech_recognition.Microphone(device_index=find_microphone()) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                recognizer.pause_threshold = 1.5
                audio = recognizer.listen(
                    source,
                    timeout=15,
                    phrase_time_limit=10,
                )

        print("Recognizing...")
        return recognizer.recognize_google(audio, language="en-US")

    except speech_recognition.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except speech_recognition.UnknownValueError:
        print("Could not understand audio.")
        return ""

    except Exception as error:
        print(f"Speech recognition failed: {error}")
        return ""
