import math

class Projectile:
    '''Visual Projectile when a shooter tower attack, simply visual, no collision or anything else included'''
    def __init__(self, canvas, start: int, target: int, speed=1500) -> None:
        self.__canvas = canvas

        self.__x, self.__y = start
        self.__target_x, self.__target_y = target

        dx = self.__target_x - self.__x
        dy = self.__target_y - self.__y

        distance = math.hypot(dx, dy)

        if distance == 0:
            self.__vx = 0
            self.__vy = 0
        else:
            self.__vx = dx / distance * speed
            self.__vy = dy / distance * speed

        self.__speed = speed

        self.__id = canvas.create_oval(
            self.__x - 4,
            self.__y - 4,
            self.__x + 4,
            self.__y + 4,
            fill="yellow",
            outline=""
        )

    def update(self, dt: int | float) -> bool:
        dx = self.__target_x - self.__x
        dy = self.__target_y - self.__y
        remaining_distance = math.hypot(dx, dy)
        step_distance = self.__speed * dt

        if remaining_distance <= step_distance or remaining_distance <= 4:
            self.__x = self.__target_x
            self.__y = self.__target_y
        else:
            self.__x += self.__vx * dt
            self.__y += self.__vy * dt

        self.__canvas.coords(
            self.__id,
            self.__x - 4,
            self.__y - 4,
            self.__x + 4,
            self.__y + 4
        )

        return self.__x == self.__target_x and self.__y == self.__target_y

    def destroy(self) -> None:
        self.__canvas.delete(self.__id)
