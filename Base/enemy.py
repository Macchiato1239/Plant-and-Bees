from Base.rect import Rect
from Base.entity import Entity
from Base.debuff import BurnEffect, FreezeEffect, StatusEffect

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

        self.__effects: list[StatusEffect] = []
        # Compatibility values used by the existing freeze/burn properties.
        self.__freeze=0
        self.__freeze_level=0
        self.__burn=0
        self.__burn_damage=0
        self.__burn_tick=1
        self.__stun=0

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

    @property
    def burn_tick(self) -> int | float:
        return self.__burn_tick

    @burn_tick.setter
    def burn_tick(self, value: int | float) -> None:
        if isinstance(value, (int, float)) and value > 0:
            self.__burn_tick=value
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

    def apply_effect(self, effect: StatusEffect) -> None:
        '''Attach an effect object; new enemy effects are added without changing the manager.'''
        if not isinstance(effect, StatusEffect):
            raise TypeError("effect must be a StatusEffect")
        for active_effect in self.__effects:
            if active_effect.refresh_from(effect):
                self.__sync_effect_properties()
                return
        self.__effects.append(effect)
        self.__sync_effect_properties()

    def update(self, delta_time: int | float, canvas, destination) -> bool:
        '''Update effects and movement; return whether the destination was reached.'''
        self.__update_effects(delta_time)
        if self.__health <= 0 or self.__speed <= 0:
            return False
        x, y = destination
        return self.move(canvas, x, y, delta_time * 100)

    def __update_effects(self, delta_time: int | float) -> None:
        self.__effects = [effect for effect in self.__effects
                          if not effect.update(self, delta_time)]
        self.__sync_effect_properties()

    def __sync_effect_properties(self) -> None:
        self.__freeze = max((effect.remaining for effect in self.__effects
                             if isinstance(effect, FreezeEffect) and effect.level < 4), default=0)
        self.__freeze_level = min(4, sum(effect.level for effect in self.__effects
                                          if isinstance(effect, FreezeEffect) and effect.level < 4))
        self.__burn = max((effect.remaining for effect in self.__effects
                           if isinstance(effect, BurnEffect)), default=0)
        self.__burn_damage = sum(effect.damage for effect in self.__effects
                                 if isinstance(effect, BurnEffect))
        active_burns = [effect for effect in self.__effects
                        if isinstance(effect, BurnEffect)]
        self.__burn_tick = active_burns[0].tick if active_burns else 1
        self.__stun = max((effect.stun_remaining for effect in self.__effects
                           if isinstance(effect, FreezeEffect) and effect.level >= 4), default=0)
        multiplier = 1.0
        stunned = False
        for effect in self.__effects:
            multiplier *= effect.speed_multiplier
            stunned = stunned or effect.is_stunning
        self.__speed = 0 if stunned else self.__initial_speed * multiplier

    def process_debuff(self, delta_time: int | float) -> None:
        '''Process the debuff that enemy may have'''
        # === Apply freeze to self ===
        if self.__freeze > 0 and not any(isinstance(effect, FreezeEffect) for effect in self.__effects):
            self.apply_effect(FreezeEffect(self.__freeze, self.__freeze_level))
        # === Apply burn to self ===
        if self.__burn > 0 and not any(isinstance(effect, BurnEffect) for effect in self.__effects):
            self.apply_effect(BurnEffect(
                self.__burn, self.__burn_damage, self.__burn_tick
            ))
        self.__update_effects(delta_time)

    def add_freeze(self, duration: int | float, level: int | float) -> None:
        self.apply_effect(FreezeEffect(duration, level))

    def add_burn(self, duration: int | float, damage: int | float,
                 tick: int | float = 1) -> None:
        self.apply_effect(BurnEffect(duration, damage, tick))
        

class Enemy_Info:
    '''Information cards for enemy, Enemy Manager class uses Enemy_Info to create Enemy '''
    def __init__(self, name: str, health: int, speed: int, color:str, width: int, height: int) -> None:
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

