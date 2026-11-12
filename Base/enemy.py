from Base.rect import Rect
from Base.interactable import Interactable
from abc import ABC, abstractmethod
class Enemy(Interactable): #this is supposed to be abc
    def __init__(self, canva, name, x1, y1, width, height, health, speed, color): 
        '''add armor, buff later
        health = damage'''
        super().__init__(Rect(canva, x1, y1, width, height, color))
        self.__name=name
        self.__reward=health
        self.__initial_health=health
        self.__initial_speed=speed
        self.__health=health
        self.__speed=speed
        self.__progress=0
        self.__distance_covered=0

        '''Debuff'''
        self.__freeze=0
        self.__freeze_level=0

        self.__burn=0
        self.__burn_damage=0

        self.__stun=0

        self.__debuff=[]
        '''Buff and debuff is given during gameplay, not at spawn'''

        '''self.__progress is the index of the item in a list of path,
        each index point to a pair of x,y (corners)'''

    @property
    def initial_health(self):
        return self.__inital_health

    @property
    def freeze(self):
        return self.__freeze
    @freeze.setter
    def freeze(self, value):
        if isinstance(value, (int, float)):
            self.__freeze=value

    @property
    def freeze_level(self):
        return self.__freeze_level
    @freeze_level.setter
    def freeze_level(self, value):
        if isinstance(value, int):
            self.__freeze_level=min(4,value)

    @property
    def burn(self):
        return self.__burn
    @burn.setter
    def burn(self, value):
        if isinstance(value, [int, float]):
            self.__burn=value

    @property
    def burn_damage(self):
        return self.__burn_damage
    @burn_damage.setter
    def burn_damage(self,value):
        if isinstance(value, (float, int)):
            self.__burn_damage=value

    @property
    def stun(self):
        return self.__stun
    @stun.setter
    def stun(self, value):
        if isinstance(value, [int, float]):
            self.__stun=value

    @property
    def name(self):
        return self.__name

    @property
    def reward(self):
        return self.__reward
    
    @property
    def health(self):
        return self.__health
    
    @property
    def speed(self):
        return self.__speed

    @property
    def color(self):
        return self.__color

    @property
    def progress(self):
        return self.__progress

    @property
    def buff(self):
        return self.__buff

    @buff.setter
    def buff(self, value):
        self.__buff=value

    @property
    def debuff(self):
        return self.__debuff

    @debuff.setter
    def debuff(self, value):
        self.__debuff=value
    
    @progress.setter
    def progress(self, value):
        if isinstance(value, int):
            self.__progress=value

    @property
    def distance_covered(self):
        return self.__distance_covered
    
    @distance_covered.setter
    def distance_covered(self, value):
        if isinstance(value, [int, float]):
            self.__distance_covered=value


    @health.setter
    def health(self,value):
        if isinstance(value, int):
            self.__health=value

    @speed.setter
    def speed(self, value):
        if isinstance(value, int):
            self.__speed=value

    @color.setter
    def color(self, value):
        if isinstance(value, str):
            self.__color=value


    def move(self, canva, x, y, delta_time):
        x_reach=True
        y_reach=True
        if self.rect.cord_x!=x:
            di=1 if self.rect.cord_x<x else -1

            x_after_move=self.rect.cord_x+di*self.__speed * delta_time

            if (di==1 and x_after_move>x) or (di==-1 and x_after_move<x):
                self.rect.x1=x-self.rect.width/2
                canva.move(self.rect.rect_id, x-self.rect.cord_x, 0)
            else:
                self.__distance_covered+=abs(x_after_move-self.rect.cord_x)
                self.rect.x1+=di*self.__speed * delta_time
                canva.move(self.rect.rect_id, di*self.__speed * delta_time, 0)
                x_reach=False
        if self.rect.cord_y!=y:
            di=1 if self.rect.cord_y<y else -1

            y_after_move=self.rect.cord_y+di*self.__speed * delta_time

            if (di==1 and y_after_move>y) or (di==-1 and y_after_move<y):
                self.rect.y1=y-self.rect.height/2
                canva.move(self.rect.rect_id, 0, y-self.rect.cord_y)
            else:
                self.__distance_covered+=abs(y_after_move-self.rect.cord_y)
                self.rect.y1+=di*self.__speed * delta_time
                canva.move(self.rect.rect_id, 0, di*self.__speed * delta_time)
                y_reach=False
        return x_reach and y_reach

    def process_debuff(self, delta_time):
        if self.__burn!=0:
            self.__health-=self.__burn_damage
            self.__burn=max(0, self.__burn-delta_time)

        if self.__freeze!=0:
            if self.__freeze_level in [1,2,3]:
                self.__speed-=(self.__speed*20*self.__freeze_level)/100
                self.__freeze=max(0, self.__freeze-delta_time)
            if self.__freeze_level == 4:
                self.__stun=0.6
                self.__freeze_level=0
                self.__freeze=0

        if self.__stun!=0:
            self.__speed=0
            self.__stun=max(0, self.__stun-delta_time)
        if self.__stun==0 and self.__freeze==0:
            self.__speed=self.__initial_speed

    def delete(self):
        self.rect.delete()
        

class Enemy_Info:
    def __init__(self, name, health, speed, color, width, height):
        self.__name=name
        self.__health=health
        self.__speed=speed
        self.__color=color
        self.__width=width
        self.__height=height

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health
    @property
    def speed(self):
        return self.__speed

    @property
    def color(self):
        return self.__color

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height

