import tkinter as tk
class Window:
    '''The main window of the game, display everything inside it'''
    def __init__(self) -> None:
        # === Dimensions ===
        self.__window_width = 1000
        self.__window_height = 700
        # === Background color ===
        self.__bg_color = "#a0de81"

        # === The screen ===
        self.__window = tk.Tk()
        self.__running = True

        # === Things drawn onto the screen ===
        self.__canva = tk.Canvas(
            self.__window,
            width=self.__window_width,
            height=self.__window_height,
            bg=self.__bg_color
        )

    def create_window(self) -> None:
        '''Creates a window'''
        self.__window.geometry(
            f"{self.__window_width}x{self.__window_height}"
        )
        self.__canva.pack()

    # === Window's properties ===
    @property
    def window_width(self) -> int:
        return self.__window_width
    
    @window_width.setter
    def window_width(self, value: int) -> None:
        if isinstance(value, int):
            self.__window_width=value

    @property
    def window_height(self) -> int:
        return self.__window_height
    
    @window_height.setter
    def window_height(self, value: int) -> None:
        if isinstance(value, int):
            self.__window_height = value

    @property
    def bg_color(self) -> str:
        return self.__bg_color
    
    @bg_color.setter
    def bg_color(self, value: str) -> None:
        if isinstance(value, str):
            self.__bg_color = value

    # ======
    @property
    def window(self) -> tk.Tk:
        return self.__window

    @property
    def running(self) -> bool:
        return self.__running
    
    @running.setter
    def running(self, value: bool) -> None:
        if isinstance(value, bool):
            self.__running = value

    @property
    def canva(self) -> tk.Canvas:
        return self.__canva