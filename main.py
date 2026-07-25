import pygame

from enemy import Enemy

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_speed = 600

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

enemies = []
enemies.append(Enemy((0,0)))


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

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    pygame.draw.circle(screen, "green", player_pos, 40)

    for e in enemies:
        e.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()