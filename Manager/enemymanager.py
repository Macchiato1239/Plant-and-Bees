import math

from dictionary import Ebook
from Base.enemy import Enemy
from Manager.difficulty import diff

class EnemyManager:
    '''Spawn waves and update enemy movement, effects, deaths, and base damage.'''

    def __init__(self, canvas, difficulty_level, spawn, path_points):
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
        if difficulty_level==1:
            self.__game_info=diff.get("normal")
        elif difficulty_level==2:
            self.__game_info=diff.get("hard")
        elif difficulty_level==3:
            self.__game_info=diff.get("insane")

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
                enemy_id, delay = self.__game_info[self.__game_progress][self.__wave_progress]
                self.spawn(Ebook.get(enemy_id))
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
            current_enemy.process_debuff(delta_time)
            # === Enemy process debuff ===

            if current_enemy in self.__active_enemies and current_enemy.health <= 0:
                # === Process enemies' death and add it to the reward ===
                reward += current_enemy.reward
                self.__active_enemies.remove(current_enemy)
                current_enemy.delete()
                continue
            

            destination = self.__path_points[current_enemy.progress]
            reached = current_enemy.move(canvas, destination[0], destination[1], delta_time * 100)

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
        width, height = enemy_info.width, enemy_info.height
        x = self.__spawn.rect.cord_x - width / 2
        y = self.__spawn.rect.cord_y - height / 2
        spawned_enemy = Enemy(
            self.__canvas, enemy_info.name, x, y, width, height,
            enemy_info.health, enemy_info.speed, enemy_info.color,
        )
        self.__active_enemies.append(spawned_enemy)
        return spawned_enemy
