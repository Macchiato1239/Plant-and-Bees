from build import Base, Path, Spawn

class Buildings:
    '''Manage the spawn, base, and path geometry for a game map.'''
    def __init__(self, canvas, base_health):
        self.__spawn = Spawn(canvas, 0, 300)
        self.__base = Base(canvas, base_health, 900, 300)
        self.__path_points = [
            [self.__spawn.rect.cord_x, self.__spawn.rect.cord_y],
            [100, 300],
            [100, 400],
            [350, 400],
            [350, 300],
            [self.__base.rect.cord_x, self.__base.rect.cord_y],
        ]
        self.__paths = [
            Path(canvas, *start, *end)
            for start, end in zip(self.__path_points, self.__path_points[1:])
        ]
        self.__map_length = sum(
            abs(end_x - start_x) + abs(end_y - start_y)
            for (start_x, start_y), (end_x, end_y)
            in zip(self.__path_points, self.__path_points[1:])
        )

    @property
    def spawn(self):
        return self.__spawn

    @property
    def base(self):
        return self.__base

    @property
    def path_points(self):
        return self.__path_points

    @property
    def paths(self):
        return self.__paths

    @property
    def map_length(self):
        return self.__map_length
