import time
import tkinter as tk
from typing import Callable
from Head.states import GameState, State
from Manager.buildings import Buildings
from Manager.collision import CollisionManager
from Manager.display import Display
from Manager.enemymanager import EnemyManager
from Manager.hotbarmanager import HotBarManager
from Manager.mouseevent import MouseHandler
from Manager.towermanager import TowerManager


class GameFlow(GameState):
    '''Create the game and coordinate its frame-by-frame flow.'''
    def __init__(self, window: tk.Tk, difficulty: int, finish_game: Callable):
        super().__init__(window)
        self.__on_finish = finish_game
        canvas = self.window.canva
        self.__existing_canvas_items = set(canvas.find_all())
        self.__paused=False
        self.__disposed = False
        self.__after_id = None

        # === Input events ===
        self.__key_binding_id = None
        self.__click_binding_id = None
        self.__motion_binding_id = None

        # === Changable stats during the game flow ===
        self.__base_health = 100
        self.__starting_money = 750
        self.__money = self.__starting_money
        self.__paid_wave_count=0

        # === Used to calculate delta time ===
        self.__last_time = time.time()
        self.__current_time = self.__last_time

        # === Game play's properties managers
        self.__collision = CollisionManager()
        self.__buildings = Buildings(canvas, self.__base_health)
        self.__collision.taken.extend(
            [self.__buildings.spawn.rect, self.__buildings.base.rect]
        )
        self.__hotbar = HotBarManager(canvas, self.__collision)
        self.__towers = TowerManager(canvas, self.__collision)
        self.__enemies = EnemyManager(canvas, difficulty, self.__buildings.spawn, self.__buildings.path_points)

        # === Put the enemies' path into unplaceable place for towers ===
        for path in self.__buildings.paths:
            self.__collision.taken.append(path.rect)

        # === Display manager, responsible for some of the game's UI: Cash, Wave number, base health, time til next wave, etc
        self.__display = Display(canvas, self.__money, self.__base_health, len(self.__enemies.game_info))
        self.__mouse_handler = MouseHandler(self)

    def enter(self) -> None:
        '''Pause the game'''
        self.__paused = False
        self.__last_time = time.time()

    def exit(self) -> None:
        '''Exit the pause state'''
        self.__paused = True
        self.__towers.cancel_selection()

    def cleanup(self) -> None:
        '''Stop the main game flow and remove the canvas items it created.'''
        if self.__disposed:
            return
        self.exit()
        self.__disposed = True
        # === Mark the gameflow as being shut down ===

        if self.__after_id is not None:
            try:
                self.window.window.after_cancel(self.__after_id)
            except tk.TclError:
                pass
            self.__after_id = None
            # === Delete the schedule callback to stop the game loop ===

        # === Unbind every input events with its input functions ===
        bindings = (
            (self.window.window, "<KeyPress>", self.__key_binding_id),
            (self.window.window, "<Button-1>", self.__click_binding_id),
            (self.window.canva, "<Motion>", self.__motion_binding_id),
        )

        for widget, sequence, binding_id in bindings:
            if binding_id is not None:
                widget.unbind(sequence, binding_id)

        for item_id in self.window.canva.find_all():
            if item_id not in self.__existing_canvas_items:
                self.window.canva.delete(item_id)

        # === Clear every collision detections ===
        self.__collision.interactive.clear()
        self.__collision.taken.clear()

    def create_game_loop(self) -> None:
        if self.__disposed:
            return
        # === Create slots ===
        self.__hotbar.create_slots()
        # === Equip towers ===
        for tower_id in (1, 2, 3, 4):
            self.__hotbar.equip_tower(tower_id)
        # === Signal which slot is empty ===
        self.__hotbar.update_colors()

        # === Bind input events to corressponding functions ===
        self.__key_binding_id = self.window.window.bind(
            "<KeyPress>", self.__mouse_handler.on_key_press, add="+"
        )
        self.__motion_binding_id = self.window.canva.bind(
            "<Motion>", self.__mouse_handler.track_display_range
        )

        # === Render the base and spawn on top of everything ===
        self.window.canva.tag_raise(self.__buildings.spawn.rect.rect_id)
        self.window.canva.tag_raise(self.__buildings.base.rect.rect_id)

        # === Immediately trigger game loop ===
        self.game_loop()

    def game_loop(self) -> None:
        self.__after_id = None
        if self.__disposed:
            return
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

            # === Process tower actions ===
            self.__towers.update(
                self.__enemies.active_enemies, self.__collision, delta_time
            )
            
            # === Amount of money gained from farms per wave ===
            completed = self.__enemies.completed_waves
            newly_completed = completed - self.__paid_wave_count

            if newly_completed > 0:
                self.__money += self.__towers.farm_income_per_wave * newly_completed
                self.__paid_wave_count = completed

            # === Update money, base health and wave number
            self.__display.money_display = self.__money
            self.__display.health_display = self.__base_health
            self.__display.wave_display = self.__enemies.display_wave
            self.__display.next_wave_display = self.__enemies.next_wave_countdown

            if self.game_over_check():
                return

        # Keep checking while paused so the game can resume, and while playing
        # to process the next frame.
        self.__after_id = self.window.window.after(16, self.game_loop)

    def handle_click(self, event: tk.Event) -> None:
        '''Handling click inputs'''
        if self.__disposed or self.__paused:
            return
        x, y = event.x, event.y
        item = self.__collision.interactive_at(x, y)
        if item is not None:
            if self.__hotbar.contains(item):
                self.__towers.select_tower_card(item.tower)
                return

        # A click used to place a tower should not also investigate it.
        # Keep placement mode active after invalid placements so the player
        # can choose another spot.
        if self.__towers.current_tower is not None:
            placed, remaining_money = self.__towers.place_tower(x, y, self.__money)
            if placed:
                self.__money = remaining_money
            return

        self.__towers.investigate_tower(event)



    def handle_key(self, event: tk.Event) -> None:
        '''Handle keyboards input'''
        if event.keysym.lower() == "q":
            # === Stop selecting the selected tower ===
            self.__towers.cancel_selection()
        if event.keysym.lower() == "x":
            # === Delete a tower ===
            self.__towers.delete_tower()

    def update_range_display(self, event: tk.Event) -> None:
        '''Update the property of the preview circle when a new tower is selected '''
        tower_info = self.__towers.selected_tower_info
        self.__display.show_range(event.x, event.y, tower_info)

    def game_over_check(self) -> bool:
        '''Check if the game is over, either winning or losing'''
        if self.__base_health <= 0:
            #  === Clear placement mode before handing input over to the result overlay. 
            # This also resets the hotbar selection indicator. ===
            self.__towers.cancel_selection()
            self.__on_finish(State.LOST)
            return True

        if self.__enemies.is_complete:
            self.__towers.cancel_selection()
            self.__on_finish(State.VICTORY)
            return True

        return False
