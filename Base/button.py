from Base.Entity import Entity
from Base.rect import Rect

class Button(Entity):
    '''Rectangle that triggers an event on click'''
    def __init__(self, canva, cord_x: int, cord_y: int, width: int, height: int, text="", fill="#bd7e1a", outline="#613c01", border_width=1) -> None:
        self.__canva = canva

        # === The rendered rectangle ===
        super().__init__(Rect(
            canva, cord_x-width/2, 
            cord_y-height/2, 
            width, 
            height, 
            fill, 
            outline, 
            border_width))

        # === The rendered text ===
        self.__text=canva.create_text(
            cord_x, cord_y, text=text, font=("Arial", 15, "bold"), fill="black", state="hidden"
        )
    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        self.__canva.itemconfig(self.__text, text=value)
    @property
    def rect_id(self) -> int:
        return self.rect.rect_id
