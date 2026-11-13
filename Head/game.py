from Head.module_window import Window
from Head.states import State
from States.gameflow import GameFlow
from States.pause import PausedState
from States.menu import MenuState
from States.victory import VictoryState
from States.lose import LostState
class Game:
    def __init__(self):
        self.__window_object=Window()
        self.__window=self.__window_object.window
        # === Pass this to the other states ===
        self.__state=State.MENU
        self.__game=None #To be executed while state is playing
        self.__pause=PausedState(self.__window_object) #To be executed while state is paused
        self.__menu=MenuState(self.__window_object)
        self.__victory=VictoryState(self.__window_object)
        self.__lose=LostState(self.__window_object)
        self.__window.bind("<KeyPress>", self.toggle_pause, add="+")
        self.__window.bind("<KeyPress>", self.quit, add="+")
        self.__window.bind("<Button-1>", self.menu_handler, add="+")



    def menu_handler(self, event):
        action=self.__menu.handle_click(event)
        if action == None:
            return
        if action == "play":
            difficulty=self.__menu.difficulty
            self.__state=State.PLAYING
            self.__menu.exit()
            self.__game=GameFlow(self.__window_object, difficulty, self.finish_game)
            self.__game.create_game_loop()

        elif action == "difficulty":
            self.__menu.cycle_difficulty()

        elif action == "quit":
            self.__window.destroy()

    def process_state(self):
        if self.__state==State.MENU:
            self.__menu.enter()


    def toggle_pause(self, event):
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

    def finish_game(self, result):
        if self.__state != State.PLAYING:
            return

        self.__state = result
        self.__game.exit()

        if result == State.LOST:
            self.__lose.enter()
        elif result == State.VICTORY:
            self.__victory.enter()

    def start(self):
        self.__window_object.create_window()
        self.__menu.enter()
        self.__window.mainloop()

    def quit(self, event):
        if event.keysym.lower() == "q":
            # === Quit the game ===
            self.__window.destroy()

        


