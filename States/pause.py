from States.gameover import GameOverState


class PausedState(GameOverState):
    def __init__(self, window):
        super().__init__(window, "Paused", include_resume=True)
