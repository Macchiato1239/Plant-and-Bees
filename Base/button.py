from Base.interactable import Interactable
from Base.rect import Rect
class Button(Interactable):
    def __init__(self, canva, cord_x, cord_y, width, height, text="", fill="#bd7e1a", outline="#613c01", border_width=1):
        self.__canva = canva
        super().__init__(Rect(canva, cord_x-width/2, cord_y-height/2, width, height, fill, outline, border_width))
        self.__text=canva.create_text(
            cord_x, cord_y, text=text, font=("Arial", 15, "bold"), fill="black", state="hidden"
        )
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__canva.itemconfig(self.__text, text=value)
    @property
    def rect_id(self):
        return self.rect.rect_id
