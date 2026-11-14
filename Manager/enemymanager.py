import math

from dictionary import Ebook
from Base.enemy import Enemy
from Base.exceptions import (
    InvalidDifficultyError,
    InvalidWaveDataError,
    UnknownDefinitionError,
)
from difficulty import diff

class EnemyManager:
    '''Spawn waves and update enemy movement, effects, deaths, and base damage.'''

    def __init__(self, canvas, difficulty_level, spawn, path_points):
        if not isinstance(difficulty_level, int):
            raise TypeError("difficulty_level must be an integer")
        self.__canvas = canvas
        self.__spawn = spawn
        self.__path_points = path_points
        self.__active_enemies = []
        self.__time_til_next_spawn = 0
        self.__time_since_last_spawn = 0
        self.__wave_progress = 0
        self.__game_progress = 0
        self.__base_damage = 0
        self.__completed_waves=0
        self.__time_til_next_wave = 3.0
        self.__time_since_last_wave = 0.0
        self.__waiting_for_next_wave = False
        modes = {1: "normal", 2: "hard", 3: "insane"}
        try:
            mode = modes[difficulty_level]
        except KeyError as error:
            raise InvalidDifficultyError(
                "difficulty_level must be 1 (normal), 2 (hard), or 3 (insane)"
            ) from error
        self.__game_info = diff.get(mode)

        # ===A map containing enemy id, time before spawning the next enemy===

    @property
    def completed_waves(self):
        return self.__completed_waves
    @property 
    def is_complete(self):
        return self.__game_progress == -1 and not self.__active_enemies
    
    @property
    def base_damage(self):
        return self.__base_damage

    @base_damage.setter
    def base_damage(self, value):
        if isinstance(value, (float, int)):
            self.__base_damage=value
    @property
    def active_enemies(self):
        return self.__active_enemies

    @property
    def game_info(self):
        return self.__game_info

    @property
    def display_wave(self):
        '''Display current wave number'''
        if self.__game_progress < 0:
            return f"Wave {len(self.__game_info)}/{len(self.__game_info)}"
        return f"Wave {self.__game_progress + 1}/{len(self.__game_info)}"

    @property
    def next_wave_countdown(self):
        if not self.__waiting_for_next_wave:
            return ""
        remaining = max(
            0, self.__time_til_next_wave - self.__time_since_last_wave
        )
        return f"Next wave in: {math.ceil(remaining)}s"

    def update(self, delta_time, canvas):
        if not isinstance(delta_time, (int, float)):
            raise TypeError("delta_time must be a number")
        if delta_time < 0:
            raise ValueError("delta_time cannot be negative")
        if self.__waiting_for_next_wave:
            self.__time_since_last_wave += delta_time
            if self.__time_since_last_wave >= self.__time_til_next_wave:
                self.__waiting_for_next_wave = False
                self.__time_since_last_wave = 0.0
                self.__game_progress += 1
                self.__wave_progress = 0
                self.__time_til_next_spawn = 0.0
                self.__time_since_last_spawn = 0.0
        else:
            self.__time_since_last_spawn += delta_time

        # === Processing waves ===
        if (not self.__waiting_for_next_wave
                and self.__game_progress != -1
                and self.__wave_progress != -1):
            # === If there are still waves and unsummoned enemies ===
            if self.__time_since_last_spawn >= self.__time_til_next_spawn:
                # === Enough time has passed to spawn the next enemy ===
                try:
                    enemy_id, delay = self.__game_info[self.__game_progress][self.__wave_progress]
                except IndexError as error:
                    raise IndexError(
                        f"Wave data is missing wave {self.__game_progress + 1}, "
                        f"spawn {self.__wave_progress + 1}"
                    ) from error
                except (TypeError, ValueError) as error:
                    raise InvalidWaveDataError(
                        "Each wave entry must contain an enemy ID and spawn delay"
                    ) from error
                try:
                    enemy_info = Ebook.get(enemy_id)
                except KeyError as error:
                    raise UnknownDefinitionError(
                        f"Enemy_Dictionary has no entry for key {enemy_id!r}"
                    ) from error
                except TypeError as error:
                    raise TypeError("Wave enemy IDs must be hashable dictionary keys") from error
                self.spawn(enemy_info)
                self.__time_til_next_spawn = delay
                self.__time_since_last_spawn = 0

                if self.__wave_progress == len(self.__game_info[self.__game_progress]) - 1:
                    # === Check if current wave is last ===
                    self.__wave_progress = -1
                else:
                    self.__wave_progress += 1

        reward = 0
        self.__base_damage=0
        for current_enemy in self.__active_enemies[:]:
            try:
                destination = self.__path_points[current_enemy.progress]
                destination_x, destination_y = destination
            except IndexError as error:
                raise IndexError(
                    f"Enemy path progress {current_enemy.progress} is not in the path list"
                ) from error
            except (TypeError, ValueError) as error:
                raise InvalidWaveDataError(
                    "Each path point must contain an x and y coordinate"
                ) from error

            reached = current_enemy.update(
                delta_time, canvas, (destination_x, destination_y)
            )

            if current_enemy in self.__active_enemies and current_enemy.health <= 0:
                # === Process enemies' death and add it to the reward ===
                reward += current_enemy.reward
                self.__active_enemies.remove(current_enemy)
                current_enemy.delete()
                continue


            # === Check if enemy reached a coordinate in the paths (corner or base) ===
            if reached:
                if current_enemy.progress == len(self.__path_points) - 1:
                    # === Check if that point reached is the base ===
                    self.__base_damage += current_enemy.health
                    self.__active_enemies.remove(current_enemy)
                    current_enemy.delete()

                else:
                    # === Keep advancing if not ===
                    current_enemy.progress += 1

        if (not self.__active_enemies
                and self.__game_progress != -1
                and self.__wave_progress == -1
                and not self.__waiting_for_next_wave):
            # The wave is complete once all its enemies have been removed.
            self.__completed_waves += 1
            if self.__game_progress == len(self.__game_info) - 1:
                self.__game_progress = -1
            else:
                self.__waiting_for_next_wave = True
                self.__time_since_last_wave = 0.0
        return reward

    def spawn(self, enemy_info):
        '''spawn enemy from given enemy information'''
        try:
            width, height = enemy_info.width, enemy_info.height
            name, speed = enemy_info.name, enemy_info.speed
            health, color = enemy_info.health, enemy_info.color
        except AttributeError as error:
            raise AttributeError(
                "enemy_info must provide name, health, speed, color, width, and height"
            ) from error
        x = self.__spawn.rect.cord_x - width / 2
        y = self.__spawn.rect.cord_y - height / 2
        spawned_enemy = Enemy(
            self.__canvas, name, x, y, width, height, health, speed, color,
        )
        self.__active_enemies.append(spawned_enemy)
        return spawned_enemy
