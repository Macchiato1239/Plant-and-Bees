from Base.button import Button
from dictionary import Tbook
from Base.module_tower import TowerInfo

class Slot(Button):
    '''Contains equipped towers, interact to select a tower for next placement'''
    def __init__(self, canvas, cord_x: int, cord_y: int, width: int, height: int, tower=None, fill="black") -> None:
        super().__init__(canvas, cord_x, cord_y, width, height, fill=fill, text="None")
        self.__tower = None
        canvas.itemconfig(self.text, state="normal")
        self.tower = tower
    
    @property
    def tower(self) -> TowerInfo:
        return self.__tower

    @tower.setter
    def tower(self, value: TowerInfo) -> None:
        if value is None or isinstance(value, int):
            self.__tower=value
            self.text = "None" if value is None else Tbook.get(value).name




