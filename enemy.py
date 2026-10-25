from rect import Rect
from interactable import Interactable
from abc import ABC, abstractmethod
class Enemy(Interactable):
    def __init__(self, health, speed, color): 
        '''add armor, buff later
        health = damage'''
        super().__init__(Rect(0, 200, 30, 230, color))
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

    def move_right(self):
        self.__rect.x1+=self.__speed
        self.__rect.x2+=self.__speed

    def move_left(self):
        self.__rect.x1-=self.__speed
        self.__rect.x2-=self.__speed
        pass

    def move_top(self):
        pass

    def move_bottom(self):
        pass