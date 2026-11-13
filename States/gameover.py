from Base.button import Button
from Head.states import GameState
from Manager.collision import CollisionManager


class GameOverState(GameState):
    '''Show a result overlay with menu and restart actions.'''

    def __init__(self, window, title, include_resume=False):
        super().__init__(window)
        self.__canvas = self.window.canva
        width = self.window.window_width
        height = self.window.window_height
        center_x = width / 2
        center_y = height / 2
        
        panel_half_height = 205 if include_resume else 170
        self.__panel = self.__canvas.create_rectangle(
            center_x - 250, center_y - panel_half_height,
            center_x + 250, center_y + panel_half_height,
            fill="white", outline="black", width=3, state="hidden"
        )
        self.__title = self.__canvas.create_text(
            center_x, center_y - 115, text=title, fill="black",
            font=("Arial", 30), state="hidden"
        )
        self.__resume_button = None
        if include_resume:
            self.__resume_button = Button(
                self.__canvas, center_x, center_y - 35, 200, 60, "Resume"
            )
        self.__menu_button = Button(
            self.__canvas, center_x, center_y + (25 if include_resume else 0),
            200, 60, "Main Menu"
        )
        self.__restart_button = Button(
            self.__canvas, center_x, center_y + (85 if include_resume else 65),
            200, 60, "Restart"
        )
        self.__collision = CollisionManager()

        for item_id in self.__item_ids():
            self.__canvas.itemconfigure(item_id, state="hidden")

    def enter(self):
        for item_id in self.__item_ids():
            self.__canvas.itemconfigure(item_id, state="normal")
            self.__canvas.tag_raise(item_id)
        buttons = [self.__menu_button, self.__restart_button]
        if self.__resume_button is not None:
            buttons.insert(0, self.__resume_button)
        self.__collision.interactive = buttons

    def exit(self):
        for item_id in self.__item_ids():
            self.__canvas.itemconfigure(item_id, state="hidden")
        self.__collision.interactive = []

    def handle_click(self, event):
        '''Check if user chose to resume, go to main menu or restart the game'''
        item = self.__collision.interactive_at(event.x, event.y)
        if item is None:
            return None
        if item is self.__resume_button:
            return "resume"
        if item is self.__menu_button:
            return "menu"
        if item is self.__restart_button:
            return "restart"
        return None

    def __item_ids(self):
        item_ids = [
            self.__panel,
            self.__title,
            self.__menu_button.rect_id,
            self.__menu_button.text,
            self.__restart_button.rect_id,
            self.__restart_button.text,
        ]
        if self.__resume_button is not None:
            item_ids.extend((self.__resume_button.rect_id, self.__resume_button.text))
        return tuple(item_ids)
