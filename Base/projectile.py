import math

class Projectile:
    def __init__(self, canvas, start, target, speed=1000):
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

    def update(self, dt):
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

    def destroy(self):
        self.__canvas.delete(self.__id)
