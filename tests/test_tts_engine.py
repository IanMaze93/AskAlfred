import subprocess

import src.tts.tts_engine as tts_engine


def test_speak_falls_back_when_voice_model_missing(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(tts_engine, "VOICE_MODEL", tmp_path / "missing-model.onnx")

    tts_engine.speak("Testing fallback")

    output = capsys.readouterr().out
    assert "Missing Piper voice model" in output
    assert "Alfred: Testing fallback" in output


def test_speak_runs_piper_and_aplay(monkeypatch, tmp_path):
    model = tmp_path / "voice.onnx"
    model.write_text("model")
    audio_output = tmp_path / "audio" / "alfred_response.wav"
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append((cmd, kwargs))
        return None

    monkeypatch.setattr(tts_engine, "VOICE_MODEL", model)
    monkeypatch.setattr(tts_engine, "AUDIO_OUTPUT", audio_output)
    monkeypatch.setattr(tts_engine.subprocess, "run", fake_run)

    tts_engine.speak("Good evening")

    assert audio_output.parent.exists()
    assert calls[0][0] == [
        "piper",
        "--model",
        str(model),
        "--output_file",
        str(audio_output),
    ]
    assert calls[0][1]["input"] == "Good evening"
    assert calls[0][1]["text"] is True
    assert calls[0][1]["check"] is True
    assert calls[1][0] == ["aplay", str(audio_output)]
    assert calls[1][1]["check"] is True


def test_speak_falls_back_when_subprocess_fails(monkeypatch, capsys, tmp_path):
    model = tmp_path / "voice.onnx"
    model.write_text("model")
    audio_output = tmp_path / "audio" / "alfred_response.wav"

    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(returncode=1, cmd=args[0])

    monkeypatch.setattr(tts_engine, "VOICE_MODEL", model)
    monkeypatch.setattr(tts_engine, "AUDIO_OUTPUT", audio_output)
    monkeypatch.setattr(tts_engine.subprocess, "run", fake_run)

    tts_engine.speak("Fallback on failure")

    output = capsys.readouterr().out
    assert "Piper TTS failed:" in output
    assert "Alfred: Fallback on failure" in output
