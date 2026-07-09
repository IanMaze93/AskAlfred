# Ask Alfred (Batman Fan Project)

Virtual Assistant Named Alfred created with python
![alt text](./images/ask_alfred.png)

An offline voice assistant written in Python that listens for spoken commands, responds with natural-sounding speech, and performs useful desktop tasks.

Inspired by the classic gentleman-butler archetype, Ask Alfred is a lightweight personal assistant built to explore speech recognition, text-to-speech, and modular command handling. The project serves as both a learning platform and a software engineering portfolio piece.

> **Status:** Active Development 🚧

---

## Features

- 🎤 Offline speech recognition
- 🗣️ Natural-sounding voice responses using Piper TTS
- ⚡ Modular command architecture
- 💬 Conversational command processing
- 📅 Date and time utilities
- 🌐 Web search support
- 🎵 Launch applications (Pandora, etc.)
- 🧩 Easy to extend with new commands
- 🐧 Linux development support
- ✅ Automated linting with Ruff and GitHub Actions

---

## Tech Stack

| Technology        | Purpose                |
| ----------------- | ---------------------- |
| Python 3.12       | Main language          |
| Poetry            | Dependency management  |
| SpeechRecognition | Speech-to-text         |
| PyAudio           | Microphone input       |
| Piper TTS         | Offline text-to-speech |
| Ruff              | Linting & formatting   |
| GitHub Actions    | CI/CD                  |

---

## Project Structure

```text
.
├── src/
│   ├── commands/              # Voice commands
│   ├── handler/               # Command dispatcher
│   ├── prompts/               # Prompt builders
│   ├── speechRecognition/     # Speech recognition
│   ├── speechGeneration/      # Piper TTS
│   ├── audio/                 # Generated audio
│   ├── api/                   # API integrations
│   ├── types/                 # Shared types
│   └── tools/                 # Utility helpers
├── tests/
├── .github/
│   └── workflows/
├── app.py
├── pyproject.toml
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/IanMaze93/AskAlfred.git
cd AskAlfred
```

### Install Poetry

```bash
pipx install poetry
```

### Install Linux Dependencies

PyAudio requires PortAudio to be installed.

Ubuntu/Debian:

```bash
sudo apt-get update

sudo apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential
```

### Install Python Dependencies

```bash
poetry install
```

---

## Running Alfred

```bash
poetry run python app.py
```

Once started, Alfred will begin listening for voice commands.

---

## Example Commands

- "What time is it?"
- "What's today's date?"
- "Play Pandora"
- "Open Google"
- "Tell me a joke"
- "Who are you?"

Adding new commands only requires creating a new command module and registering it with the command handler.

---

## Development

### Lint

```bash
poetry run ruff check .
```

### Format

```bash
poetry run ruff format .
```

### Run Tests

```bash
poetry run pytest
```

---

## Continuous Integration

Every push and pull request automatically:

- Installs project dependencies
- Builds the project
- Runs Ruff linting
- Executes the test suite

---

## Roadmap

- [ ] AI conversation support
- [ ] Wake-word detection
- [ ] Conversation memory
- [ ] Calendar integration
- [ ] Weather commands
- [ ] Plugin architecture
- [ ] Smart home integrations
- [ ] Local LLM support
- [ ] Cross-platform packaging

---

## Why I Built This

Ask Alfred began as a way to learn how voice assistants work under the hood without relying on cloud services. Since then it has evolved into a modular Python application that combines speech recognition, offline text-to-speech, automation, and AI experimentation.

The long-term goal is to create a fully capable offline desktop assistant while maintaining clean architecture and easily extensible code.

---
