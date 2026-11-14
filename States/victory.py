from States.gameover import GameOverState
import tkinter as tk

class VictoryState(GameOverState):
    def __init__(self, window: tk.Tk):
        super().__init__(window, "Victory!")
