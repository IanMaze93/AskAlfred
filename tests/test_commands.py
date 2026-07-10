from datetime import datetime

import src.commands.date_time as date_time
import src.commands.goodby as goodbye
import src.commands.greeting as greeting
import src.commands.look_up as look_up
import src.commands.music as music
import src.commands.self as self_command


def test_greeting_calls_speak(monkeypatch):
    calls = []
    monkeypatch.setattr(greeting, "speak", lambda text: calls.append(text))

    greeting.greeting()

    assert calls == ["Hello, Master Wayne. How can I assist you today?"]


def test_self_calls_speak(monkeypatch):
    calls = []
    monkeypatch.setattr(self_command, "speak", lambda text: calls.append(text))

    self_command.self()

    assert calls == ["I am Alfred, your virtual assistant."]


def test_say_goodbye_calls_speak(monkeypatch):
    calls = []
    monkeypatch.setattr(goodbye, "speak", lambda text: calls.append(text))

    goodbye.say_goodbye()

    assert calls == ["Goodbye, Master Wayne. Have a great day!"]


def test_tell_day_speaks_weekday(monkeypatch):
    calls = []
    monkeypatch.setattr(date_time, "speak", lambda text: calls.append(text))

    class FakeDateTime:
        @staticmethod
        def now():
            return datetime(2026, 7, 10, 10, 30, 0)

    monkeypatch.setattr(date_time, "datetime", FakeDateTime)

    date_time.tellDay()

    assert calls == ["The day is Friday"]


def test_tell_time_speaks_formatted_time(monkeypatch):
    calls = []
    monkeypatch.setattr(date_time, "speak", lambda text: calls.append(text))

    class FakeDateTime:
        @staticmethod
        def now():
            return datetime(2026, 7, 10, 17, 5, 0)

    monkeypatch.setattr(date_time, "datetime", FakeDateTime)

    date_time.tellTime()

    assert calls == ["Master Wayne, the time is 05:05 PM"]


def test_look_up_prompts_and_opens_google(monkeypatch):
    spoken = []
    opened = []

    monkeypatch.setattr(look_up, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(look_up, "recognize_speech", lambda: "What is Python")
    monkeypatch.setattr(look_up.webbrowser, "open", lambda url: opened.append(url))

    look_up.look_up()

    assert spoken == [
        "What is your question sir",
        "Displaying the results on the bat computer Master Wayne",
    ]
    assert opened == ["https://www.google.com/search?q=what is python"]


def test_play_pandora_speaks_and_opens(monkeypatch):
    spoken = []
    opened = []

    monkeypatch.setattr(music, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(music.webbrowser, "open", lambda url: opened.append(url))

    music.play_pandora()

    assert spoken == ["Playing music, Master Wayne."]
    assert opened == ["www.pandora.com"]


def test_play_spotify_speaks_and_opens(monkeypatch):
    spoken = []
    opened = []

    monkeypatch.setattr(music, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(music.webbrowser, "open", lambda url: opened.append(url))

    music.play_spotify()

    assert spoken == ["Playing music, Master Wayne."]
    assert opened == ["www.spotify.com"]
