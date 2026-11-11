from enemy import Enemy, Enemy_Info
from module_tower import Tower_Info, Tower
from abc import ABC, abstractmethod
class Dictionary(ABC):
    def __init__(self):
        self.__dictionary={}

    @property
    def dictionary(self):
        return self.__dictionary

    @abstractmethod
    def add():
        pass

    def get(self, key):
        return self.__dictionary[key]
class Tower_Dictionary(Dictionary):
    def __init__(self):
        super().__init__()

    def add(self, name, key, cost, color, damage, fire_rate, act_range, size=20):
        item=Tower_Info(name, cost, color, damage, fire_rate, act_range, size=20)
        self.dictionary[key]=item
    
class Enemy_Dictionary(Dictionary):
    def __init__(self):
        super().__init__()

    def add(self, name, key, health, speed, color, width, height):
        item=Enemy_Info(name, health, speed, color, width, height)
        self.dictionary[key]=item

Ebook=Enemy_Dictionary()
Ebook.add("normal", 1, 10, 0.5, "green", 30, 30)
Ebook.add("swift", 2, 12, 1, "lime", 26, 26)
Ebook.add("heavy", 3, 60, 0.25, "black", 32, 32)

Tbook=Tower_Dictionary()
Tbook.add("soldier", 1, 200, "red", 5, 0.5, 100, 20)
Tbook.add("freezer", 2, 250, "blue", 4, 0.6, 150, 20)
