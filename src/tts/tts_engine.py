import subprocess
from pathlib import Path

VOICE_MODEL = Path("src/voices/en_US-lessac-medium.onnx")
AUDIO_OUTPUT = Path("src/audio/alfred_response.wav")


def speak(text: str) -> None:
    if not VOICE_MODEL.exists():
        print(f"Missing Piper voice model: {VOICE_MODEL}")
        print(f"Alfred: {text}")
        return

    AUDIO_OUTPUT.parent.mkdir(exist_ok=True)

    try:
        ## Convert text to speech using Piper and save to WAV file
        subprocess.run(
            [
                "piper",
                "--model",
                str(VOICE_MODEL),
                "--output_file",
                str(AUDIO_OUTPUT),
            ],
            input=text,
            text=True,
            check=True,
        )

        ## Play the generated WAV file
        subprocess.run(
            ["aplay", str(AUDIO_OUTPUT)],
            check=True,
        )

    except Exception as error:
        print(f"Piper TTS failed: {error}")
        print(f"Alfred: {text}")
