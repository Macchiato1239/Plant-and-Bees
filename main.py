from gameflow import GameFlow
class Game:
    def __init__(self):
        self.__gameflow=GameFlow()

    def play(self):
        self.__gameflow.create_game_loop()
game=Game()
game.play()