from abc import ABC, abstractmethod
import tkinter as tk

class Rect():
    def __init__(self, canva, x1, y1, width, height, fill="red"):
        self.__x1=x1
        self.__y1=y1
        self.__width=width
        self.__height=height
        self.__fill=fill
        self.__canva=canva
        self.__rect_id=canva.create_rectangle(self.__x1, self.__y1, self.__x1+self.__width, self.__y1+self.__height, fill=self.__fill)


    def cord_overlap_check(self, x, y):
        return (self.__x1 < x < self.__x1+self.__width and self.__y1 < y < self.__y1+self.height)


    def change_color(self, value):
        if isinstance(value, str):
            self.__canva.itemconfig(self.__rect_id, fill=value)
            self.__fill=value

    @property 
    def cord_x(self):
        return self.__x1+self.__width/2

    @property
    def cord_y(self):
        return self.__y1+self.__height/2
    
    @property
    def rect_id(self):
        return self.__rect_id

    @property
    def x1(self):
        return self.__x1
    @x1.setter
    def x1(self,value):
        if isinstance(value, int):
            self.__x1=value

    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self,value):
        if isinstance(value, int):
            self.__width=value

    @property
    def y1(self):
        return self.__y1
    @y1.setter
    def y1(self,value):
        if isinstance(value, int):
            self.__y1=value

    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self,value):
        if isinstance(value, int):
            self.__height=value

    @property
    def fill(self):
        return self.__fill
    @fill.setter
    def fill(self, value):
        if isinstance(value, str):
            self.__fill=value
        


