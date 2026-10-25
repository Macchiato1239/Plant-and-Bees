from rect import Rect
from interactable import Interactable
'''
Tower_Card contains the information about the default stats and abilities of the tower'''
class Tower_Card():
    def __init__(self, name, cost, color, damage, fire_rate, act_range, size=30):
        self.__name=name
        self.__cost=cost
        self.__color=color
        self.__damage=damage
        self.__fire_rate=fire_rate
        self.__act_range=act_range
        self.__size=size 

    @property
    def name(self):
        return self.__name

    @property
    def cost(self):
        return self.__cost
    @cost.setter
    def cost(self, value):
        if isinstance(value, int) and value>0:
            self.__cost=value

    @property
    def color(self):
        return self.__color

    @property
    def size(self):
        return self.__size

    @property
    def fire_rate(self):
        return self.__fire_rate

    @fire_rate.setter
    def fire_rate(self, value):
        if value>0 and (isinstance(value, float) or isinstance(value, int)):
            self.__fire_rate=value

    @property
    def act_range(self):
        return self.__act_range
    @act_range.setter
    def act_range(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self.__act_range=value

    @property
    def damage(self):
        return self.__damage
    @damage.setter
    def damage(self, value):
        if isinstance(value, int):
            self.__damage=value


'''
Tower_Manifested are the towers that are placed down, therefore a manifestation of the info card'''
class Tower_Manifested(Tower_Card): 
    def __init__(self, name, cost, color, damage, fire_rate, act_range, rect):
        super().__init__(name, cost, color, damage, fire_rate, act_range)
        self.__rect=rect
        self.__cord_x=self.__rect.x1+self.__rect.width/2
        self.__cord_y=self.__rect.y1+self.__rect.height/2

    @property
    def rect(self):
        return self.__rect

    @property
    def cord_x(self):
        return self.__cord_x

    @property
    def cord_y(self):
        return self.__cord_y