from rect import Rect
from interactable import Interactable
from abc import ABC, abstractmethod
class Enemy(Interactable):
    def __init__(self, canva, health, speed, color): 
        '''add armor, buff later
        health = damage'''
        super().__init__(Rect(canva, 0, 200, 40, 40, color))
        self.__health=health
        self.__speed=speed
        self.__cord_x=self.rect.x1+self.rect.width/2
        self.__cord_y=self.rect.y1+self.rect.height/2

    @property
    def cord_x(self):
        return self.__cord_x
    @property
    def cord_y(self):
        return self.__cord_y

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