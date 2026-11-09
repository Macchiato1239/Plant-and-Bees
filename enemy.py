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

    @property
    def health(self):
        return self.__health
    @property
    def speed(self):
        return self.__speed

    @property
    def color(self):
        return self.__color

    @health.setter
    def health(self,value):
        if isinstance(value, int):
            self.__health=int

    @speed.setter
    def speed(self, value):
        if isinstance(value, int):
            self.__speed=int

    @color.setter
    def color(self, value):
        if isinstance(value, str):
            self.__color=value

    def move_right(self, canva, delta_time):
        self.rect.x1+=self.__speed * delta_time
        self.rect.y1+=self.__speed * delta_time
        canva.move(self.rect.rect_id, self.__speed * delta_time, 0)

    def move_left(self, canva, delta_time):
        self.rect.x1-=self.__speed * delta_time
        self.rect.x2-=self.__speed * delta_time
        canva.move(self.rect.rect_id, -self.__speed * delta_time, 0)

    def move_top(self, canva, delta_time):
        self.rect.y1-=self.__speed * delta_time
        self.rect.y2-=self.__speed * delta_time
        canva.move(self.rect.rect_id, 0, -self.__speed * delta_time)

    def move_bottom(self, canva, delta_time):
        self.rect.y1+=self.__speed * delta_time
        self.rect.y2+=self.__speed * delta_time
        canva.move(self.rect.rect_id, 0, self.__speed * delta_time)