from module_window import Window
from gameflow import GameFlow
from pause import PausedState
from states import State
class Game:
    def __init__(self):
        self.__window_object=Window()
        self.__window=self.__window_object.window
        # === Pass this to the other states ===
        self.__state=State.PLAYING
        self.__game=GameFlow(self.__window_object) #To be executed while state is playing
        self.__pause=PausedState(self.__window_object) #To be executed while state is paused
        self.__window.bind("<KeyPress>", self.change_state, add="+")

    def change_state(self, event):
        # === Pause the game ===
        key = event.keysym.lower()
        if key == "r" and self.__state == State.PLAYING:
            self.__state=State.PAUSED
            self.__pause.enter()
            self.__game.exit()

        # === Continue the game ===
        elif key == "escape" or (key == "r" and self.__state == State.PAUSED):
            if self.__state==State.PAUSED:
                self.__state=State.PLAYING
                self.__pause.exit()
                self.__game.enter()


    def start(self):
        self.__game.create_game_loop()


        


