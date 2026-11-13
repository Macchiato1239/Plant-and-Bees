from Base.interactable import Interactable
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
from Base.debuff import EffectType
@dataclass(frozen=True)
class DpsStats:
    damage: float | int 
    fire_rate: float | int

@dataclass(frozen=True)
class DebuffStats:
    type: EffectType
    magnitude: float | int
    duration: float | int

@dataclass(frozen=True)
class IncomeStats:
    income: int

@dataclass(frozen=True)
class SupportStats:
    fire_rate: float | int
    cost: int
    act_range: float | int
    damage: float | int

@dataclass(frozen=True)
class TowerInfo():
    '''Contains the information about the default stats and abilities of the tower'''
    name: str
    cost: int
    color: str
    act_range: float | int
    size: float | int

    dps: DpsStats | None=None
    debuff: DebuffStats | None=None
    income: IncomeStats | None=None
    support: SupportStats | None=None


class Tower(Interactable, ABC): 
    '''Tower_Manifested are the towers that are placed down, therefore a manifestation of the info card'''
    def __init__(self, TowerInfo, rect):
        self.__name=TowerInfo.name
        self.__cost=TowerInfo.cost
        self.__color=TowerInfo.color
        self.__act_range=TowerInfo.act_range
        self.__size=TowerInfo.size
        super().__init__(rect)
        self.__last_act=0

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return self.__size
    
    @property
    def last_act(self):
        return self.__last_act
    
    @last_act.setter
    def last_act(self, value):
        self.__last_act=value

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
    def act_range(self):
        return self.__act_range
    @act_range.setter
    def act_range(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self.__act_range=value

    def cooldown_check(self):
        current_time=time.monotonic()
        if current_time-self.__last_act<self.fire_rate:
            return False
        self.__last_act=current_time
        return True 
    
    @abstractmethod
    def act(self):
        pass
        

class DpsTower(Tower):
    def __init__(self, TowerInfo, rect):
        super().__init__(TowerInfo, rect)
        self.__damage=TowerInfo.dps.damage
        self.__fire_rate=TowerInfo.dps.fire_rate

    @property
    def fire_rate(self):
        return self.__fire_rate

    @fire_rate.setter
    def fire_rate(self, value):
        if value>0 and (isinstance(value, float) or isinstance(value, int)):
            self.__fire_rate=value

    @property
    def damage(self):
        return self.__damage
    @damage.setter
    def damage(self, value):
        if isinstance(value, int):
            self.__damage=value

    def act(self):
        current_time=time.time()
        delta_time=current_time-self.last_act
        if delta_time>=self.__fire_rate:
            self.last_act=current_time
            return self.__damage


class DebuffTower(DpsTower):
    def __init__(self, TowerInfo, rect):
        super().__init__(TowerInfo, rect)
        self.__type=TowerInfo.debuff.type
        self.__magnitude=TowerInfo.debuff.magnitude
        self.__duration=TowerInfo.debuff.duration

    @property
    def type(self):
        return self.__type

    @property
    def magnitude(self):
        return self.__magnitude
    
    @magnitude.setter
    def magnitude(self, value):
        if isinstance(value, (float, int)):
            self.__magnitude=value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if isinstance(value, (float, int)):
            self.__duration=value
    def act(self):
        damage=super().act()
        return damage


class Farm(Tower):
    def __init__(self, TowerInfo, rect):
        super().__init__(TowerInfo, rect)
        self.__income=TowerInfo.income.income

    @property
    def income(self):
        return self.__income
    @income.setter
    def income(self, value):
        if isinstance(value, int):
            self.__income=value

    def act(self):
        return None
