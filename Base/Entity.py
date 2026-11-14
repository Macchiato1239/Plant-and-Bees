from Base.rect import Rect
from abc import ABC, abstractmethod

class Entity(ABC):
    '''Everything drawn onto the screen inherits from this class as it has a rect'''
    def __init__(self, rect: Rect) -> None:
        self.__rect=rect
        # === Visual representation of the object ===

    @property
    def rect(self) -> Rect:
        return self.__rect

    @rect.setter
    def rect(self, value: Rect):
        if isinstance(value, Rect):
            self.__rect=value

    @property
    def cord_x(self) -> int:
        '''Coordinate x of the center of an entity object'''
        return self.__rect.cord_x
    @cord_x.setter
    def cord_x(self, value: int) -> None:
        if isinstance(value, (int,float)):
            self.__rect.x1=value

    @property
    def cord_y(self) -> int:
        '''Coordinate x of the center of an entity object'''
        return self.__rect.cord_y  
    @cord_y.setter
    def cord_y(self, value: int | float) -> None:
        if isinstance(value, (int,float)):
            self.__rect.y1=value

    def delete(self) -> None:
        '''Deleting the visual representation itself'''
        self.rect.delete()
