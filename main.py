import random
import pygame
from pygame import Vector2
from pygame.sprite import Group
from bullet import Bullet
from enemy import Enemy
from player import Player
from environment import Environment
import time

SCREEN_SIZE = WIDTH, HEIGHT = (1280, 720)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0
FPS = 60
env = Environment()

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

env.start_time = time.time()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    players.update(dt=dt)
    enemies.update(player=player, dt=dt)
    bullets.update(dt=dt)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")
    env.tileBackground(screen, env.bg)
    # pygame.draw.circle(screen, "orange", player_pos, 40)


    players.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)

    screen.blit(env.get_time_text(screen), (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(FPS) / 1000

pygame.quit()