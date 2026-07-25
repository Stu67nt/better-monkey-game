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
import util
from upgrades import Upgrades

SCREEN_SIZE = WIDTH, HEIGHT = (1280, 720)

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0
FPS = 60
wave = 20
current_enemy_spawn_counter = wave
last_score = 0
die = False

env = Environment()
camera = Camera(screen)

player = Player((WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), camera)
players = Group()
players.add(player)

upgrades = Upgrades()

enemies = Group()

player_bullets = Group()
env.start_time = time.time()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not die and player.health <= 0:
        die = True
        score = env.time_progressed()
        for enemy in enemies:
            enemy.kill()
        player.kill()
        wave = 20
        current_enemy_spawn_counter = wave
        last_score = 0
        for bullet in player_bullets:
            bullet.kill()
        old_high = util.read_highscores("scores.txt")[0]
        if max(util.read_highscores("scores.txt")) < env.time_progressed():
            util.write_highscores("scores.txt", env.time_progressed())
            pygame.mixer.music.load("assets/audio/winsong.mp3")
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.load("assets/audio/losesong.mp3")
            pygame.mixer.music.play(loops=-1)
        env.deathscreen(screen, score, old_high)

    if die:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            die = False
            player = Player((WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT), camera)
            players = Group()
            players.add(player)

            enemies = Group()

            player_bullets = Group()
            env.start_time = time.time()
            pygame.mixer.music.stop()

    #e = Enemy((
    #    random.randint(0, WIDTH), random.randint(0, HEIGHT)
    #), camera)
    #enemies.add(e)

    if not die:
        players.update(dt=dt, bullets=player_bullets)
        enemies.update(player=player, dt=dt)
        #bullets.update(dt=dt)

        if not env.time_progressed() == last_score:
            if env.time_progressed() % 10 == 0 and wave > 0:
                wave -= 1
                last_score = env.time_progressed()
                print(wave)
                print(env.time_progressed())

        upgrades.apply(player)


        players.update(dt=dt, bullets=player_bullets)
        enemies.update(player=player, dt=dt)
      #bullets.update(dt=dt)

        if not env.time_progressed() == last_score:
          if env.time_progressed() % 10 == 0 and wave > 0:
              wave -= 1
              last_score = env.time_progressed()


        if current_enemy_spawn_counter <= 0:

            enemy_x = random.randint(-800, 800)
            if abs(enemy_x) < 600:
                enemy_x = 600

            enemy_y = random.randint(-800, 800)
            if abs(enemy_y) < 600:
                enemy_y = 600

            e = Enemy((
                player.rect.x + enemy_x, player.rect.y + enemy_y
            ), camera, 700 - (wave * 10))
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

    if not die:
        env.tileBackground(screen, env.bg, camera.offset)
        screen.blit(env.get_time_text(screen), (0,0))
        camera.new_draw(player.rect, dt)
        env.healthbar(screen, player.health)


    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(FPS) / 1000

pygame.quit()