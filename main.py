import random

import pygame
from pygame import Vector2
from pygame.sprite import Group

from bullet import Bullet
from enemy import Enemy
from player import Player

SCREEN_SIZE = WIDTH, HEIGHT = (1280, 720)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0

player = Player((WIDTH/2, HEIGHT/2))
players = Group()
players.add(player)

enemies = Group()

bullets = Group()
test_bullet = Bullet((WIDTH/2, HEIGHT/2), (0,1))
bullets.add(test_bullet)

for _ in range(20):
    e = Enemy((
        random.randint(0,WIDTH), random.randint(0,HEIGHT)
    ))
    enemies.add(e)




while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    players.update(dt=dt)
    enemies.update(player=player, dt=dt)
    bullets.update(dt=dt)

    hits = pygame.sprite.spritecollide(player, enemies, dokill=False)
    for monkey in hits: player.hit(0.01)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    #pygame.draw.circle(screen, "green", player.pos, 40)

    players.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()