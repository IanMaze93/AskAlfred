from enum import Enum

class Commands(Enum):
    NAME = "tell me your name"
    QUESTION = "alfred i have a question"
    PANDORA = "alfred play pandora"
    SPOTIFY = "alfred play spotify"
    DATE = "alfred what's today"
    TIME = "alfred what time is it"
    SHUTDOWN = "alfred shutdown"
