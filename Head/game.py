from Head.module_window import Window
from Head.states import State
from States.gameflow import GameFlow
from States.pause import PausedState
from States.menu import MenuState
from States.victory import VictoryState
from States.lose import LostState
import tkinter as tk

class Game:
    def __init__(self) -> None:
        self.__window_object=Window()
        self.__window=self.__window_object.window
        # === Pass this to the other states ===
        self.__state=State.MENU
        self.__game=None 
        
        self.__pause=PausedState(self.__window_object) #To be executed while state is paused
        self.__menu=MenuState(self.__window_object)
        self.__difficulty=self.__menu.difficulty
        self.__victory=VictoryState(self.__window_object)
        self.__lose=LostState(self.__window_object)

        '''Binding input events to input source'''
        self.__window.bind("<KeyPress>", self.toggle_pause, add="+")
        self.__window.bind("<KeyPress>", self.quit, add="+")

        # Canvas-local coordinates match the coordinates used by button hit tests.
        self.__window_object.canva.bind("<Button-1>", self.click_manager)



    def click_manager(self, event: tk.Event) -> str:
        '''Handle actions happening within the main menu'''
        if self.__state == State.MENU:
            # === If state is menu, the menu handles all input events ===
            action = self.__menu.handle_click(event)
            if action == "play":

                # ===Enter the main gameplay===

                self.__difficulty = self.__menu.difficulty
                self.__menu.exit()
                self.__start_game()

            elif action == "difficulty":
                # === Cycle through all difficulty settings ===
                self.__menu.cycle_difficulty()

            elif action == "quit":
                # === Quit the game ===
                self.__window.destroy()

            return "break"

        if self.__state == State.PLAYING:
            # === If state is playing, the main game handles all input events ===
            if self.__game is not None:
                self.__game.handle_click(event)
            return "break"

        if self.__state == State.PAUSED:
            # === If state is paused, the pause menu handles all input events ===
            action = self.__pause.handle_click(event)

        elif self.__state == State.LOST:
            # === If state is lost, the lost menu handles all input events ===
            action = self.__lose.handle_click(event)

        elif self.__state == State.VICTORY:
            # === If state is victory, the victory menu handles all input events ===
            action = self.__victory.handle_click(event)

        else:
            return

        if action == "resume":
            # === Available during the pause menu, swtich from pause state to playing state ===
            self.__pause.exit()
            self.__state = State.PLAYING
            self.__game.enter()

        elif action == "menu":
            # === Available during the pause, victory and lost menu, swtich from pause state to menu state ===
            self.__return_to_menu()

        elif action == "restart":
            # === Available during the pause, victory and lost menu,
            # destroy all game bindings, attributes and reset them to default ===
            if self.__game is not None:
                self.__game.cleanup()
            self.__pause.exit()
            self.__lose.exit()
            self.__victory.exit()
            self.__start_game()

        return "break"

    def __start_game(self) -> None:
        '''Start the main game flow'''
        self.__state = State.PLAYING
        self.__game = GameFlow(
            self.__window_object, self.__difficulty, self.finish_game
        )
        self.__game.create_game_loop()

    def __return_to_menu(self) -> None:
        '''Exit from all states and switch to menu state'''
        if self.__game is not None:
            self.__game.cleanup()
            self.__game = None
        self.__lose.exit()
        self.__victory.exit()
        self.__pause.exit()
        self.__state = State.MENU
        self.__menu.enter()


    def toggle_pause(self, event: tk.Event) -> None:
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

    def finish_game(self, result: State) -> None:
        '''Entering a gameover state if the gameplay has been concluded (player won or lost)'''
        if self.__state != State.PLAYING:
            return

        self.__state = result
        self.__game.exit()
        # === Exit the main game flow ===

        if result == State.LOST:
            self.__lose.enter()
            # === Disply losing menu ===
            
        elif result == State.VICTORY:
            self.__victory.enter()
            # === Display victory menu ===

    def start(self) -> None:
        '''Booting up the game'''
        self.__window_object.create_window()
        # === Build the main window ===
        self.__menu.enter()
        # === Entering the main menu first ===
        self.__window.mainloop()
        # === Start the loop thats check for input events ===

    def quit(self, event: tk.Event) -> None:
        '''Quit the game'''
        if event.keysym.lower() == "s":
            # === Destroy the main window ===
            self.__window.destroy()

        


