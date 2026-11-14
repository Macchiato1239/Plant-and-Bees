from Base.enemy import Enemy, Enemy_Info
from Base.module_tower import TowerInfo, Tower, EffectType, DpsStats, DebuffStats, IncomeStats
from Base.module_tower import DpsTower, DebuffTower, Farm
from abc import ABC, abstractmethod
class Dictionary(ABC):
    '''Quite self-explanatory huh'''
    def __init__(self):
        self.__dictionary={}

    @property
    def dictionary(self):
        return self.__dictionary

    @abstractmethod
    def add():
        pass

    def get(self, key):
        '''Retrieve an item, adding context to unknown-key errors.'''
        try:
            return self.__dictionary[key]
        except KeyError as error:
            raise KeyError(
                f"{type(self).__name__} has no entry for key {key!r}"
            ) from error
        except TypeError as error:
            raise TypeError("Dictionary keys must be hashable") from error
    
class Enemy_Dictionary(Dictionary):
    '''Contains all enemy information'''
    def __init__(self):
        super().__init__()

    def add(self, name, key, health, speed, color, width, height):
        '''Create and add a new enemy to the dictionary'''
        item=Enemy_Info(name, health, speed, color, width, height)
        self.dictionary[key]=item

class Tower_Dictionary(Dictionary):
    '''Contains all tower information'''
    def __init__(self):
        super().__init__()

    def add(self, type, key, name, cost, color, act_range, size, dps=None, debuff=None, support=None, income=None):
        '''Create and add a new tower to the dictionary'''
        if type == "dps":
            item=TowerInfo(name, cost, color, act_range, size, dps)
        elif type == "debuff":
            item=TowerInfo(name, cost, color, act_range, size, dps, debuff)
        elif type =="income":
            item=TowerInfo(name, cost, color, act_range, size, income=income)
        else:
            raise ValueError(f"Unsupported tower type: {type!r}")
        self.dictionary[key]=[type,item]

    def get(self,key):
        ''' Retrieve the request tower'''
        packet=super().get(key)
        return packet[1]


    def summon_tower(self, key, rect):
        '''Summon the requested tower'''
        try:
            tower_type, tower_info = self.dictionary[key]
        except KeyError as error:
            raise KeyError(f"Unknown tower ID: {key!r}") from error

        try:
            if tower_type == "dps":
                return DpsTower(tower_info, rect)
            if tower_type == "debuff":
                return DebuffTower(tower_info, rect)
            if tower_type == "income":
                return Farm(tower_info, rect)
        except AttributeError as error:
            raise AttributeError(
                f"Tower {key!r} is missing stats required for type {tower_type!r}"
            ) from error
        raise ValueError(f"Tower {key!r} has unsupported type {tower_type!r}")
        
Ebook=Enemy_Dictionary()

Ebook.add("Normal", 1, 6, 0.5, "#baff7d", 20, 20)
Ebook.add("Quick", 2, 8, 1, "#43adc4", 20, 20)
Ebook.add("Heavy", 3, 30, 0.4, "#63838a", 25, 25)
Ebook.add("Abnormal", 4, 12, 0.5, "#7cb24d", 22,22)
Ebook.add("Swift", 5, 20, 1.2, "#145463", 22, 22)
Ebook.add("Elite abnormal", 6, 150, 0.5, "#076f00", 27, 27)
Ebook.add("Speedy Boss", 7, 500, 0.8, "#005e94", 30, 30)
Ebook.add("Giant Boss", 8, 2000, 0.2, "black", 35, 35)

Tbook=Tower_Dictionary() 

Tbook.add(type="dps", key=1, name="soldier", cost=250, color="red", act_range=150, size=20, dps=DpsStats(10, 0.5))
Tbook.add(type="debuff", key=2, name="freezer", cost=400, color="blue", act_range=150, size=20, dps=DpsStats(5, 0.8), debuff=DebuffStats(EffectType.FROZEN,1,0.4))
Tbook.add(type="dps", key=3, name="minigunner", cost=2000, color="pink", act_range=250, size=25, dps=DpsStats(15,0.2))
Tbook.add(type="income", key=4, name="farm", cost=200, color="yellow", act_range=10, size=20, income=IncomeStats(100))
Tbook.add(type="debuff", key=5, name="Pyro", cost=500, color="orange", act_range=80, size=20, dps=DpsStats(2, 0.6), debuff=DebuffStats(EffectType.BURN, 3, 20, tick=0.5))
