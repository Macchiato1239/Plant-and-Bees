import tkinter as tk
class Window:
    def __init__(self):
        '''Creates a window and manages UI'''
        self.__window_width = 1000
        self.__window_height = 700
        self.__bg_color = "white"
        self.__window = tk.Tk()
        self.__running = True
        self.__canva = tk.Canvas(
            self.__window,
            width=self.__window_width,
            height=self.__window_height,
            bg=self.__bg_color
        )

    def create_window(self):
        '''Creates a window'''
        self.__window.geometry(
            f"{self.__window_width}x{self.__window_height}"
        )
        self.__canva.pack()
    
    @property
    def window_width(self):
        return self.__window_width
    
    @window_width.setter
    def window_width(self, value):
        if isinstance(value, int):
            self.__window_width=value

    @property
    def window_height(self):
        return self.__window_height
    
    @window_height.setter
    def window_height(self, value):
        if isinstance(value, int):
            self.__window_height = value

    @property
    def bg_color(self):
        return self.__bg_color
    
    @bg_color.setter
    def bg_color(self, value):
        if isinstance(value, str):
            self.__bg_color = value

    @property
    def window(self):
        return self.__window

    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self, value):
        if isinstance(value, bool):
            self.__running = value

    @property
    def canva(self):
        return self.__canva