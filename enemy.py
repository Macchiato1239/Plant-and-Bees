from rect import Rect
class Enemy:
    def __init__(self, health, speed, color): 
        '''add armor, buff later
        health = damage'''
        self.__health=health
        self.__speed=speed
        self.__color=color

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