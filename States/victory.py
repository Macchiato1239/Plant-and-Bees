from States.gameover import GameOverState


class VictoryState(GameOverState):
    def __init__(self, window):
        super().__init__(window, "Victory!")
