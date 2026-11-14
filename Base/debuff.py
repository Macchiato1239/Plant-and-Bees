from enum import Enum, auto

class EffectType(Enum):
    '''Type of debuff applied on enemy'''
    FROZEN=auto(),
    # === Slow down then stun ===
    BURN=auto(),
    # === Apply damage over time ===