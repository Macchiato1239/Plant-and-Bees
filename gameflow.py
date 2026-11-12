import time
import tkinter as tk
from buildings import Buildings
from collision import CollisionManager
from display import Display
from enemymanager import EnemyManager
from hotbarmanager import HotBarManager
from module_window import Window
from mouseevent import MouseHandler
from towermanager import TowerManager


class GameFlow:
    '''Create the game and coordinate its frame-by-frame flow.'''
    def __init__(self):
        self.__window = Window()
        canvas = self.__window.canva

        self.__base_health = 100
        self.__starting_money = 750
        self.__money = self.__starting_money

        self.__last_time = time.time()
        self.__current_time = self.__last_time

        self.__collision = CollisionManager()
        self.__buildings = Buildings(canvas, self.__base_health)
        self.__collision.taken.extend(
            [self.__buildings.spawn.rect, self.__buildings.base.rect]
        )
        for path in self.__buildings.paths:
            self.__collision.taken.append(path.rect)

        self.__hotbar = HotBarManager(canvas, self.__collision)
        self.__towers = TowerManager(canvas, self.__collision)
        self.__enemies = EnemyManager(canvas, self.__buildings.spawn, self.__buildings.path_points)
        self.__display = Display(canvas, self.__money, self.__base_health, len(self.__enemies.mode))
        self.__mouse_handler = MouseHandler(self)

    def create_game_loop(self):
        self.__window.create_window()

        # === Create slots ===
        self.__hotbar.create_slots()
        # === Equip towers ===
        for tower_id in (1, 2, 3, 4):
            self.__hotbar.equip_tower(tower_id)
        # === Signal which slot is empty ===
        self.__hotbar.update_colors()

        # === Bind input events to corressponding functions ===
        self.__window.window.bind("<KeyPress>", self.__mouse_handler.on_key_press)
        self.__window.window.bind("<Button-1>", self.__mouse_handler.interact_with_ui)
        self.__window.canva.bind("<Motion>", self.__mouse_handler.track_display_range)

        # === Render the base and spawn on top of everything ===
        self.__window.canva.tag_raise(self.__buildings.spawn.rect.rect_id)
        self.__window.canva.tag_raise(self.__buildings.base.rect.rect_id)

        # === Immediately trigger game loop ===
        self.game_loop()
        # === Trigger tkinter main event loop that processes input events ===
        self.__window.window.mainloop()

    def game_loop(self):
        if not self.__window.running:
            self.__window.window.destroy()
            return
        # === Get Delta Time ===
        self.__current_time = time.time()
        delta_time = self.__current_time - self.__last_time
        self.__last_time = self.__current_time

        # === Process enemies movement, death and debuff ===
        reward = self.__enemies.update(delta_time, self.__window.canva)
        self.__money += reward
        self.__base_health = max(0, self.__base_health - self.__enemies.base_damage)

        # === Process tower actions
        self.__towers.update(self.__enemies.active_enemies, self.__collision)

        # === Update money, base health and wave number
        self.__display.money_display = self.__money
        self.__display.health_display = self.__base_health
        self.__display.wave_display = self.__enemies.display_wave

        # === Recall itself after 16 miliseconds ===
        self.__window.window.after(16, self.game_loop)

    def handle_click(self, event):
        x, y = event.x, event.y
        item = self.__collision.interactive_at(x, y)
        if item is not None:
            if self.__hotbar.contains(item):
                self.__towers.select_tower_card(item.tower)
                return

        if self.__collision.compare_cord_rect(x, y, self.__collision.taken):
            return

        placed, remaining_money = self.__towers.place_tower(x, y, self.__money)
        if placed:
            self.__money = remaining_money

    def handle_key(self, event):
        if event.keysym.lower() == "q":
            # === Quit the game ===
            self.__window.running = False
        elif event.keysym.lower() == "x":
            # === Stop selecting the selected tower ===
            self.__towers.cancel_selection()

    def update_range_display(self, event):
        tower_info = self.__towers.selected_tower_info
        self.__display.show_range(event.x, event.y, tower_info)


