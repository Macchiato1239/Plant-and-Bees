from Base.button import Button
from dictionary import Tbook

class Slot(Button):
    def __init__(self, canvas, cord_x, cord_y, width, height, tower=None, fill="black"):
        super().__init__(canvas, cord_x, cord_y, width, height, fill=fill, text="None")
        self.__tower = None
        canvas.itemconfig(self.text, state="normal")
        self.tower = tower
    
    @property
    def tower(self):
        return self.__tower

    @tower.setter
    def tower(self, value):
        if value is None or isinstance(value, int):
            self.__tower=value
            self.text = "None" if value is None else Tbook.get(value).name




