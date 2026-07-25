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
from upgrades import Upgrades, SpeedPowerup, random_powerup
from util import random_coordinate_on_a_ring

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
powerup_spawn_counter = random.randint(5, 10)
die = False

env = Environment()
camera = Camera(screen)

player = Player((WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), camera)
players = Group()
players.add(player)

upgrades = Upgrades()

enemies = Group()

powerups = Group()
powerups.add(
    SpeedPowerup((WIDTH/2, HEIGHT/2), upgrades, camera)
)

player_bullets = Group()
env.start_time = time.time()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # activate deathscreen
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

    # deathscreen ig
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

    # normal logic
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

        if not env.time_progressed() == last_score:
          if env.time_progressed() % 10 == 0 and wave > 0:
              wave -= 1
              last_score = env.time_progressed()


        if current_enemy_spawn_counter <= 0:
            pos = random_coordinate_on_a_ring(player.rect.center, 600, 200)
            e = Enemy(pos, camera, 700 - (wave * 30))
            enemies.add(e)
            current_enemy_spawn_counter = wave/2
        else:
            current_enemy_spawn_counter -= 1

        if powerup_spawn_counter <= 0:
            pos = random_coordinate_on_a_ring(player.rect.center, 400, 200)

            powerup = random_powerup()(pos, upgrades, camera)
            powerups.add(powerup)

            e = Enemy((
                player.rect.x + enemy_x, player.rect.y + enemy_y
            ), camera, 600 - (wave * 10), 0.07 + (0.005 * wave))
            enemies.add(e)
            current_enemy_spawn_counter = wave
            powerup_spawn_counter = random.randint(10,15)
        else:
            powerup_spawn_counter -= dt

        player_bullets.update(dt=dt, enemies=enemies)

        hits = pygame.sprite.spritecollide(player, enemies, dokill=False)
        for monkey in hits: player.hit(0.01)

        hits = pygame.sprite.spritecollide(player, powerups, dokill=False)
        for powerup in hits: powerup.on_collect()

        # =====================
        # ------RENDERING------
        # =====================

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