from rect import Rect
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