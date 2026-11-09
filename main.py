import tkinter as tk
from rect import Rect
import hotbar
import module_tower
import enemy
import math
import time
import build
class Game:
    def __init__(self):
        '''Window property'''
        self.__last_time=0
        self.__current_time=0
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
        self.__spawn=build.Spawn(self.__canva, 0, 300)
        self.__active_enemies=[]
        self.__starting_money=600
        self.__money=self.__starting_money
        self.__base=build.Base(self.__canva, self.__base_health, 900, 300)
        self.__money_display=self.__canva.create_text(
            50,50,
            text=f"{self.__money}",
            font=("Arial", 24),
            fill="black")

        self.__health_display=self.__canva.create_text(
            500,50,
            text=f"{self.__base_health}",
            font=("Arial", 24),
            fill="red")
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
        self.__towers=[]

        self.__current_tower=None
        self.__current_tower_signal=self.create_rect(0, 0, 30, 30, "red")


        '''Build properties'''
        self.__map=[[self.__spawn.rect.cord_x, self.__spawn.rect.cord_y],
                    [100,300],
                    [100, 400],
                    [350, 400],
                    [350, 300], 
                    [self.__base.rect.cord_x, self.__base.rect.cord_y]]

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

        freezer=self.create_tower_card("freezer", 250, "blue", 4, 0.5, 10)
        soldier=self.create_tower_card("soldier", 200, "red", 5, 0.2, 10)
        self.equip_tower(freezer)
        self.equip_tower(soldier)

        self.__taken.append(self.__spawn.rect)
        self.__taken.append(self.__base.rect)
        self.__last_time=time.time()


        '''
        Path creation from self.__map
        '''
        for i in range(len(self.__map)-1):
            path=build.Path(self.__canva, self.__map[i][0], self.__map[i][1], self.__map[i+1][0], self.__map[i+1][1])
            self.__taken.append(path.rect)
        zombie=self.spawn_enemy(self.__canva, 30, 30, 50, 0.5, "green")
        self.__canva.tag_raise(self.__spawn.rect.rect_id)
        self.__canva.tag_raise(self.__base.rect.rect_id)
        self.game_loop()
        self.__window.mainloop()

    def game_loop(self):
        self.__current_time=time.time()
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

        '''
        Moving enemies'''
        for i in self.__active_enemies[:]:

            '''
            Loop through a copy version of the list,
            So to remove enemies if they die or reach base,
            this is to fix skipping items in the list
            '''


            delta_time=(self.__current_time-self.__last_time)*100
            cord_index=i.progress

            dest_x=self.__map[cord_index][0]
            dest_y=self.__map[cord_index][1]

            if i.move(self.__canva, dest_x, dest_y, delta_time):
                '''
                Enemy reached a corner OR base
                '''
                if cord_index==len(self.__map)-1:
                    print("End reached")
                    self.__base_health=max(0, self.__base_health-i.health)
                    self.__active_enemies.remove(i)
                else:
                    i.progress+=1
                    i.move(self.__canva, self.__map[i.progress][0], self.__map[i.progress][1], delta_time)
            else:
                i.move(self.__canva, dest_x, dest_y, delta_time)

        '''
        Money UI
        '''
        self.__canva.itemconfig(
            self.__money_display,
            text=f"{self.__money}"
        )

        '''
        Health UI
        '''
        self.__canva.itemconfig(
            self.__health_display,
            text=f"{self.__base_health}"
        )

        '''
        Towers' action
        '''

        # Game logic goes here
        self.__last_time=self.__current_time
        self.__window.after(16, self.game_loop)








    def on_key_press(self, event): #Shutting down the game
        if event.keysym == "q":
            print("Quitted")
            self.__running = False

    def get_click_cord(self, event): #Get coordinate of every click on the screen
        a=(f"X: {event.x}, Y: {event.y}")
        print(a)
        return event.x, event.y


    def create_rect(self, x1, y1, width, height, fill="red"):
        rect=Rect(self.__canva, x1, y1, width, height, fill)
        return rect


    def interact_with_ui(self, event):
        x,y=self.get_click_cord(event)
        for i in self.__interactive:
            i_x1=i.rect.x1
            i_width=i.rect.width
            i_y1=i.rect.y1
            i_height=i.rect.height
            ''' Checking for UI '''
            if i_x1<x<i_x1+i_width and i_y1<y<i_y1+i_height:
                if isinstance(i, hotbar.Slot):
                    if i.tower!=None:
                        print(f"Hotbar's slot clicked, it's a {i.tower.name}")
                        self.select_tower_card(i.tower)
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
                                    self.__hotbar_slot_width,
                                    self.__hotbar_slot_height,
                                    color),
                                    tower=selected_tower
                                    )
        self.__interactive.append(hotbar_slot)
        return hotbar_slot

    def create_tower_card(self, name, cost, color, damage, fire_rate, act_range):
        created_tower=module_tower.Tower_Card(name, cost, color, damage, fire_rate, act_range)
        return created_tower

    def equip_tower(self, selected_tower):
        if isinstance(selected_tower, module_tower.Tower_Card):
            self.__equipped_towers.append(selected_tower)
            if len(self.__equipped_towers)>self.__max_towers:
                self.__equipped_towers.pop(0)
            for i,v in enumerate(self.__equipped_towers):
                self.__hotbar[i].tower=v 

    def select_tower_card(self, selected_tower):
        if isinstance(selected_tower, module_tower.Tower_Card):
            self.__current_tower=selected_tower
            print(f"Locked onto the tower: {self.__current_tower.name}")

    def cancel_selection(self, event):
        if event.keysym == "x":
            self.__current_tower=None
            print("Selection released", self.__current_tower)

    def create_tower(self, name, cost, color, damage, fire_rate, act_range, rect):
        if self.__current_tower==None:
            return
        tower=module_tower.Tower_Manifested(name, cost, color, damage, fire_rate, act_range, rect)
        self.__towers.append(tower) #does this create a duplicate version of tower and would it affect anything?
        return tower



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
        rect=self.create_rect(x1,y1,rad*2,rad*2, color)
        tower=self.create_tower(self.__current_tower.name,
                                self.__current_tower.cost,
                                color,
                                self.__current_tower.damage,
                                self.__current_tower.fire_rate,
                                self.__current_tower.act_range,
                                rect)
        self.__money-=self.__current_tower.cost
        self.__taken.append(rect)
        
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
            i_width=i.width
            i_y1=i.y1
            i_height=i.height
            print(len(rect_list))

            if i_x1<cord_x<i_x1+i_width and i_y1<cord_y<i_y1+i_height:
                return True
        return False

    def dist_cord_cord(self, rect1, rect2):
        cord1_x=rect1.cord_x
        cord1_y=rect1.cord_y
        cord2_x=rect2.cord_x
        cord2_y=rect2.cord_y

        horizontal=(cord1_x-cord2_x)**2
        vertical=(cord1_y-cord2_y)**2
        dist=math.sqrt(horizontal+vertical)
        return dist

    def range_enemy_tower(self, enemy, tower):
        dist=self.dist_cord_cord(enemy.rect, tower.rect)
        if dist<=tower.act_range:
            return True
        return False

    def spawn_enemy(self, canva, width, height, health, speed, color):
        spawn_x=self.__spawn.rect.cord_x-width/2
        spawn_y=self.__spawn.rect.cord_y-height/2
        spawned_enemy=enemy.Enemy(canva, spawn_x, spawn_y, health, speed, color)
        self.__active_enemies.append(spawned_enemy)
        return spawned_enemy

    def builder(self, path_type):
        pass
    # def condition_for_action(self, selected_tower):
    #     if selected_tower.cooldown_check() and :
game = Game()
game.create_game_loop()

