from hotbar import Slot
from rect import Rect


class HotBarManager:
    '''Create and manage the tower selection slots.'''
    def __init__(self, canvas, collision):
        self.__canvas = canvas
        self.__collision = collision
        self.__slot_count = 5
        self.__hotbar = {}
        self.__equipped_towers = []
        self.__slot_x1 = 50
        self.__slot_y1 = 550
        self.__slot_width = 130
        self.__slot_height = 700
        self.__empty_slot_color = "black"
        self.__filled_slot_color = "red"

    @property
    def hotbar(self):
        return self.__hotbar

    @property
    def equipped_towers(self):
        return self.__equipped_towers

    def create_slots(self):
        '''Creates display of slot for player selection of tower.'''
        if self.__hotbar:
            return
        for index in range(self.__slot_count):
            x1 = self.__slot_x1 + (self.__slot_width + 50) * index
            rect = Rect(self.__canvas, x1, self.__slot_y1, self.__slot_width,
                        self.__slot_height, self.__empty_slot_color)
            slot = Slot(rect)
            self.__hotbar[index] = slot
            self.__collision.interactive.append(slot)

    def equip_tower(self, tower_id):
        '''Storing the tower's id inside the created slot'''
        if not isinstance(tower_id, int) or not self.__hotbar:
            return
        if tower_id not in self.__equipped_towers:
            # === If haven't already equipped ===
            self.__equipped_towers.append(tower_id)
        
        if len(self.__equipped_towers) > self.__slot_count:
            self.__equipped_towers.pop(0)
        # === Pop the first tower if there are more towers equipped than the limit ===
        for index, slot in self.__hotbar.items():
            slot.tower = self.__equipped_towers[index] if index < len(self.__equipped_towers) else None

    def update_colors(self):
        '''Signaling which slot is empty'''
        for slot in self.__hotbar.values():
            color = self.__filled_slot_color if slot.tower is not None else self.__empty_slot_color
            slot.rect.change_color(color)

    def contains(self, item):
        '''Check if the tower is equipped'''
        return item in self.__hotbar.values()
