class Difficulty:
    def __init__(self):
        self.__modes = {}

    def add(self, key, waves):
        self.__modes[key] = waves

    def get(self, key):
        return self.__modes[key]


def make_wave(*groups):
    '''Build a wave from (enemy_id, count, delay_after_spawn) groups.'''
    enemies = []
    for enemy_id, count, delay in groups:
        enemies.extend([[enemy_id, delay] for _ in range(count)])
    if enemies:
        enemies[-1][1] = 0
    return enemies


diff = Difficulty()

# Enemy IDs from dictionary.py:
# 1 normal (6 HP), 2 quick (8), 3 heavy (30), 4 abnormal (12),
# 5 swift (20), 6 elite abnormal (150), 7 speedy boss (500), 8 giant boss (2000).
diff.add("normal", [
    make_wave((1, 8, 0.7)),
    make_wave((1, 5, 0.55), (2, 4, 0.7)),
    make_wave((2, 7, 0.5), (3, 3, 0.9)),
    make_wave((4, 6, 0.6), (2, 5, 0.5), (3, 4, 0.9)),
    make_wave((5, 8, 0.5), (3, 4, 0.8)),
    make_wave((6, 4, 1.3), (3, 6, 0.7)),
    make_wave((5, 10, 0.4), (7, 1, 0)),
    make_wave((6, 6, 0.6), (8, 1, 0)),
])

diff.add("hard", [
    make_wave((1, 12, 0.45)),
    make_wave((2, 10, 0.45), (1, 8, 0.4)),
    make_wave((2, 10, 0.35), (3, 7, 0.7)),
    make_wave((4, 10, 0.4), (5, 8, 0.4)),
    make_wave((3, 10, 0.45), (6, 4, 0.9)),
    make_wave((5, 12, 0.3), (6, 6, 0.7)),
    make_wave((6, 8, 0.5), (7, 2, 1.4)),
    make_wave((3, 8, 0.45), (7, 3, 0.8)),
    make_wave((6, 8, 0.4), (7, 2, 1.2), (8, 1, 0)),
])

diff.add("insane", [
    make_wave((1, 18, 0.3), (2, 12, 0.35)),
    make_wave((2, 18, 0.28), (3, 10, 0.55)),
    make_wave((4, 14, 0.35), (5, 14, 0.3)),
    make_wave((3, 15, 0.4), (5, 14, 0.3)),
    make_wave((6, 10, 0.45), (3, 12, 0.4)),
    make_wave((5, 20, 0.25), (6, 10, 0.4)),
    make_wave((6, 14, 0.35), (7, 3, 0.7)),
    make_wave((3, 16, 0.35), (7, 5, 0.6)),
    make_wave((6, 12, 0.3), (7, 3, 0.7), (8, 1, 0)),
    make_wave((5, 20, 0.25), (6, 16, 0.35), (8, 2, 0)),
])
