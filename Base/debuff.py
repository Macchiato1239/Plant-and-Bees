from enum import Enum, auto
from abc import ABC, abstractmethod

class EffectType(Enum):
    '''Type of debuff applied on enemy'''
    FROZEN=auto(),
    # === Slow down then stun ===
    BURN=auto(),
    # === Apply damage over time ===


class StatusEffect(ABC):
    '''A timed effect that can be applied to and updated on an enemy.'''

    @abstractmethod
    def update(self, enemy, delta_time: int | float) -> bool:
        '''Update the effect; return True once it has expired.'''
        raise NotImplementedError

    @property
    def speed_multiplier(self) -> float:
        return 1.0

    @property
    def is_stunning(self) -> bool:
        return False

    def refresh_from(self, other) -> bool:
        '''Refresh this effect from another instance; return whether handled.'''
        return False


class FreezeEffect(StatusEffect):
    '''Slows an enemy, or stuns it when the freeze level reaches four.'''

    def __init__(self, duration: int | float, level: int | float) -> None:
        self.remaining = max(0, duration)
        self.level = max(0, level)
        self.stun_remaining = 0.6 if self.level >= 4 else 0

    def update(self, enemy, delta_time: int | float) -> bool:
        if self.level >= 4:
            self.stun_remaining = max(0, self.stun_remaining - delta_time)
            return self.stun_remaining == 0
        self.remaining = max(0, self.remaining - delta_time)
        return self.remaining == 0

    @property
    def speed_multiplier(self) -> float:
        if self.level >= 4:
            return 1.0
        return max(0.4, 1 - 0.2 * self.level)

    @property
    def is_stunning(self) -> bool:
        return self.stun_remaining > 0


class BurnEffect(StatusEffect):
    '''Deals damage at fixed intervals until its duration expires.'''

    def __init__(self, duration: int | float, damage: int | float,
                 tick: int | float = 1) -> None:
        self.remaining = max(0, duration)
        self.damage = damage
        self.tick = tick
        self.__time_since_tick = 0

    def update(self, enemy, delta_time: int | float) -> bool:
        if self.remaining <= 0:
            return True
        elapsed = min(delta_time, self.remaining)
        self.remaining -= elapsed
        self.__time_since_tick += elapsed
        while self.__time_since_tick >= self.tick:
            enemy.health -= self.damage
            self.__time_since_tick -= self.tick
        return self.remaining == 0

    def refresh_from(self, other) -> bool:
        if not isinstance(other, BurnEffect):
            return False
        self.remaining = other.remaining
        self.damage = other.damage
        self.tick = other.tick
        return True
