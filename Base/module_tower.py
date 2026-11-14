from Base.Entity import Entity
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
from Base.debuff import EffectType
from Base.rect import Rect

@dataclass(frozen=True)
class DpsStats:
    '''Stats for towers that can shoot'''
    damage: float | int 
    # === How much damage dealt per shot
    fire_rate: float | int
    # === How fast the tower shoots


@dataclass(frozen=True)
class DebuffStats:
    '''Stats for towers that can apply debuff on damaging enemies'''
    type: EffectType
    # === What type of debuff it is: Freeze / Burn
    magnitude: float | int
    # === How strong the debuff is ===
    duration: float | int
    # === How long the debuff is applied ===

@dataclass(frozen=True)
class IncomeStats:
    '''Stats for towers that can bring income'''
    income: int

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

class Tower(Entity, ABC): 
    '''Physical Tower summoned using the infromation from the class TowerInfo, TowerManager performs the summoning.'''
    def __init__(self, TowerInfo: TowerInfo, rect: Rect) -> None:
        self.__name=TowerInfo.name
        self.__cost=TowerInfo.cost
        self.__color=TowerInfo.color
        self.__act_range=TowerInfo.act_range
        self.__size=TowerInfo.size
        super().__init__(rect)
        self.__last_act=0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def size(self) -> int | float:
        return self.__size

    # =====
    @property
    def last_act(self) -> int | float:
        return self.__last_act
    @last_act.setter
    def last_act(self, value: int | float) -> None:
        self.__last_act=value
    # =====
    @property
    def cost(self) -> int: 
        return self.__cost
    @cost.setter
    def cost(self, value: int) -> None:
        if isinstance(value, int) and value>0:
            self.__cost=value
    # =====
    @property
    def color(self) -> str:
        return self.__color

    # =====
    @property
    def act_range(self) -> int | float:
        return self.__act_range
    @act_range.setter
    def act_range(self, value: int | float) -> None:
        if isinstance(value, int) or isinstance(value, float):
            self.__act_range=value
    # =====
    def cooldown_check(self) -> bool:
        '''Check if enough time has passed for the tower to shoot again'''
        current_time=time.monotonic()
        if current_time-self.__last_act<self.fire_rate:
            return False
        self.__last_act=current_time
        return True 

    # ======
    @abstractmethod
    def act(self) -> None:
        '''Each tower type has its own action'''
        pass
        

class DpsTower(Tower):
    '''Tower that can shoot'''
    def __init__(self, TowerInfo: TowerInfo, rect: Rect) -> None:
        super().__init__(TowerInfo, rect)
        self.__damage=TowerInfo.dps.damage
        self.__fire_rate=TowerInfo.dps.fire_rate

    # ======
    @property
    def fire_rate(self) -> int | float:
        return self.__fire_rate

    @fire_rate.setter
    def fire_rate(self, value: int | float) -> None:
        if value>0 and (isinstance(value, float) or isinstance(value, int)):
            self.__fire_rate=value
    # ======
    @property
    def damage(self) -> int | float:
        return self.__damage
    @damage.setter
    def damage(self, value: int | float) -> None:
        if isinstance(value, int):
            self.__damage=value
    # ======
    def act(self) -> None | int | float:
        '''Expose the output damage for the enemies to process'''
        current_time=time.time()
        delta_time=current_time-self.last_act
        if delta_time>=self.__fire_rate:
            self.last_act=current_time
            return self.__damage


class DebuffTower(DpsTower):
    '''Tower that can shoot and apply debuff with it'''
    def __init__(self, TowerInfo: TowerInfo, rect: Rect) -> None:
        super().__init__(TowerInfo, rect)
        self.__type=TowerInfo.debuff.type
        self.__magnitude=TowerInfo.debuff.magnitude
        self.__duration=TowerInfo.debuff.duration

    @property
    def type(self) -> EffectType:
        return self.__type

    # =====
    @property
    def magnitude(self) -> int | float:
        return self.__magnitude
    @magnitude.setter
    def magnitude(self, value: int | float) -> None:
        if isinstance(value, (float, int)):
            self.__magnitude=value
    # =====
    @property
    def duration(self) -> int | float:
        return self.__duration
    @duration.setter
    def duration(self, value: int | float) -> None:
        if isinstance(value, (float, int)):
            self.__duration=value
    # =====

    def act(self) -> None | int | float:
        return super().act()


class Farm(Tower):
    '''Tower that makes money'''
    def __init__(self, TowerInfo: TowerInfo, rect: Rect) -> None:
        super().__init__(TowerInfo, rect)
        self.__income=TowerInfo.income.income

    # =====
    @property
    def income(self) -> int:
        return self.__income
    @income.setter
    def income(self, value: int | float) -> None:
        if isinstance(value, int):
            self.__income=value
    # =====
    def act(self) -> None:
        '''The tower only action is existing, its number in the game will count towards how much money is gained per wave'''
        return None
