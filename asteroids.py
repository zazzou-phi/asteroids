#!/usr/bin/env python

import pygame
import game_objects as go
import math
from vec2d import Vec2d
import random

pygame.init()

# global variables
WIDTH = 800
HEIGHT = 600
FPS = 60

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# start the display
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asteroids')


player = go.Spaceship(WIDTH/2, HEIGHT/2)
asteroids = []
bullets = []

for i in range(4):
    colliding = True
    while colliding:
        asteroid_x = random.randrange(0, WIDTH)
        asteroid_y = random.randrange(0, HEIGHT)
        if (Vec2d(asteroid_x,asteroid_y) - player.pos).get_length() > go.Asteroid.size[0] + player.width/3:
            colliding = False

    dir_x = random.uniform(-1, 1)
    dir_y = random.uniform(-1, 1)
    direction = Vec2d(dir_x, dir_y).normalized()

    asteroids.append(go.Asteroid(asteroid_x, asteroid_y, direction, 0))

# start the clock
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(go.Bullet(player.pos.x + player.direction.x * player.width/3,
                                         player.pos.y + player.direction.y * player.width/3, player.direction))

    gameDisplay.fill(BLACK)
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_LEFT]:
        player.theta -= player.dtheta
    if pressed_keys[pygame.K_RIGHT]:
        player.theta += player.dtheta
    if pressed_keys[pygame.K_UP]:
        player.vel += player.vel_increment *player.direction


    player.update(gameDisplay)
    player.draw(gameDisplay)

    for bullet in bullets:
        bullet.update(gameDisplay)
        bullet.draw(gameDisplay)

    for asteroid in asteroids:
        asteroid.update(gameDisplay)
        asteroid.draw(gameDisplay)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()
