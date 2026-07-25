import pygame
from pygame import Vector2
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, start_position:tuple[int,int]):
        super().__init__()

        self.hit_radius = 40

        self.health = 1

        self.rect = pygame.Rect(0,0,self.hit_radius*2, self.hit_radius*2)
        self.image = pygame.image.load("img/monkey.gif")
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.rect.center = start_position

    def update(self, *args, **kwargs):
        dt = kwargs["dt"]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= 300 * dt
        if keys[pygame.K_s]:
            self.rect.y += 300 * dt
        if keys[pygame.K_a]:
            self.rect.x -= 300 * dt
        if keys[pygame.K_d]:
            self.rect.x += 300 * dt

    def hit(self, amount:float=0.1):
        self.health-=amount
        if self.health < 0: self.kill()
