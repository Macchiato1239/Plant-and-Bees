from rect import Rect
from interactable import Interactable
from abc import ABC, abstractmethod
class Enemy(Interactable):
    def __init__(self, canva, x1, y1, health, speed, color): 
        '''add armor, buff later
        health = damage'''
        super().__init__(Rect(canva, x1, y1, 40, 40, color))
        self.__health=health
        self.__speed=speed
        self.__progress=0
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
                self.rect.y1+=di*self.__speed * delta_time
                canva.move(self.rect.rect_id, 0, di*self.__speed * delta_time)
                y_reach=False
        return x_reach and y_reach
