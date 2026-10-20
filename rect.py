from abc import ABC, abstractmethod
import tkinter as tk
class Rect():
    def __init__(self, x1, y1, x2, y2, fill="red"):
        self.__x1=x1
        self.__x2=x2
        self.__y1=y1
        self.__y2=y2
        self.__fill=fill

    def render(self, canva):
        canva.create_rectangle(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__fill)

    def cord_overlap_check(self, x, y):
        return (self.__x1 < x < self.__x2 and self.__y1 > y > self.__y2)

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