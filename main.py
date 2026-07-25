import random
import pygame
from pygame import Vector2
from pygame.sprite import Group
from playerBullet import PlayerBullet
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
FPS = 60
env = Environment(clock, FPS)

player = Player((WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))
players = Group()
players.add(player)

enemies = Group()

player_bullets = Group()
test_bullet = PlayerBullet((WIDTH/2, HEIGHT/2), (0,1))
player_bullets.add(test_bullet)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.throw_banana(player_bullets)

    e = Enemy((
        random.randint(0, WIDTH), random.randint(0, HEIGHT)
    ))
    enemies.add(e)

    players.update(dt=dt)
    enemies.update(player=player, dt=dt)
    player_bullets.update(dt=dt, enemies=enemies)


    hits = pygame.sprite.spritecollide(player, enemies, dokill=False)
    for monkey in hits: player.hit(0.01)

#    hits =

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")
    env.tileBackground(screen, env.bg)
    # pygame.draw.circle(screen, "orange", player_pos, 40)


    players.draw(screen)
    enemies.draw(screen)
    player_bullets.draw(screen)

    env.frame_count += 1
    screen.blit(env.get_time_text(screen), (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(FPS) / 1000

pygame.quit()