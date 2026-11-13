import time
import tkinter as tk
from Head.states import GameState
from Base.buildings import Buildings
from Manager.collision import CollisionManager
from Manager.display import Display
from Manager.enemymanager import EnemyManager
from Manager.hotbarmanager import HotBarManager
from Manager.mouseevent import MouseHandler
from Manager.towermanager import TowerManager


class GameFlow(GameState):
    '''Create the game and coordinate its frame-by-frame flow.'''
    def __init__(self, window, difficulty):
        super().__init__(window)
        canvas = self.window.canva
        self.__paused=False

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
        self.__enemies = EnemyManager(canvas, difficulty, self.__buildings.spawn, self.__buildings.path_points)
        self.__display = Display(canvas, self.__money, self.__base_health, len(self.__enemies.game_info))
        self.__mouse_handler = MouseHandler(self)

    def enter(self):
        self.__paused = False
        self.__last_time = time.time()

    def exit(self):
        self.__paused = True

    def create_game_loop(self):
        # === Create slots ===
        self.__hotbar.create_slots()
        # === Equip towers ===
        for tower_id in (1, 2, 3, 4):
            self.__hotbar.equip_tower(tower_id)
        # === Signal which slot is empty ===
        self.__hotbar.update_colors()

        # === Bind input events to corressponding functions ===
        self.window.window.bind("<KeyPress>", self.__mouse_handler.on_key_press, add="+")
        self.window.window.bind("<Button-1>", self.__mouse_handler.interact_with_ui, add="+")
        self.window.canva.bind("<Motion>", self.__mouse_handler.track_display_range)

        # === Render the base and spawn on top of everything ===
        self.window.canva.tag_raise(self.__buildings.spawn.rect.rect_id)
        self.window.canva.tag_raise(self.__buildings.base.rect.rect_id)

        # === Immediately trigger game loop ===
        self.game_loop()

    def game_loop(self):
        if not self.window.running:
            self.window.window.destroy()
            return
        if not self.__paused:
            # === Get Delta Time ===
            self.__current_time = time.time()
            delta_time = self.__current_time - self.__last_time
            self.__last_time = self.__current_time

            # === Process enemies movement, death and debuff ===
            reward = self.__enemies.update(delta_time, self.window.canva)
            self.__money += reward
            self.__base_health = max(0, self.__base_health - self.__enemies.base_damage)
            self.__enemies.base_damage = 0

            # === Process tower actions
            self.__towers.update(self.__enemies.active_enemies, self.__collision)

            # === Update money, base health and wave number
            self.__display.money_display = self.__money
            self.__display.health_display = self.__base_health
            self.__display.wave_display = self.__enemies.display_wave

        # Keep checking while paused so the game can resume, and while playing
        # to process the next frame.
        self.window.window.after(16, self.game_loop)

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
            self.window.running = False
        elif event.keysym.lower() == "x":
            # === Stop selecting the selected tower ===
            self.__towers.cancel_selection()

    def update_range_display(self, event):
        tower_info = self.__towers.selected_tower_info
        self.__display.show_range(event.x, event.y, tower_info)


