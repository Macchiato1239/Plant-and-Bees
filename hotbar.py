from rect import Rect
import module_tower
from interactable import Interactable

class Slot(Interactable):
    def __init__(self, rect, tower=None):
        super().__init__(rect)
        self.__tower=tower
    #if tower=None, uninteractable
    
    @property
    def tower(self):
        return self.__tower

    @tower.setter
    def tower(self, value):
        if isinstance(value, module_tower.Tower):
            self.__tower=value




# class Slot():
#     def __init__(self, num):

#         self.__start_pos_x=150
#         self.__start_pos_y=570
#         self.__slot_width=120
#         self.__slot_height=150
#         super().__init__(self.__start_pos_x*(num)+10*(num-1),
#                         self.__start_pos_y,
#                         self.__start_pos_x*num+10*(num-1)+self.__slot_width,
#                         self.__start_pos_y+self.__slot_height, 
#                         fill="red")        
#         #Slot should contain information about the tower it stores
# class Inventory():
#     def __init__(self, canva):
#         self.__canva=canva
#         self.__slots=[]

#     def add_tower(self, tower_value):
#         if isinstance(tower_value, tower.Tower):
#             self.__slots.append(tower_value)
#             if len(self.__slots)>5:
#                 self.__slots.pop(0)

#     def render(self):
#         for i in range(len(self.__slots)):
#             slot=Slot(i+1)
#             slot.render(self.__canva)

#     @property
#     def slots(self):
#         return self.__slots

