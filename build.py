from rect import Rect
from interactable import Interactable
from abc import ABC, abstractmethod
class Spawn(Interactable):
    def __init__(self, canva, x1, y1):
        self.__width=50
        self.__height=100
        self.__color="blue"
        super().__init__(Rect(canva, x1, y1, self.__width, self.__height, self.__color))


class Base(Interactable):
    def __init__(self, canva, health, x1, y1):
        self.__width=50
        self.__height=50
        self.__color="red"
        super().__init__(Rect(canva, x1, y1, self.__width, self.__height, self.__color))
        self.__health=health

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if isinstance(value, int):
            self.__health=max(0,value)

    def game_end_lost(self):
        if self.__health==0:
            print("Game ended")
class Path(Interactable, ABC):
    def __init__(self, travel):
        self.__width=50
        self.__travel=travel

    @property
    def width(self):
        return self.__width

    @property 
    def travel(self):
        return self.__travel

    @property
    def middle(self):
        return self.__width/2
class Horizontal_Path(Path):
    def __init__(self, travel):
        super().__init__(travel)

class Right_Path(Horizontal_Path):
    def __init__(self, travel):
        super().__init__(travel)

class Left_Path(Horizontal_Path):
    def __init__(self, travel):
        super().__init__(travel)

class Vertical_Path(Path):
    def __init__(self, travel):
        super().__init__(travel)

class Up_Path(Vertical_Path):
    def __init__(self, travel):
        super().__init__(travel)

class Down_Path(Vertical_Path):
    def __init__(self, travel):
        super().__init__(travel)
        





    '''
    Path should be nodes, the nodes are in the middle of the path
    Path will be splitted into up path, down path, right path and left path
    The type of path will dictate which direction the enemy will move
    '''
