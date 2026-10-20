import tkinter as tk
from rect import Rect

class Game:
    def __init__(self):
        self.__interactive = []       # UI collision check
        self.__taken = []    # Space taken by towers
        self.__window_width = 1000
        self.__window_height = 700
        self.__bg_color = "white"
        self.__window = tk.Tk()
        self.__running = True
        self.__canva = tk.Canvas(
            self.__window,
            width=self.__window_width,
            height=self.__window_height,
            bg=self.__bg_color
        )



    def create_game_loop(self):
        self.__window.geometry(
            f"{self.__window_width}x{self.__window_height}"
        )
        self.__canva.pack()
        self.__window.bind("<KeyPress>", self.on_key_press)
        self.__window.bind("<Button-1>", self.interaction_with_ui)
        self.game_loop()
        self.create_rect(10, 10, 100, 100, "black")
        self.__window.mainloop()

    def game_loop(self):
        if not self.__running:
            self.__window.destroy()
            return

        # Game logic goes here

        self.__window.after(16, self.game_loop)

    def on_key_press(self, event): #Shutting down the game
        if event.keysym == "q":
            print("Quitted")
            self.__running = False

    def get_click_cord(self, event): #Get coordinate of everyone click on the screen
        a=(f"X: {event.x}, Y: {event.y}")
        print(a)
        return event.x, event.y

    def create_rect(self, x1, y1, x2, y2, fill="red"):

        rect=Rect(x1, y1, x2, y2, fill)
        rect.render(self.__canva)
        self.__interactive.append(rect)
        return rect


    def interaction_with_ui(self, event):
        x,y=self.get_click_cord(event)
        for i in self.__interactive:
            if i.x1<x<i.x2 and i.y1<y<i.y2:
                print(f"Interactive clicked, it's {i.fill}")
                return True


        
        



game = Game()
game.create_game_loop()

    
# def on_click(event):
#     print(f"X: {event.x}, Y: {event.y}")



# soldier=tower.single_dps_Tower(100, 50, 10, 50, 10)
# inventory=slots.Inventory(canvas)
# inventory.add_tower(soldier)
# inventory.render()
# #Each element has a rect
