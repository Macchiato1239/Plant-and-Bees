from rect import Rect
from interactable import Interactable

class Spawn(Interactable):
    def __init__(self, rect):
        super().__init__(rect)

class Base(Interactable):
    def __init__(self, rect, health):
        super().__init__(rect)
        self.__health=health

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if isinstance(value, int):
            self.__health=max(0,value)


class Path:
    def __init__(self):
        pass
    '''Path should be nodes, the nodes are in the middle of the path'''