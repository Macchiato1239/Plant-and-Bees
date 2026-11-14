from States.gameover import GameOverState
import tkinter as tk

class PausedState(GameOverState):
    def __init__(self, window: tk.Tk):
        super().__init__(window, "Paused", include_resume=True)
