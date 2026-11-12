from dictionary import Ebook
from enemy import Enemy


class EnemyManager:
    '''Spawn waves and update enemy movement, effects, deaths, and base damage.'''

    def __init__(self, canvas, spawn, path_points):
        self.__canvas = canvas

        self.__spawn = spawn
        self.__path_points = path_points
        self.__active_enemies = []
        self.__time_til_next_spawn = 0
        self.__time_since_last_spawn = 0
        self.__wave_progress = 0
        self.__mode_progress = 0
        self.__base_damage = 0
        # ===A map containing enemy id, time before spawning the next enemy===
        self.__mode = [
            [[1, 0.5]] * 4 + [[1, 0]],
            [[1, 0.5]] * 6 + [[1, 0]],
            [[2, 0.3]] * 2 + [[2, 1]] + [[1, 0.5]] * 4,
            [[2, 0.3]] + [[2, 0.5]] + [[3, 0.8]] * 5,
            [[4, 1]] * 5,
        ]


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
    def mode(self):
        return self.__mode

    @property
    def display_wave(self):
        '''Display current wave number'''
        if self.__mode_progress < 0:
            return f"Wave {len(self.__mode)}/{len(self.__mode)}"
        return f"Wave {self.__mode_progress + 1}/{len(self.__mode)}"

    def update(self, delta_time, canvas):
        # === Get delta time ===
        self.__time_since_last_spawn += delta_time

        # === Processing waves ===
        if self.__mode_progress != -1 and self.__wave_progress != -1:
            # === If there are still waves and unsummoned enemies ===
            if self.__time_since_last_spawn >= self.__time_til_next_spawn:
                # === Enough time has passed to spawn the next enemy ===
                enemy_id, delay = self.__mode[self.__mode_progress][self.__wave_progress]
                self.spawn(Ebook.get(enemy_id))
                self.__time_til_next_spawn = delay
                self.__time_since_last_spawn = 0

                if self.__wave_progress == len(self.__mode[self.__mode_progress]) - 1:
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

        if (not self.__active_enemies and self.__mode_progress != -1
            and self.__wave_progress == -1):
            # === Condition to move to next wave: 
            # All enemies have been spawned and died
            # The current wave is not the last ===

            self.__wave_progress = 0
            self.__mode_progress += 1
            if self.__mode_progress >= len(self.__mode):
                self.__mode_progress = -1
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
