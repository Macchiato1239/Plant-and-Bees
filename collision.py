import math
from rect import Rect
class CollisionManager:
    def __init__(self):
        self.__interactive = []
        # === UI collision check ===
        self.__taken = []  
        # === Space taken up by paths and towers ===

    @property
    def interactive(self):
        return self.__interactive

    @interactive.setter
    def interactive(self, value):
        self.__interactive = value

    @property
    def taken(self):
        return self.__taken

    @taken.setter
    def taken(self, value):
        self.__taken = value

    def compare_cord_rect(self, cord_x, cord_y, rect_list):
        '''Check whether a coordinate is within a rectangle'''
        for i in rect_list:
            i_x1=i.x1
            i_width=i.width
            i_y1=i.y1
            i_height=i.height

            if i_x1<cord_x<i_x1+i_width and i_y1<cord_y<i_y1+i_height:
                return True
        return False

    def dist_cord_cord(self, rect1, rect2):
        '''Distance between two points'''
        cord1_x=rect1.cord_x
        cord1_y=rect1.cord_y
        cord2_x=rect2.cord_x
        cord2_y=rect2.cord_y

        horizontal=(cord1_x-cord2_x)**2
        vertical=(cord1_y-cord2_y)**2
        dist=math.sqrt(horizontal+vertical)
        return dist

    def range_enemy_tower(self, enemy, tower):
        '''Range between a tower and an enemy'''
        dist=self.dist_cord_cord(enemy.rect, tower.rect)
        if dist<=tower.act_range:
            return True
        return False

    def interactive_at(self, x, y):
        '''Return the first registered interactive item on click'''
        for item in self.__interactive:
            rect = item.rect
            if rect.x1 < x < rect.x1 + rect.width and rect.y1 < y < rect.y1 + rect.height:
                return item
        return None


    
