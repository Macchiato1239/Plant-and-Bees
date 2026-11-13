
class Difficulty:
    def __init__(self):
        self.__dict={}

    def add(self, key, game_info):
        self.__dict[key]=game_info

    def get(self, key):
        return self.__dict[key]

diff=Difficulty()
diff.add(
    "normal", 
    [
    [[1, 0.5]] * 4 + [[1, 0]],
    [[1, 0.5]] * 6 + [[1, 0]],
    [[2, 0.3]] * 2 + [[2, 1]] + [[1, 0.5]] * 4,
    [[2, 0.3]] + [[2, 0.5]] + [[3, 0.8]] * 5,
    [[4, 1]] * 5,
    ]
    )
diff.add(
    "hard",
    [
    [[1, 0.5]] * 8 + [[1, 0]],
    [[1, 0.5]] * 10 + [[1, 0]],
    [[2, 0.3]] * 6 + [[2, 1]] + [[1, 0.5]] * 5,
    [[2, 0.3]] + [[2, 0.5]] + [[3, 0.8]] * 8,
    [[4, 1]] * 7,  
    ]
    )