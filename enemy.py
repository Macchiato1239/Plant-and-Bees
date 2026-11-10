from rect import Rect
from interactable import Interactable
from abc import ABC, abstractmethod
class Enemy(Interactable): #this is supposed to be abc
    def __init__(self, canva, x1, y1, width, height, health, speed, color): 
        '''add armor, buff later
        health = damage'''
        super().__init__(Rect(canva, x1, y1, width, height, color))
        self.__health=health
        self.__speed=speed
        self.__progress=0
        self.__distance_covered=0
        '''
        self.__progress is the index of the item in a list of path, each index point to a pair of x,y (corners)'''

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

    def delete(self):
        self.rect.delete()
        

class Enemy_Info:
    def __init__(self, health, speed, color, width, height):
        self.__health=health
        self.__speed=speed
        self.__color=color
        self.__width=width
        self.__height=height

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

    

    '''
Stats: Health, speed, -> Inherit from info card
->Is universal on spawn
UI: color, position: x,y, distance to base, progress
    
    '''
'''
The card points to the entity with a spawn function
Enemy must be inside a the active list
Enemy must already have predefined info'''