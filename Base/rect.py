from abc import ABC, abstractmethod
import tkinter as tk

class Rect():
    def __init__(self, canva, x1: int, y1: int, width: int, height: int, fill="brown", outline="#613c01", border_width=1) -> None:
        self.__x1=x1
        self.__y1=y1
        self.__width=width
        self.__height=height
        self.__fill=fill
        self.__canva=canva
        self.__outline=outline
        self.__rect_id=canva.create_rectangle(self.__x1,
                                            self.__y1,
                                            self.__x1+self.__width,
                                            self.__y1+self.__height,
                                            fill=self.__fill,
                                            outline=self.__outline,
                                            width=border_width)


    def cord_overlap_check(self, x: int, y: int) -> bool:
        ''' Check if a coordinate is within itself'''
        return (self.__x1 < x < self.__x1+self.__width and self.__y1 < y < self.__y1+self.__height)


    def change_color(self, value: str) -> None:
        ''' Change color'''
        if isinstance(value, str):
            self.__canva.itemconfig(self.__rect_id, fill=value)
            self.__fill=value

    def delete(self) -> None:
        self.__canva.delete(self.__rect_id)

    @property 
    def cord_x(self) -> None:
        return self.__x1+self.__width/2

    @property
    def cord_y(self) -> None:
        return self.__y1+self.__height/2
    
    @property
    def rect_id(self) -> None:
        return self.__rect_id
    # =====
    @property
    def x1(self) -> int:
        return self.__x1
    @x1.setter
    def x1(self,value: int) -> None:
        if isinstance(value, (int,float)):
            self.__x1=value
    # =====
    @property
    def width(self) -> int:
        return self.__width
    @width.setter
    def width(self,value: int) -> None:
        if isinstance(value, (int,float)):
            self.__width=value

    # =====
    @property
    def y1(self) -> int:
        return self.__y1
    @y1.setter
    def y1(self,value: int) -> None:
        if isinstance(value, (int,float)):
            self.__y1=value

    # =====
    @property
    def height(self) -> int:
        return self.__height
    @height.setter
    def height(self,value: int) -> None:
        if isinstance(value, (int,float)):
            self.__height=value

    # =====
    @property
    def fill(self) -> str:
        return self.__fill
    @fill.setter
    def fill(self, value: str) -> None:
        if isinstance(value, str):
            self.__fill=value
        


