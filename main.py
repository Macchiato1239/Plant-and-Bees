import tkinter as tk
from rect import Rect
import hotbar
import module_tower
from module_tower import TowerInfo, Tower, DpsStats, DebuffStats, IncomeStats, SupportStats
from module_tower import DpsTower, DebuffTower, Farm, SupportTower
from debuff import EffectType
import enemy
import math
import time
import build
from dictionary import Ebook, Tbook
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
        self.__starting_money=800
        self.__money=self.__starting_money
        self.__base=build.Base(self.__canva, self.__base_health, 900, 300)
        self.__max_towers=40

        self.__mode=[]
        self.__wave_progress=0
        self.__mode_progress=0
        self.__time_til_next_spawn=0
        self.__time_since_last_spawn=0
        self.__range_circle=self.__canva.create_oval(0,0,0,0, fill="orange",
                                                      outline="black",
                                                        stipple="gray25",
                                                        state="hidden")
        
        '''UI'''
        self.__money_display=self.__canva.create_text(
            100,50,
            text=f"Cash: {self.__money}",
            font=("Arial", 24),
            fill="green")

        self.__health_display=self.__canva.create_text(
            500,50,
            text=f"Health: {self.__base_health}",
            font=("Arial", 24),
            fill="red")
        self.__wave_display=self.__canva.create_text(
            700,50,
            text=f"Wave {self.__mode_progress+1}",
            font=("Arial", 20),
            fill="black")



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
        self.__active_towers=[]

        self.__current_tower=None
        self.__current_tower_signal=self.create_rect(0, 0, 30, 30, "red")


        '''Build properties'''
        self.__map=[[self.__spawn.rect.cord_x, self.__spawn.rect.cord_y], 
                    [100, 300], #+100
                    [100, 400], #+100
                    [350, 400], #+250
                    [350, 300], #+100
                    [self.__base.rect.cord_x, self.__base.rect.cord_y]] #+550

        self.__map_length=0


        '''Enemies properties'''


    def create_game_loop(self):
        self.__window.geometry(
            f"{self.__window_width}x{self.__window_height}"
        )
        self.__canva.pack()
        self.__window.bind("<KeyPress>", self.on_key_press)
        self.__window.bind("<KeyPress>", self.cancel_selection, add="+")
        self.__window.bind("<Button-1>", self.interact_with_ui)
        self.__canva.bind("<Motion>", self.mouse_coordinate)
        self.__canva.bind("<Motion>", self.track_display_range)

        for i in range(self.__max_towers):
            slot=self.create_hotbar_slot(i+1, self.__empty_slot_color)
            self.__hotbar[i]=slot


        self.equip_tower(1)
        self.equip_tower(2)
        self.equip_tower(3)
        self.equip_tower(4)

        self.__taken.append(self.__spawn.rect)
        self.__taken.append(self.__base.rect)
        self.__last_time=time.time()

        '''Calculating map length'''
        for i in range(1,len(self.__map)):
            if self.__map[i][0]==self.__map[i-1][0]: 
                '''x2=x1 -> horizontal -> length=abs(y2-y1)'''
                self.__map_length+=abs(self.__map[i][1]-self.__map[i-1][1])
                

            if self.__map[i][1]==self.__map[i-1][1]: 
                self.__map_length+=abs(self.__map[i][0]-self.__map[i-1][0])
                

        '''Path creation from self.__map'''
        for i in range(len(self.__map)-1):
            path=build.Path(self.__canva, self.__map[i][0], self.__map[i][1], self.__map[i+1][0], self.__map[i+1][1])
            self.__taken.append(path.rect)

        '''Enemy'''
        wave1=[[[1,0.5]]*4+[[1,0]]]
        wave2=[[[1,0.5]]*6+[[1,0]]]
        wave3=[[[2,0.3]]*2+[[2,1]]+[[1,0.5]]*4]
        wave4=[[[2,0.3]]+[[2,0.5]]+[[3,0.8]]*5]
        self.__mode+=wave1+wave2+wave3+wave4

        # zombie=enemy.Enemy_Info(10, 0.5, "green", 30, 30)
        # self.spawn(zombie)

        '''Rendering base and spawn on top of all'''
        self.__canva.tag_raise(self.__spawn.rect.rect_id)
        self.__canva.tag_raise(self.__base.rect.rect_id)
        self.game_loop()
        self.__window.mainloop()

    def game_loop(self):
        self.__current_time=time.time()
        delta_time=(self.__current_time-self.__last_time)
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

        '''Spawning enemies from the wave list'''


        self.__time_since_last_spawn+=delta_time
        if self.__mode_progress!=-1:
            if self.__time_since_last_spawn>=self.__time_til_next_spawn and self.__wave_progress!=-1:
                self.spawn(Ebook.get(self.__mode[self.__mode_progress][self.__wave_progress][0]))
                self.__time_til_next_spawn=self.__mode[self.__mode_progress][self.__wave_progress][1]
                if self.__wave_progress!=len(self.__mode[self.__mode_progress])-1:
                    self.__wave_progress+=1
                else:
                    self.__wave_progress=-1
                self.__time_since_last_spawn=0

        '''Check if the enemy in this wave is dead before going to the next wave'''
        if not self.__active_enemies and self.__mode_progress!=-1:
            self.__wave_progress=0
            self.__mode_progress+=1
            if self.__mode_progress==len(self.__mode):
                self.__mode_progress = -1

        
        '''Moving enemies'''
        for i in self.__active_enemies[:]:
            i.process_debuff(delta_time)
            
            '''
            Loop through a copy version of the list,
            So to remove enemies if they die or reach base,
            this is to fix skipping items in the list
            '''

            cord_index=i.progress

            dest_x=self.__map[cord_index][0]
            dest_y=self.__map[cord_index][1]

            if i.move(self.__canva, dest_x, dest_y, delta_time*100):
                '''
                Enemy reached a corner OR base
                '''
                if cord_index==len(self.__map)-1:
                    print("End reached")
                    self.__base_health=max(0, self.__base_health-i.health)
                    self.__active_enemies.remove(i)
                    i.delete()
                else:
                    i.progress+=1
                    i.move(self.__canva, self.__map[i.progress][0], self.__map[i.progress][1], delta_time*100)
            else:
                i.move(self.__canva, dest_x, dest_y, delta_time*100)

        '''Tower actions'''
        for tower in self.__active_towers:
            if isinstance(tower, DpsTower):
                in_range=[]
                damage=tower.act()
                if not damage:
                    continue

                for enemy in self.__active_enemies:
                    if self.range_enemy_tower(enemy, tower):
                        in_range.append(enemy)

                final_target=self.enemy_sorter(in_range)
                if final_target==0:
                    continue
                final_target.health-=damage
                if isinstance(tower, DebuffTower):
                    if tower.type==EffectType.FROZEN:
                        final_target.freeze=tower.duration
                        final_target.freeze_level+=tower.magnitude
            elif isinstance(tower, SupportTower):
                pass
            elif isinstance(tower, Farm):
                pass
        



        '''Money UI'''
        self.__canva.itemconfig(
            self.__money_display,
            text=f"Cash: {self.__money}"
        )

        '''Health UI'''
        self.__canva.itemconfig(
            self.__health_display,
            text=f"Health: {self.__base_health}"
        )

        '''Wave counter UI'''
        if self.__mode_progress!=-1:
            self.__canva.itemconfig(
                self.__wave_display,
                text=f"Wave {self.__mode_progress+1}/{len(self.__mode)}"
            )
        '''Deleting dead enemies'''
        for i in self.__active_enemies[:]:
            if i.health<=0:
                self.__money+=i.reward
                self.__active_enemies.remove(i)
                i.delete()

        self.__last_time=self.__current_time
        self.__window.after(16, self.game_loop)



    def mouse_coordinate(self, event):
        '''Constantly return mouse's coordinate'''
        cord_x=event.x
        cord_y=event.y
        print(cord_x, cord_y)
        return cord_x,cord_y
    
    def update_display_range(self, cord_x, cord_y):
        '''Constantly display the range of the selected tower if exists'''
        tower_range=Tbook.get(self.__current_tower).act_range
        x1=cord_x-tower_range/2
        y1=cord_y-tower_range/2
        x2=cord_x+tower_range/2
        y2=cord_y+tower_range/2
        
        self.__canva.coords(self.__range_circle, x1,y1,x2,y2)

    def track_display_range(self, event):
        if not self.__current_tower:
            self.__canva.itemconfigure(self.__range_circle, state="hidden")
            return
        self.__canva.itemconfigure(self.__range_circle, state="normal")

        cord_x,cord_y=self.mouse_coordinate(event)
        self.update_display_range(cord_x, cord_y)

    
    def on_key_press(self, event): #Shutting down the game
        if event.keysym == "q":
            self.__running = False

    def get_click_cord(self, event): #Get coordinate of every click on the screen
        a=(f"X: {event.x}, Y: {event.y}")
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

            if i_x1<x<i_x1+i_width and i_y1<y<i_y1+i_height:
                if isinstance(i, hotbar.Slot):
                    if i.tower!=None:
                        print(f"Hotbar's slot clicked, it's a {Tbook.get(i.tower).name}")
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

    def equip_tower(self, tower):
        '''Select towers to be in the 5 slots'''
        if isinstance(tower, int):
            self.__equipped_towers.append(tower)
            if len(self.__equipped_towers)>self.__max_towers:
                self.__equipped_towers.pop(0)
            for i,v in enumerate(self.__equipped_towers):
                self.__hotbar[i].tower=v

    def select_tower_card(self, tower):
        '''Decide which tower will be placed on the next left click'''
        if isinstance(tower, int):
            self.__current_tower=tower

    def cancel_selection(self, event):
        '''Cancel the tower thats being selected to perform other actions'''
        if event.keysym == "x":
            self.__current_tower=None

    def place_tower(self,center_x,center_y):
        tower_info=Tbook.get(self.__current_tower)
        if self.__money<tower_info.cost:
            print("Not enough money")
            self.__current_tower=None
            return False
        rad=tower_info.size
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
        color=tower_info.color
        rect=self.create_rect(x1,y1,rad*2,rad*2, color)
        tower=Tbook.summon_tower(self.__current_tower, rect)
        print(tower.color)
        self.__active_towers.append(tower) 
        self.__money-=tower.cost
        self.__taken.append(rect)
        self.__towers.append(tower)
        return True

    def compare_cord_rect(self, cord_x, cord_y, rect_list):
        for i in rect_list:
            i_x1=i.x1
            i_width=i.width
            i_y1=i.y1
            i_height=i.height

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

    def spawn(self, enemy_info):
        if not isinstance(enemy_info, enemy.Enemy_Info):
            return
        name=enemy_info.name
        health=enemy_info.health
        speed=enemy_info.speed
        color=enemy_info.color
        width=enemy_info.width
        height=enemy_info.height

        spawn_x=self.__spawn.rect.cord_x-width/2
        spawn_y=self.__spawn.rect.cord_y-height/2



        spawned_enemy=enemy.Enemy(self.__canva, name, spawn_x, spawn_y, width, height, health, speed, color)
        self.__active_enemies.append(spawned_enemy)

        return spawned_enemy
 
    def enemy_sorter(self, enemies):
        most_covered=0
        closest_enemy=0
        for i in enemies:
            if i.distance_covered>most_covered:
                most_covered=i.distance_covered
                closest_enemy=i
        return closest_enemy

'''
Buff:
-Hidden
-Lead
-Swift
-Aggro
-Boss
-Blessed
->Buff can also stack
Debuff:
-Burn: Deal tick damage for however long
-Freeze: 4 level: each -20% speed, at the 4th shot, stop completely for 0.5s
-Stun: Just stop completely for certain time
'''

game = Game()
game.create_game_loop()

