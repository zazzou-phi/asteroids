import pygame
from vec2d import Vec2d
import math
from random import uniform

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameObject():
    """
    This class is the user spaceship
    """

    def __init__(self, x, y, vel, direction, dtheta):
        self.pos = Vec2d(x, y)
        self.vel = vel
        self.direction = direction
        self.theta = direction.get_angle()
        self.theta_old = 0
        self.dtheta = dtheta
        self.vertices = []

    def draw(self, display):
        points = []
        for i in range(len(self.vertices)):
            points.append((self.pos + self.vertices[i]).as_tuple())

        pygame.draw.aalines(display, WHITE, True, points, 1)

    def update(self, display):
        for vector in self.vertices:
            vector.rotate(self.dtheta)

        self.theta %= 2*math.pi

        self.pos += self.vel
        self.pos[0] %= display.get_width()
        self.pos[1] %= display.get_height()


class Spaceship(GameObject):
    """
    This class is the user spaceship
    """

    def __init__(self, x, y):
        super().__init__(x, y, Vec2d(0, 0), Vec2d(1, 0), math.pi/45)
        self.width = 20
        self.height = 12
        self.vel_increment = 0.2
        self.max_speed = 4
        self.theta_old = self.theta
        self.vertices = [Vec2d(- self.width/3, - self.height/2),
                         Vec2d(2*self.width/3, 0),
                         Vec2d(- self.width/3, self.height/2),
                         Vec2d(- self.width/5, 0)]

    def update(self, display):
        if self.theta != self.theta_old:
            for vector in self.vertices:
                vector.rotate(self.theta - self.theta_old)
            self.direction.rotate(self.theta - self.theta_old)

        self.theta %= 2*math.pi
        self.theta = self.theta_old

        if self.vel.get_length() > self.max_speed:
            self.vel = self.max_speed* self.vel.normalized()

        self.pos += self.vel
        self.pos[0] %= display.get_width()
        self.pos[1] %= display.get_height()


class Asteroid(GameObject):
    """
    This is the class for the asteroids
    """
    speed = [0.2, 3.8]
    size = [40, 5]

    def __init__(self, x, y, direction, aster_type):

        vel = Asteroid.speed[aster_type] * direction

        super().__init__(x, y, vel, direction, math.pi/360)

        for i in range(8):
            self.vertices.append(uniform(0.8, 1.2) * Asteroid.size[aster_type] * Vec2d(math.cos(2*(i+1)*math.pi/8),
                                                                                       math.sin(2*(i+1)*math.pi/8)))


class Bullet(GameObject):
    """
    Bullet class
    """
    def __init__(self, x, y, direction):
        super().__init__(x, y, 5*direction, direction, 0)

    def draw(self, display):
        pygame.draw.line(display, WHITE, (self.pos.x, self.pos.y), (self.pos.x, self.pos.y))

    def update(self, display):
        self.pos += self.vel
        self.pos[0] %= display.get_width()
        self.pos[1] %= display.get_height()