import random
import pygame
from pygame import Vector2
from pygame.sprite import Group
from playerBullet import PlayerBullet
from enemy import Enemy
from player import Player
from environment import Environment
from camera import Camera
import time

SCREEN_SIZE = WIDTH, HEIGHT = (1280, 720)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0
FPS = 60
wave = 20
current_enemy_spawn_counter = wave
last_score = 0
frame_count = 0

env = Environment()
camera = Camera(screen)

player = Player((WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), camera)
players = Group()
players.add(player)

enemies = Group()

player_bullets = Group()
test_bullet = PlayerBullet((WIDTH/2, HEIGHT/2), (0,1), camera)

env.start_time = time.time()

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
    ), camera)
    enemies.add(e)

    players.update(dt=dt)
    enemies.update(player=player, dt=dt)
    #bullets.update(dt=dt)

    if not env.time_progressed() == last_score:
        if env.time_progressed() % 10 == 0 and wave > 0:
            wave -= 1
            last_score = env.time_progressed()
            print(wave)
            print(env.time_progressed())

    if current_enemy_spawn_counter <= 0:
        e = Enemy((
            random.randint(player.rect.x - 500, player.rect.x + 500), random.randint(player.rect.y - 500, player.rect.y + 500)
        ), camera)
        enemies.add(e)
        current_enemy_spawn_counter = wave
    else: 
        current_enemy_spawn_counter -= 1

    player_bullets.update(dt=dt, enemies=enemies)


    hits = pygame.sprite.spritecollide(player, enemies, dokill=False)
    for monkey in hits: player.hit(0.01)

    # =====================
    # ------RENDERING------
    # =====================

    screen.fill("green")
    env.tileBackground(screen, env.bg, camera.offset)
    screen.blit(env.get_time_text(screen), (0,0))
    camera.new_draw(player.rect, dt)
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(FPS) / 1000

pygame.quit()