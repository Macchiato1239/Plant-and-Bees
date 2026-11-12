class Display:
    '''Manages canvas text and preview towers before placement.'''
    def __init__(self, canvas, money, health, wave):
        self.__canvas = canvas
        # === Stats display ===
        self.__money_display = canvas.create_text(
            100, 50, text = f"Cash: {money}", font=("Arial", 24), fill="green")
        self.__health_display = canvas.create_text(
            500, 50, text = f"Health: {health}", font=("Arial", 24), fill="red")
        self.__wave_display = canvas.create_text(
            700, 50, text = f"Wave {wave}", font=("Arial", 20), fill="black")

        # === Placement preview ===
        self.__range_circle = canvas.create_oval(
            0, 0, 0, 0, outline = "black", stipple="gray12", state="hidden")
        self.__space_taken_rect = canvas.create_rectangle(
            0, 0, 0, 0, fill = "orange", outline="black", stipple="gray12", state="hidden")

    @property
    def money_display(self):
        return self.__money_display

    @money_display.setter
    def money_display(self, value):
        self.__canvas.itemconfig(self.__money_display, text=f"Cash: {value}")

    @property
    def health_display(self):
        return self.__health_display

    @health_display.setter
    def health_display(self, value):
        self.__canvas.itemconfig(self.__health_display, text=f"Health: {value}")

    @property
    def wave_display(self):
        return self.__wave_display

    @wave_display.setter
    def wave_display(self, value):
        self.__canvas.itemconfig(self.__wave_display, text=str(value))

    @property
    def range_circle(self):
        return self.__range_circle

    @property
    def space_taken_rect(self):
        return self.__space_taken_rect

    def show_range(self, cord_x, cord_y, tower_info):
        '''Preview range of tower and the space it takes up'''
        if tower_info is None:
            # === If none selected, keeps the two objects hidden ===
            self.__canvas.itemconfigure(self.__range_circle, state="hidden")
            self.__canvas.itemconfigure(self.__space_taken_rect, state="hidden")
            return

        reach = tower_info.act_range/2
        size = tower_info.size

        # === Change the circle's coordinate and size ===
        self.__canvas.coords(
            self.__range_circle,
            cord_x-reach, cord_y-reach, cord_x+reach, cord_y+reach,
        )
        # === Change the rectangle's coordinate and size ===
        self.__canvas.coords(
            self.__space_taken_rect,
            cord_x-size, cord_y-size, cord_x+size, cord_y+size,
        )
        self.__canvas.itemconfigure(self.__range_circle, state="normal")
        self.__canvas.itemconfigure(self.__space_taken_rect, state="normal")
