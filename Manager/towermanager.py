from dictionary import Tbook
from Base.module_tower import DebuffTower, DpsTower, EffectType, Farm, SupportTower
from Base.rect import Rect


class TowerManager:
    '''Manages tower selection, placement, and tower actions.'''

    def __init__(self, canvas, collision):
        self.__canvas = canvas
        self.__collision = collision
        self.__active_towers = []
        self.__max_active_towers=20
        # === list of towers placed on the map
        self.__current_tower = None
        self.__current_tower_signal = Rect(canvas, 0, 0, 30, 30, "red")

    
    @property
    def active_towers(self):
        return self.__active_towers

    @property
    def current_tower(self):
        return self.__current_tower

    @property
    def selected_tower_info(self):
        if self.__current_tower is None:
            return None
        return Tbook.get(self.__current_tower)

    def select_tower_card(self, tower_id):
        '''Select a tower to place'''
        if isinstance(tower_id, int):
            self.__current_tower = tower_id
            # === Signaling a tower has been selected ===
            self.__current_tower_signal.change_color("green")

    def cancel_selection(self):
        '''Cancel selection'''
        self.__current_tower = None
        self.__current_tower_signal.change_color("red")

    def place_tower(self, cord_x, cord_y, money):
        '''Creating a tower object using the current selected tower's info'''
        if self.__current_tower is None:
            # === Check if a tower is selected ===
            return False, money

        if len(self.__active_towers)==self.__max_active_towers:
            # === Check if the number of towers has hit the limit
            return

        tower_info = Tbook.get(self.__current_tower)
        if money < tower_info.cost:
            # === Check if there is sufficient fund ===
            return False, money

        radius = tower_info.size
        x1, y1 = cord_x - radius, cord_y - radius
        width = height = radius * 2
        corners = ((x1, y1), (x1 + width, y1),
                   (x1, y1 + height), (x1 + width, y1 + height))
        if any(self.__collision.compare_cord_rect(x, y, self.__collision.taken)
               for x, y in corners):
            # === Check if the placement is valid ===
            return False, money

        rect = Rect(self.__canvas, x1, y1, width, height, tower_info.color)
        tower = Tbook.summon_tower(self.__current_tower, rect)
        # === Create the tower object ===
        self.__active_towers.append(tower)
        # === Append to the list of all placed towers ===
        self.__collision.taken.append(rect)
        self.cancel_selection()
        return True, money - tower.cost

    def update(self, enemies, collision):
        ''''''
        for tower in self.__active_towers:
            if not isinstance(tower, DpsTower):
                if isinstance(tower, (SupportTower, Farm)):
                    continue
                continue

            damage = tower.act()
            if not damage:
                continue
            in_range = [enemy for enemy in enemies if collision.range_enemy_tower(enemy, tower)]
            # === Collect enemies within the act range of tower ===
            target = self.__enemy_sorter(in_range)
            # === Find the closest enemy to base in the tower range ===
            if target == 0:
            # === None in range ===
                continue
            target.health -= damage
            if isinstance(tower, DebuffTower) and tower.type == EffectType.FROZEN:
                # === Apply freeze debuff ===
                target.freeze = tower.duration
                target.freeze_level += tower.magnitude

    @staticmethod
    def __enemy_sorter(enemies):
        if not enemies:
            return 0
        return max(enemies, key=lambda enemy: enemy.distance_covered)
