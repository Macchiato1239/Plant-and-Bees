from States.gameover import GameOverState


class LostState(GameOverState):
    def __init__(self, window):
        super().__init__(window, "Game Over")
