from rect import Rect
from interactable import Interactable
from abc import ABC, abstractmethod
class Spawn(Interactable):
    def __init__(self, canva, x, y):
        self.__width=25
        self.__height=25
        self.__color="blue"
        super().__init__(Rect(canva, x-self.__width, y-self.__height, self.__width*2, self.__height*2, self.__color))


class Base(Interactable):
    def __init__(self, canva, health, x, y):
        self.__width=25
        self.__height=25
        self.__color="purple"
        super().__init__(Rect(canva, x-self.__width, y-self.__width, self.__width*2, self.__height*2, self.__color))
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
class Path(Interactable):
    '''
    This is just UI,
    important thing is the cord of start and end 
    Before the game loop, run through all the coordinate in the self.__map and create paths from them
    '''
    def __init__(self, canva, start_x, start_y, end_x, end_y):
        self.__start_x=start_x
        self.__start_y=start_y
        self.__end_x=end_x
        self.__end_y=end_y
        self.__path_width=25
        x1=min(start_x, end_x)-self.__path_width
        y1=min(start_y, end_y)-self.__path_width
        width=self.__path_width*2 + abs(start_x-end_x)
        height=self.__path_width*2 + abs(start_y-end_y)
        path=Rect(canva, x1, y1, width, height, "grey")
        super().__init__(path)

    @property
    def start_x(self):
        return self.__start_x

    @property
    def start_y(self):
        return self.__start_y

    @property
    def end_x(self):
        return self.__end_x

    @property
    def end_y(self):
        return self.__end_y









    
# class Horizontal_Path(Path, Interactable): 
#     def __init__(self, canva, x1, y1, width, travel):
#         Path.__init__(self, travel, width)
#         Interactable.__init__(self, Rect(canva, x1, y1, travel, width, "grey"))
        

# class Right_Path(Horizontal_Path):
#     def __init__(self, canva, x1, y1, width, travel):
#         super().__init__(canva, x1, y1, travel, width)

# class Left_Path(Horizontal_Path):
#     def __init__(self, canva, x1, y1, width, travel):
#         super().__init__(canva, x1, y1, travel, width)

#     '''
#     For vertical
#     Width=Width
#     Travel=Height
#     '''
# class Vertical_Path(Path, Interactable):
#     def __init__(self, canva, x1, y1, width, travel):
#         Path.__init__(self, travel, width)
#         Interactable.__init__(self, Rect(canva, x1, y1, width, travel, "grey"))

# class Up_Path(Vertical_Path):
#     def __init__(self, canva, x1, y1, width, travel):
#         super().__init__(canva, x1, y1, width, travel)

# class Down_Path(Vertical_Path):
#     def __init__(self, canva, x1, y1, width, travel):
#         super().__init__(canva, x1, y1, width, travel)
        





    '''
    Path should be nodes, the nodes are in the middle of the path
    Path will be splitted into up path, down path, right path and left path
    The type of path will dictate which direction the enemy will move
    '''
