import random
import pygame
from pygame import Vector2
from pygame.sprite import Group
from bullet import Bullet
from enemy import Enemy
from player import Player
from environment import Environment

SCREEN_SIZE = WIDTH, HEIGHT = (1280, 720)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0
player_speed = 600
FPS = 60
env = Environment(clock, FPS)

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
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            player_pos.y -= player_speed * dt * 0.7
        else:
            player_pos.y -= player_speed * dt
    if keys[pygame.K_s]:
        if keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_d]:
            player_pos.y += player_speed * dt * 0.7
        else:
            player_pos.y += player_speed * dt
    if keys[pygame.K_a]:
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]:
            player_pos.x -= player_speed * dt * 0.7
        else:
            player_pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w]:
            player_pos.x += player_speed * dt * 0.7
        else:
            player_pos.x += player_speed * dt

    for e in enemies:
        e.update(player_pos)

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

    env.frame_count += 1
    screen.blit(env.get_time_text(screen), (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(FPS) / 1000

pygame.quit()