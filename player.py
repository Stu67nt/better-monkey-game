import pygame
from pygame import Vector2
from pygame.sprite import Sprite

from playerBullet import PlayerBullet
from util import direction_to


class Player(Sprite):
    def __init__(self, start_position:tuple[int,int], game_size: tuple[int, int], camera_group):
        super().__init__(camera_group)

        self.camera_group = camera_group

        self.hit_radius = 40

        self.health = 100

        self.rect = pygame.Rect(0,0,self.hit_radius*2, self.hit_radius*2)

        self.initial_image = pygame.image.load("assets/img/banana.png")
        self.initial_image = pygame.transform.scale(self.initial_image, self.rect.size)
        self.image = self.initial_image

        self.rect.center = start_position
        self.speed = 600
        self.game_size = game_size

        self.mirror_texture = False

    def update(self, *args, **kwargs):
        dt = kwargs["dt"]
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
                self.rect.y -= self.speed * dt * 0.7
            else:
                self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            if keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_d]:
                self.rect.y += self.speed * dt * 0.7
            else:
                self.rect.y += self.speed * dt
        if keys[pygame.K_a]:
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]:
                self.rect.x -= self.speed * dt * 0.7
            else:
                self.rect.x -= self.speed * dt

            self.mirror_texture = False

        if keys[pygame.K_d]:
            if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w]:
                self.rect.x += self.speed * dt * 0.7
            else:
                self.rect.x += self.speed * dt

            self.mirror_texture = True



        if self.mirror_texture:
            self.image = pygame.transform.flip(self.initial_image, True, False)
        else:
            self.image = self.initial_image

    def hit(self, amount:float=0.1):
        self.health-=amount
        if self.health < 0: self.kill()

        #print("player health: ", self.health)

    def throw_banana(self, banana_group):
        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0]+self.camera_group.offset[0], mouse[1]+self.camera_group.offset[1])

        mouse_direction = direction_to(self.rect.center, mouse)
        banana_group.add(PlayerBullet(
           self.rect.center, mouse_direction, self.camera_group
        ))
