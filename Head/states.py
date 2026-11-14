from enum import Enum, auto
from abc import ABC, abstractmethod
import tkinter as tk
class State(Enum):
    '''States of the game'''
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    LOST = auto()
    VICTORY = auto()

# === Today i learnt about the finite state machine, it's quite a good way to manage states of a game ===
class GameState(ABC):
    '''Finite State Machine'''
    def __init__(self, window) -> None:
        self.__window=window

    @property
    def window(self) -> tk.Tk:
        return self.__window

    @abstractmethod
    def enter(self) -> None:
        '''Entering a new state'''
        pass

    @abstractmethod
    def exit(self) -> None:
        '''Exiting a state'''
        pass

    @abstractmethod
    def handle_click(self, event: tk.Tk):
        '''Handle all clicking events'''
        pass

