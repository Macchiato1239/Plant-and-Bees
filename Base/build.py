from Base.rect import Rect
from Base.entity import Entity

class Spawn(Entity):
    '''Where enemy spawns'''
    def __init__(self, canva, x: int, y: int) -> None:
        self.__width=25
        self.__height=25
        self.__color="#2b1b00"
        super().__init__(Rect(canva, x-self.__width, y-self.__height, self.__width*2, self.__height*2, self.__color))


class Base(Entity):
    '''Must prevent enemies from reach this'''
    def __init__(self, canva, health: int, x: int, y: int) -> None:
        self.__width=25
        self.__height=25
        self.__color="#2c919d"
        super().__init__(Rect(canva, x-self.__width, y-self.__width, self.__width*2, self.__height*2, self.__color))
        self.__health=health

    @property
    def health(self) -> int | float:
        return self.__health

    @health.setter
    def health(self, value: int | float) -> None:
        if isinstance(value, int):
            # === Health can not drop below 0 ===
            self.__health=max(0,value)

class Path(Entity):
    '''The paths enemy must travel to get to player'base'''
    def __init__(self, canva, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        # === Coordinate of path ===
        self.__start_x=start_x
        self.__start_y=start_y
        self.__end_x=end_x
        self.__end_y=end_y

        self.__path_width=25

        # === Determining the width and height of path ===
        x1=min(start_x, end_x)-self.__path_width
        y1=min(start_y, end_y)-self.__path_width
        width=self.__path_width*2 + abs(start_x-end_x)
        height=self.__path_width*2 + abs(start_y-end_y)
        path=Rect(canva, x1, y1, width, height, fill="#ba7f20", outline="#6b4405", border_width=3)
        super().__init__(path)

    @property
    def start_x(self) -> int:
        return self.__start_x

    @property
    def start_y(self) -> int:
        return self.__start_y

    @property
    def end_x(self) -> int:
        return self.__end_x

    @property
    def end_y(self) -> int:
        return self.__end_y

