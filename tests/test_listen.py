import builtins

import pytest

import src.handler.listen as listener


def _make_recognizer_stub(events):
    sequence = list(events)

    def _stub():
        value = sequence.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value

    return _stub


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("tell me your name", "self"),
        ("alfred i have a question", "look_up"),
        ("alfred play pandora", "play_pandora"),
        ("alfred play spotify", "play_spotify"),
        ("alfred what's today", "tellDay"),
        ("alfred what time is it", "tellTime"),
    ],
)
def test_listen_dispatches_to_expected_command(monkeypatch, query, expected):
    calls = []

    monkeypatch.setattr(listener, "greeting", lambda: calls.append("greeting"))
    monkeypatch.setattr(listener, "self", lambda: calls.append("self"))
    monkeypatch.setattr(listener, "look_up", lambda: calls.append("look_up"))
    monkeypatch.setattr(listener, "play_pandora", lambda: calls.append("play_pandora"))
    monkeypatch.setattr(listener, "play_spotify", lambda: calls.append("play_spotify"))
    monkeypatch.setattr(listener, "tellDay", lambda: calls.append("tellDay"))
    monkeypatch.setattr(listener, "tellTime", lambda: calls.append("tellTime"))
    monkeypatch.setattr(listener, "say_goodbye", lambda: calls.append("say_goodbye"))
    monkeypatch.setattr(
        listener,
        "recognize_speech",
        _make_recognizer_stub([query, KeyboardInterrupt()]),
    )

    listener.listen()

    assert "greeting" in calls
    assert expected in calls
    assert "say_goodbye" in calls


def test_listen_ignores_empty_or_none_queries(monkeypatch):
    calls = []

    monkeypatch.setattr(listener, "greeting", lambda: calls.append("greeting"))
    monkeypatch.setattr(listener, "self", lambda: calls.append("self"))
    monkeypatch.setattr(listener, "say_goodbye", lambda: calls.append("say_goodbye"))
    monkeypatch.setattr(
        listener,
        "recognize_speech",
        _make_recognizer_stub(["", "None", KeyboardInterrupt()]),
    )

    listener.listen()

    assert calls == ["greeting", "say_goodbye"]


def test_listen_shutdown_command_exits(monkeypatch):
    calls = []

    monkeypatch.setattr(listener, "greeting", lambda: calls.append("greeting"))
    monkeypatch.setattr(listener, "say_goodbye", lambda: calls.append("say_goodbye"))
    monkeypatch.setattr(
        listener,
        "recognize_speech",
        _make_recognizer_stub(["alfred shutdown"]),
    )

    def _exit():
        raise SystemExit

    monkeypatch.setattr(builtins, "exit", _exit)

    with pytest.raises(SystemExit):
        listener.listen()

    assert calls == ["greeting", "say_goodbye"]
