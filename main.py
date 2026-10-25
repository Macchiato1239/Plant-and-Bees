import tkinter as tk
from rect import Rect
import hotbar
import module_tower
import enemy
class Game:
    def __init__(self):
        '''Window property'''
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
        '''Game play properties'''
        self.__base_health=100
        self.__spawn=[]
        self.__active_enemies=[]
        self.__starting_money=600
        self.__money=self.__starting_money
        
        '''
        self.__spawn is a collection of coordinate for enemy to spawn in, one by one, never many at once
        For i in self.__spawn:
            With the cord of the spawn, we can spawn enemy in the middle of the spawn's rect
            
        '''


        '''Hot Bar Properties'''
        self.__hotbar_slot_x1=50
        self.__hotbar_slot_width=130
        self.__hotbar_slot_y1=550
        self.__hotbar_slot_height=700
        self.__hotbar={}
        self.__empty_slot_color="black"
        self.__filled_slot_color="red"



        '''Tower properties'''
        self.__equipped_towers=[]
        self.__max_towers=5

        self.__current_tower=None
        self.__current_tower_signal=self.create_rect(0, 0, 30, 30, "red")
        
    def create_game_loop(self):
        self.__window.geometry(
            f"{self.__window_width}x{self.__window_height}"
        )
        self.__canva.pack()
        self.__window.bind("<KeyPress>", self.on_key_press)
        self.__window.bind("<KeyPress>", self.cancel_selection, add="+")

        self.__window.bind("<Button-1>", self.interact_with_ui)

        for i in range(self.__max_towers):
            slot=self.create_hotbar_slot(i+1, self.__empty_slot_color)
            self.__hotbar[i]=slot

        freezer=self.create_tower("freezer", 250, "blue")
        soldier=self.create_tower("soldier", 200, "red")
        self.equip_tower(freezer)
        self.equip_tower(soldier)
        # zombie=enemy.Enemy(100, 10, "green")


        
        self.game_loop()
        # self.create_hotbar_slot(1)
        # self.create_hotbar_slot(2)
        # self.create_hotbar_slot(3)
        self.__window.mainloop()

    def game_loop(self):
        if not self.__running:
            self.__window.destroy()
            return

        for key in self.__hotbar:
            if self.__hotbar[key].tower==None:
                self.__hotbar[key].rect.change_color(self.__empty_slot_color)
            else:
                self.__hotbar[key].rect.change_color(self.__filled_slot_color)
        if self.__current_tower==None:
            self.__current_tower_signal.change_color("red")
        else:
            self.__current_tower_signal.change_color("green")

        # Game logic goes here

        self.__window.after(16, self.game_loop)








    def on_key_press(self, event): #Shutting down the game
        if event.keysym == "q":
            print("Quitted")
            self.__running = False

    def get_click_cord(self, event): #Get coordinate of every click on the screen
        a=(f"X: {event.x}, Y: {event.y}")
        print(a)
        return event.x, event.y


    def create_rect(self, x1, y1, x2, y2, fill="red"):
        rect=Rect(self.__canva, x1, y1, x2, y2, fill)
        return rect


    def interact_with_ui(self, event):
        x,y=self.get_click_cord(event)
        for i in self.__interactive:
            i_x1=i.rect.x1
            i_x2=i.rect.x2
            i_y1=i.rect.y1
            i_y2=i.rect.y2
            ''' Checking for UI '''
            if i_x1<x<i_x2 and i_y1<y<i_y2:
                if isinstance(i, hotbar.Slot):
                    if i.tower!=None:
                        print(f"Hotbar's slot clicked, it's a {i.tower.name}")
                        self.select_tower(i.tower)
                        return True
                    else:
                        print("empty slot")
        '''Checking if the space has been taken'''
        if self.compare_cord_rect(x,y, self.__taken):
            print("Space already taken")
            return False
        if self.__current_tower!=None:
            result=self.place_tower(x,y)
            if result==False:
                print("Failed")
                return
            print("Tower placed")
            self.__current_tower=None



    def create_hotbar_slot(self, num, color="black", selected_tower=None):
        hotbar_slot=hotbar.Slot(self.create_rect(self.__hotbar_slot_x1+(self.__hotbar_slot_width+50)*(num-1),
                                    self.__hotbar_slot_y1,
                                    self.__hotbar_slot_x1+(self.__hotbar_slot_width+50)*(num-1)+self.__hotbar_slot_width,
                                    self.__hotbar_slot_height,
                                    color),
                                    tower=selected_tower
                                    )
        self.__interactive.append(hotbar_slot)
        return hotbar_slot

    def create_tower(self, name, cost, color):
        created_tower=module_tower.Tower(name, cost, color)
        return created_tower

    def equip_tower(self, selected_tower):
        if isinstance(selected_tower, module_tower.Tower):
            self.__equipped_towers.append(selected_tower)
            if len(self.__equipped_towers)>self.__max_towers:
                self.__equipped_towers.pop(0)
            for i,v in enumerate(self.__equipped_towers):
                self.__hotbar[i].tower=v 

    def select_tower(self, selected_tower):
        if isinstance(selected_tower, module_tower.Tower):
            self.__current_tower=selected_tower
            print(f"Locked onto the tower: {self.__current_tower.name}")

    def cancel_selection(self, event):
        if event.keysym == "x":
            self.__current_tower=None
            print("Selection released", self.__current_tower)


    def place_tower(self,center_x,center_y):
        if self.__money<self.__current_tower.cost:
            print("Not enough money")
            self.__current_tower=None
            return False
        rad=self.__current_tower.size
        x1=center_x-rad
        y1=center_y-rad
        x2=center_x+rad
        y2=center_y+rad
        x3=x2
        y3=y1
        x4=x1
        y4=y2
        if self.compare_cord_rect(x1, y1, self.__taken) or self.compare_cord_rect(x2, y2, self.__taken) or self.compare_cord_rect(x3,y3, self.__taken) or self.compare_cord_rect(x4,y4,self.__taken):
            return False
        color=self.__current_tower.color
        rect=self.create_rect(x1,y1,x2,y2,color)
        self.__money-=self.__current_tower.cost
        self.__taken.append(rect)
        print(self.__money)
        return True
         #check if the rect collide with the others
        '''
        Check if the cord clicked is inside any of the taken area
        if yes, print cant place and do not place
        else place it down and append the cord to the space taken list
        '''
    def compare_cord_rect(self, cord_x, cord_y, rect_list):
        for i in rect_list:
            i_x1=i.x1
            i_x2=i.x2
            i_y1=i.y1
            i_y2=i.y2
            print(len(rect_list))

            if i_x1<cord_x<i_x2 and i_y1<cord_y<i_y2:
                print(f"True: {cord_x}, {cord_y}, {i_x1}, {i_x2}, {i_y1}, {i_y2}")
                return True 
                '''Collide '''
            else:
                print(f"False: {cord_x}, {cord_y}, {i_x1}, {i_x2}, {i_y1}, {i_y2}")
        return False

        #we have selected_tower list, should associate it with the slots, slot with equipped tower is a different color
        #For placing down towers, get the coord --> cord is the center of the tower-->half length, put the taken cord into a list
            
            
    
game = Game()
game.create_game_loop()

