import contextlib

import src.speech_recognition.recognizer as recognizer_module


def test_find_microphone_returns_headset_index(monkeypatch):
    monkeypatch.setattr(
        recognizer_module.speech_recognition.Microphone,
        "list_microphone_names",
        lambda: ["Built-in Mic", "USB Headset"],
    )

    assert recognizer_module.find_microphone() == 1


def test_find_microphone_returns_none_when_no_headset(monkeypatch):
    monkeypatch.setattr(
        recognizer_module.speech_recognition.Microphone,
        "list_microphone_names",
        lambda: ["Built-in Mic", "Webcam Mic"],
    )

    assert recognizer_module.find_microphone() is None


def test_recognize_speech_success(monkeypatch):
    events = []

    class FakeMicrophone:
        def __init__(self, device_index):
            events.append(("device_index", device_index))

        def __enter__(self):
            return "source"

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeRecognizer:
        pause_threshold = None

        def adjust_for_ambient_noise(self, source, duration):
            events.append(("ambient", source, duration))

        def listen(self, source, timeout, phrase_time_limit):
            events.append(("listen", source, timeout, phrase_time_limit))
            return "audio"

        def recognize_google(self, audio, language):
            events.append(("recognize", audio, language))
            return "alfred what time is it"

    monkeypatch.setattr(recognizer_module, "suppress_stderr", contextlib.nullcontext)
    monkeypatch.setattr(recognizer_module, "find_microphone", lambda: 3)
    monkeypatch.setattr(recognizer_module.speech_recognition, "Microphone", FakeMicrophone)
    monkeypatch.setattr(recognizer_module, "recognizer", FakeRecognizer())

    result = recognizer_module.recognize_speech()

    assert result == "alfred what time is it"
    assert events == [
        ("device_index", 3),
        ("ambient", "source", 1),
        ("listen", "source", 15, 10),
        ("recognize", "audio", "en-US"),
    ]


def test_recognize_speech_wait_timeout_returns_empty(monkeypatch):
    class FakeMicrophone:
        def __init__(self, device_index):
            pass

        def __enter__(self):
            return "source"

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeRecognizer:
        def adjust_for_ambient_noise(self, source, duration):
            pass

        def listen(self, source, timeout, phrase_time_limit):
            raise recognizer_module.speech_recognition.WaitTimeoutError()

    monkeypatch.setattr(recognizer_module, "suppress_stderr", contextlib.nullcontext)
    monkeypatch.setattr(recognizer_module, "find_microphone", lambda: None)
    monkeypatch.setattr(recognizer_module.speech_recognition, "Microphone", FakeMicrophone)
    monkeypatch.setattr(recognizer_module, "recognizer", FakeRecognizer())

    assert recognizer_module.recognize_speech() == ""


def test_recognize_speech_unknown_value_returns_empty(monkeypatch):
    class FakeMicrophone:
        def __init__(self, device_index):
            pass

        def __enter__(self):
            return "source"

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeRecognizer:
        def adjust_for_ambient_noise(self, source, duration):
            pass

        def listen(self, source, timeout, phrase_time_limit):
            return "audio"

        def recognize_google(self, audio, language):
            raise recognizer_module.speech_recognition.UnknownValueError()

    monkeypatch.setattr(recognizer_module, "suppress_stderr", contextlib.nullcontext)
    monkeypatch.setattr(recognizer_module, "find_microphone", lambda: None)
    monkeypatch.setattr(recognizer_module.speech_recognition, "Microphone", FakeMicrophone)
    monkeypatch.setattr(recognizer_module, "recognizer", FakeRecognizer())

    assert recognizer_module.recognize_speech() == ""


def test_recognize_speech_generic_error_returns_empty(monkeypatch):
    class FakeMicrophone:
        def __init__(self, device_index):
            pass

        def __enter__(self):
            return "source"

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeRecognizer:
        def adjust_for_ambient_noise(self, source, duration):
            pass

        def listen(self, source, timeout, phrase_time_limit):
            raise RuntimeError("microphone unavailable")

    monkeypatch.setattr(recognizer_module, "suppress_stderr", contextlib.nullcontext)
    monkeypatch.setattr(recognizer_module, "find_microphone", lambda: None)
    monkeypatch.setattr(recognizer_module.speech_recognition, "Microphone", FakeMicrophone)
    monkeypatch.setattr(recognizer_module, "recognizer", FakeRecognizer())

    assert recognizer_module.recognize_speech() == ""
