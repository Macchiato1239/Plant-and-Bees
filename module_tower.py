from rect import Rect
class Tower:
    def __init__(self, name, cost, color, size=30):
        self.__name=name
        self.__cost=cost
        self.__color=color
        self.__size=size 
        '''Size is half the square radius'''

    @property
    def name(self):
        return self.__name

    @property
    def cost(self):
        return self.__cost

    @property
    def color(self):
        return self.__color

    @property
    def size(self):
        return self.__size

# from rect import Rect
# class Tower():
#     def __init__(self, cost, range_rad, occupy):
#         super().__init__()
#         self.__cost=cost
#         self.__range=range_rad
#         self.__occupy=occupy #space taken when placed down
#         pass

#     @property
#     def cost(self):
#         return self.__cost

#     @property
#     def range_rad(self):
#         return self.__range_rad

#     @property
#     def occupy(self):
#         return self.occupy


# #--
# class dps_Tower(Tower):
#     def __init__(self, cost, range_rad, occupy, attack_rate, dmg):
#         super().__init__(cost, range_rad, occupy)
#         self.__attack_rate=attack_rate
#         self.__dmg=dmg
#         self.__occupy=occupy

#     @property
#     def attack_rate(self):
#         return self.__attack_rate

#     @property
#     def dmg(self):
#         return self.__dmg

#     @property
#     def occupy(self):
#         return self.__occupy


# class aoe_dps_Tower(dps_Tower):
#     def __init__(self, cost, range_rad, occupy, attack_rate, dmg, aoe_rad):
#         super().__init__(cost, range_rad, occupy, attack_rate, dmg)
#         self.__aoe_rad=aoe_rad

#     @property 
#     def aoe_rad(self):
#         return self.__aoe_rad

# class single_dps_Tower(dps_Tower):
#     def __init__(self, cost, range_rad, occupy, attack_rate, dmg):
#         super().__init__(cost, range_rad, occupy, attack_rate, dmg)
# #--




# class debuff_tower(Tower):
#     pass

# class support_tower(Tower):
#     pass





# class farm(Tower):
#     def __init__(self, cost, range_rad, occupy, honey):
#         super().__init__(cost, range_rad, occupy)
#         self.__honey=honey
