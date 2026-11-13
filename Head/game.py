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
        self.__difficulty=self.__menu.difficulty
        self.__victory=VictoryState(self.__window_object)
        self.__lose=LostState(self.__window_object)

        self.__window.bind("<KeyPress>", self.toggle_pause, add="+")
        self.__window.bind("<KeyPress>", self.quit, add="+")
        self.__window.bind("<Button-1>", self.menu_handler, add="+")



    def menu_handler(self, event):
        if self.__state == State.MENU:
            action = self.__menu.handle_click(event)
            if action == "play":
                self.__difficulty = self.__menu.difficulty
                self.__menu.exit()
                self.__start_game()
            elif action == "difficulty":
                self.__menu.cycle_difficulty()
            elif action == "quit":
                self.__window.destroy()
            return

        if self.__state == State.PAUSED:
            action = self.__pause.handle_click(event)
        elif self.__state == State.LOST:
            action = self.__lose.handle_click(event)
        elif self.__state == State.VICTORY:
            action = self.__victory.handle_click(event)
        else:
            return

        if action == "resume":
            self.__pause.exit()
            self.__state = State.PLAYING
            self.__game.enter()
        elif action == "menu":
            self.__return_to_menu()
        elif action == "restart":
            if self.__game is not None:
                self.__game.cleanup()
            self.__pause.exit()
            self.__lose.exit()
            self.__victory.exit()
            self.__start_game()

    def __start_game(self):
        self.__state = State.PLAYING
        self.__game = GameFlow(
            self.__window_object, self.__difficulty, self.finish_game
        )
        self.__game.create_game_loop()

    def __return_to_menu(self):
        if self.__game is not None:
            self.__game.cleanup()
            self.__game = None
        self.__lose.exit()
        self.__victory.exit()
        self.__pause.exit()
        self.__state = State.MENU
        self.__menu.enter()

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

        


