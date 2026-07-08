# Ask Alfred (Batman Fan Project)

Virtual Assistant Named Alfred created with python
![alt text](alfred.png)

## Setup

Install Poetry

```bash
pipx install poetry
```

On Linux, install system libraries required by `pyaudio` before running Poetry:

```bash
sudo apt-get update && sudo apt-get install -y portaudio19-dev
```

For voice output with `pyttsx3` on Linux, also install `espeak`:

```bash
sudo apt-get install -y espeak-ng libespeak1
```

## Installation

After cloning the repo, run the following command to install dependencies

```bash
poetry install
```

And to activate the environment

```bash
poetry env activate
```

## Run Code

```bash
poetry run python app.py
```

## Commands:

- "Tell me your name"
- "Alfred, I have a question" (Alfred will ask what your question is) -> Ask question -> answer displayed on screen
- "Alfred, Play Pandora" - (if signed into pandora, will open pandora on screen and start music)
- "Alfred, What Time is it?"
- "Alfred, What's today?"
- "Alfred Shutdown" (Ends program)
