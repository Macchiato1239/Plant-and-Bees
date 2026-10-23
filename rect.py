from abc import ABC, abstractmethod
import tkinter as tk
'''
What needs a rect
UI
towers
path
enemies

'''
class Rect():
    def __init__(self, canva, x1, y1, x2, y2, fill="red"):
        self.__x1=x1
        self.__x2=x2
        self.__y1=y1
        self.__y2=y2
        self.__fill=fill
        self.__canva=canva
        self.__rect_id=canva.create_rectangle(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__fill)

    # def render(self, canva):
    #     created_rect=canva.create_rectangle(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__fill)
    #     return created_rect
    
    def cord_overlap_check(self, x, y):
        return (self.__x1 < x < self.__x2 and self.__y1 > y > self.__y2)


    def change_color(self, value):
        if isinstance(value, str):
            self.__canva.itemconfig(self.__rect_id, fill=value)
            self.__fill=value

    @property
    def rect_id(self):
        return self.__rect_id

    @property
    def x1(self):
        return self.__x1

    @property
    def x2(self):
        return self.__x2

    @property
    def y1(self):
        return self.__y1

    @property
    def y2(self):
        return self.__y2

    @property
    def fill(self):
        return self.__fill

