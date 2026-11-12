from Head.states import GameState
class PausedState(GameState):
    def __init__(self, window):
        super().__init__(window)
        self.__canvas = self.window.canva
        self.__text = self.__canvas.create_text(
            400, 100,
            text = "Paused",
            fill = "black",
            font = ("Arial", 30),
            state = "hidden"
        )

    def exit(self):
        self.__canvas.itemconfig(self.__text, state = "hidden")

    def enter(self):
        self.__canvas.itemconfig(self.__text, state = "normal")
