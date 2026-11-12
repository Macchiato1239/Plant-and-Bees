from Base.rect import Rect
from abc import ABC, abstractmethod
class Interactable(ABC):
    def __init__(self, rect):
        self.__rect=rect

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        if isinstance(value, Rect):
            self.__rect=value

    @property
    def cord_x(self):
        return self.__rect.cord_x
    @cord_x.setter
    def cord_x(self, value):
        if isinstance(value, (int,float)):
            self.__rect.x1=value

    @property
    def cord_y(self):
        return self.__rect.cord_y  
    @cord_y.setter
    def cord_y(self, value):
        if isinstance(value, (int,float)):
            self.__rect.y1=value
