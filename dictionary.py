from Base.enemy import Enemy, Enemy_Info
from Base.module_tower import TowerInfo, Tower, EffectType, DpsStats, DebuffStats, IncomeStats, SupportStats
from Base.module_tower import DpsTower, DebuffTower, Farm, SupportTower
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
    
class Enemy_Dictionary(Dictionary):
    def __init__(self):
        super().__init__()

    def add(self, name, key, health, speed, color, width, height):
        item=Enemy_Info(name, health, speed, color, width, height)
        self.dictionary[key]=item

class Tower_Dictionary(Dictionary):
    def __init__(self):
        super().__init__()

    def add(self, type, key, name, cost, color, act_range, size, dps=None, debuff=None, support=None, income=None):
        if type == "dps":
            item=TowerInfo(name, cost, color, act_range, size, dps)
        elif type == "debuff":
            item=TowerInfo(name, cost, color, act_range, size, dps, debuff)
        elif type =="support":
            item=TowerInfo(name, cost, color, act_range, size, support=support)
        elif type =="income":
            item=TowerInfo(name, cost, color, act_range, size, income=income)
        self.dictionary[key]=[type,item]

    def get(self,key):
        packet=super().get(key)
        return packet[1]


    def summon_tower(self, key, rect):
        tower_type=self.dictionary[key][0]
        tower_info=self.dictionary[key][1]

        if tower_type=="dps":
            tower=DpsTower(tower_info, rect)
        elif tower_type=="debuff":
            tower=DebuffTower(tower_info, rect)
        elif tower_type=="support":
            tower=SupportTower(tower_info, rect)
        elif tower_type=="income":
            tower=Farm(tower_info, rect)
        return tower
        
Ebook=Enemy_Dictionary()

Ebook.add("normal", 1, 10, 0.5, "green", 30, 30)
Ebook.add("swift", 2, 12, 1, "lime", 26, 26)
Ebook.add("heavy", 3, 60, 0.25, "black", 32, 32)
Ebook.add("Normal Boss", 4, 200, 0.5, "red", 35,35)

Tbook=Tower_Dictionary()

Tbook.add(type="dps", key=1, name="soldier", cost=200, color="red", act_range=200, size=20, dps=DpsStats(5, 0.5))
Tbook.add(type="debuff", key=2, name="freezer", cost=200, color="blue", act_range=200, size=20, dps=DpsStats(5, 0.8), debuff=DebuffStats(EffectType.FROZEN,1,0.2))
Tbook.add(type="dps", key=3, name="minigunner", cost=400, color="pink", act_range=300, size=25, dps=DpsStats(7,0.25))
Tbook.add(type="income", key=4, name="farm", cost=200, color="yellow", act_range=10, size=20, income=IncomeStats(100))
