from rect import Rect
import module_tower
from interactable import Interactable

class Slot(Interactable):
    def __init__(self, rect, tower=None):
        super().__init__(rect)
        self.__tower=tower
    #if towerId=None, uninteractable
    
    @property
    def tower(self):
        return self.__tower

    @tower.setter
    def tower(self, value):
        if isinstance(value, int):
            self.__tower=value




