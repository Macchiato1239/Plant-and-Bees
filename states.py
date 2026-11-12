from enum import Enum, auto
from abc import ABC, abstractmethod
from module_window import Window
class State(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    LOST = auto()
    VICTORY = auto()

# === Today i learnt about the finite state machine, it's quite a good way to manage states of a game ===
class GameState(ABC):
    '''Finite State Machine'''
    def __init__(self, window):
        self.__window=window

    @property
    def window(self):
        return self.__window

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

