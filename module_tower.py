from rect import Rect
from interactable import Interactable
import time
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
        self.__last_act=0

    @property
    def rect(self):
        return self.__rect
    @property
    def last_act(self):
        return self.__last_act
    @last_act.setter
    def last_act(self, value):
        self.__last_act=value

    def cooldown_check(self):
        current_time=time.monotonic()
        if current_time-self.__last_act<self.__fire_rate:
            return False
        self.__last_act=current_time
        '''Has already done cooling down'''
        return True 
    


    def act(self):
        pass #Start shooting