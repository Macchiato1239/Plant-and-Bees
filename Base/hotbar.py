from Base.button import Button
from dictionary import Tbook

class Slot(Button):
    '''Contains equipped towers, interact to select a tower for next placement'''
    def __init__(self, canvas, cord_x: int, cord_y: int, width: int, height: int, tower=None, fill="black") -> None:
        super().__init__(canvas, cord_x, cord_y, width, height, fill=fill, text="None")
        self.__canvas = canvas
        self.__tower = None
        # === Display the tower's dps ===
        self.__tower_dps = canvas.create_text(
            cord_x, cord_y - 10, text="", font=("Arial", 12, "bold"),
            fill="black", state="hidden"
        )
        # === Display the tower's cost ===
        self.__cost = canvas.create_text(
            cord_x, cord_y + 20, text="", font=("Arial", 12, "bold"),
            fill="black", state="hidden"
        )
        canvas.itemconfig(self.text, state="normal")
        canvas.coords(self.text, cord_x, cord_y - 45)
        self.tower = tower

    @property
    def tower(self) -> int | None:
        return self.__tower

    @tower.setter
    def tower(self, value: int | None) -> None:
        if value is None or isinstance(value, int):
            self.__tower=value
            if value is None:
                self.text = "None"
                self.__canvas.itemconfig(self.__tower_dps, text="", state="hidden")
                self.__canvas.itemconfig(self.__cost, text="", state="hidden")
                return

            tower_info = Tbook.get(value)
            self.text = tower_info.name
            self.__canvas.itemconfig(self.__cost, text=f"Cost: {tower_info.cost}", state="normal")

            if tower_info.dps is None or tower_info.dps.fire_rate <= 0:
                dps_text = "DPS: 0"
            else:
                dps = round(tower_info.dps.damage / tower_info.dps.fire_rate,1)
                dps_text = f"DPS: {dps:g}"
            self.__canvas.itemconfig(self.__tower_dps, text=dps_text, state="normal")




