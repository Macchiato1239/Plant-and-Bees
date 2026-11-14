from Base.rect import Rect
from Base.Entity import Entity

class Enemy(Entity): 
    def __init__(self, canva, name: str, x1: int, y1: int, width: int, height: int, health: int, speed: int, color:str) -> None: 
        '''The physical enemy attacking the base'''
        super().__init__(Rect(canva, x1, y1, width, height, color))
        self.__name=name
        self.__color=color
        self.__reward=health
        self.__initial_health=health
        self.__initial_speed=speed
        self.__health=health
        self.__speed=speed
        self.__progress=0
        # === id of the next coordinate as the map is made of multiple paths===
        self.__distance_covered=0
        # === how far enemies have travelled ===

        # === Debuff ===
        self.__freeze=0 #Freeze duration
        self.__freeze_level=0 # How much enemy is slowed down
        
        self.__burn=0 # Burn duration
        self.__burn_damage=0 # How is much damage burn effect apply per tick

        self.__stun=0 # Stun duration

    @property
    def initial_health(self) -> int:
        return self.__initial_health

    @property
    def stun(self) -> int | float:
        return self.__stun
    
    
    # ======
    @property
    def freeze(self) -> int | float:
        return self.__freeze
    @freeze.setter
    def freeze(self, value: int | float) -> None:
        if isinstance(value, (int, float)):
            self.__freeze=value

    @property
    def freeze_level(self) -> int:
        return self.__freeze_level
    @freeze_level.setter
    def freeze_level(self, value: int) -> None:
        if isinstance(value, int):
            self.__freeze_level=min(4,value)

    # ======
    @property
    def burn(self) -> int | float:
        return self.__burn
    @burn.setter
    def burn(self, value: int | float) -> None:
        if isinstance(value, (int, float)):
            self.__burn=value

    @property
    def burn_damage(self) -> int | float:
        return self.__burn_damage
    @burn_damage.setter
    def burn_damage(self,value: int | float) -> None:
        if isinstance(value, (float, int)):
            self.__burn_damage=value
    # ======

    @property
    def name(self) -> str:
        return self.__name

    @property
    def reward(self) -> int:
        return self.__reward
    
    #=====
    @property
    def health(self) -> int | float:
        return self.__health
    @health.setter
    def health(self,value: int | float) -> None:
        if isinstance(value, int):
            self.__health=value

    #=====
    @property
    def speed(self) -> int | float:
        return self.__speed
    @speed.setter
    def speed(self, value: int | float) -> None:
        if isinstance(value, (int, float)):
            self.__speed=value
    #=====
    @property
    def color(self) -> str:
        return self.__color
    @color.setter
    def color(self, value: str) -> None:
        if isinstance(value, str):
            self.__color=value
    #======
    @property
    def progress(self) -> int:
        return self.__progress
    @progress.setter
    def progress(self, value: int) -> int:
        if isinstance(value, int):
            self.__progress=value

    #=====
    @property
    def distance_covered(self) -> int:
        return self.__distance_covered
    
    @distance_covered.setter
    def distance_covered(self, value: int) -> None:
        if isinstance(value, (int, float)):
            self.__distance_covered=value
    #=====

    def move(self, canva, x: int, y: int, delta_time: int | float) -> bool:
        '''Moving enemies along the path to base'''

        x_reach=True
        y_reach=True
        if self.rect.cord_x!=x:
            # === If has reached horizontally ===
            di=1 if self.rect.cord_x<x else -1

            x_after_move=self.rect.cord_x+di*self.__speed * delta_time

            if (di==1 and x_after_move>x) or (di==-1 and x_after_move<x):
                self.rect.x1=x-self.rect.width/2
                canva.move(self.rect.rect_id, x-self.rect.cord_x, 0)
            else:
                self.__distance_covered+=abs(x_after_move-self.rect.cord_x)
                self.rect.x1+=di*self.__speed * delta_time
                canva.move(self.rect.rect_id, di*self.__speed * delta_time, 0)
                x_reach=False
        if self.rect.cord_y!=y:
            # === If has reach vertically ===
            di=1 if self.rect.cord_y<y else -1

            y_after_move=self.rect.cord_y+di*self.__speed * delta_time

            if (di==1 and y_after_move>y) or (di==-1 and y_after_move<y):
                self.rect.y1=y-self.rect.height/2
                canva.move(self.rect.rect_id, 0, y-self.rect.cord_y)
            else:
                self.__distance_covered+=abs(y_after_move-self.rect.cord_y)
                self.rect.y1+=di*self.__speed * delta_time
                canva.move(self.rect.rect_id, 0, di*self.__speed * delta_time)
                y_reach=False
        # === If both are true, enemy has reach it's destination ===
        return x_reach and y_reach

    def process_debuff(self, delta_time: int | float) -> None:
        # === Apply debuff's effect onto enemy's stats ===
        if self.__burn!=0:
            # === Tick damage ===
            self.__health-=self.__burn_damage
            self.__burn=max(0, self.__burn-delta_time)

        if self.__freeze!=0:
            # === Slow and stun ===
            if self.__freeze_level in [1,2,3]:
                self.__speed-=(self.__speed*20*self.__freeze_level)/100
                self.__freeze=max(0, self.__freeze-delta_time)
            if self.__freeze_level == 4:
                self.__stun=0.6
                self.__freeze_level=0
                self.__freeze=0

        if self.__stun!=0:
            # === Stop enemy movement ===
            self.__speed=0
            self.__stun=max(0, self.__stun-delta_time)

        if self.__stun==0 and self.__freeze==0:
            # === Enemy recovery and stats recover to default ===
            self.__speed=self.__initial_speed
        

class Enemy_Info:
    '''Information cards for enemy, Enemy Manager class uses Enemy_Info to create Enemy '''
    def __init__(self, name: str, health: int, speed: int, color:str, width: int, height: ibt) -> None:
        self.__name=name
        self.__health=health
        self.__speed=speed
        self.__color=color
        self.__width=width
        self.__height=height

    @property
    def name(self) -> str:
        return self.__name

    @property
    def health(self) -> int | float:
        return self.__health
    @property
    def speed(self) -> int | float:
        return self.__speed

    @property
    def color(self) -> str:
        return self.__color

    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height

