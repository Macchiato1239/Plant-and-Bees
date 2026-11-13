from Head.states import GameState
from Manager.collision import CollisionManager
from Base.button import Button
class MenuState(GameState):
    '''Selecting mode to play'''
    def __init__(self, window):
        # === What will be here: Play, Difficulty, Quit===
        super().__init__(window)
        self.__canvas = self.window.canva
        self.__difficulty=1
        self.__collision=CollisionManager()

        # === Play Button ===
        self.__play_button=Button(self.__canvas, 500, 220, 200, 60, "Play")

        # === Difficulty Buttion ===
        self.__difficulty_button=Button(self.__canvas, 500, 310, 200, 60, "Difficulty: Normal")

        # === Quit Button ===
        self.__quit_button=Button(self.__canvas, 500, 400, 200, 60, "Quit")


    def enter(self):
        self.__canvas.itemconfig(self.__play_button.rect_id, state="normal")
        self.__canvas.itemconfig(self.__play_button.text, state="normal")

        self.__canvas.itemconfig(self.__difficulty_button.rect_id, state="normal")
        self.__canvas.itemconfig(self.__difficulty_button.text, state="normal")

        self.__canvas.itemconfig(self.__quit_button.rect_id, state="normal")
        self.__canvas.itemconfig(self.__quit_button.text, state="normal")

        self.__collision.interactive = [
            self.__play_button, self.__difficulty_button, self.__quit_button
        ]
        
    def exit(self):
        self.__canvas.itemconfig(self.__play_button.rect_id, state="hidden")
        self.__canvas.itemconfig(self.__play_button.text, state="hidden")

        self.__canvas.itemconfig(self.__difficulty_button.rect_id, state="hidden")
        self.__canvas.itemconfig(self.__difficulty_button.text, state="hidden")

        self.__canvas.itemconfig(self.__quit_button.rect_id, state="hidden")
        self.__canvas.itemconfig(self.__quit_button.text, state="hidden")

        self.__collision.interactive=[]

    def handle_click(self, event):
        x,y=event.x, event.y
        item=self.__collision.interactive_at(x,y)
        if item==self.__play_button:
            return "play"
        elif item==self.__difficulty_button:
            return "difficulty"
        elif item==self.__quit_button:
            return "quit"
        else:
            return None
    @property
    def difficulty(self):
        return self.__difficulty

    def cycle_difficulty(self):
        self.__difficulty = self.__difficulty % 3 + 1
        label = {1: "Normal", 2: "Hard", 3: "Insane"}[self.__difficulty]
        self.__difficulty_button.text = f"Difficulty: {label}"
