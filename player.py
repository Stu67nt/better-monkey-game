import pygame
from pygame import Vector2
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, start_position:tuple[int,int], game_size: tuple[int, int]):
        super().__init__()

        self.hit_radius = 40

        self.health = 1

        self.rect = pygame.Rect(0,0,self.hit_radius*2, self.hit_radius*2)
        self.image = pygame.image.load("img/banana.png")
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.rect.center = start_position
        self.speed = 600
        self.game_size = game_size

    def update(self, *args, **kwargs):
        dt = kwargs["dt"]
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and not self.rect.y <= 0:
            if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
                self.rect.y -= self.speed * dt * 0.7
            else:
                self.rect.y -= self.speed * dt
        if keys[pygame.K_s] and not self.rect.y >= self.game_size[1] - self.rect.size[1]:
            if keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_d]:
                self.rect.y += self.speed * dt * 0.7
            else:
                self.rect.y += self.speed * dt
        if keys[pygame.K_a] and not self.rect.x <= 0:
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]:
                self.rect.x -= self.speed * dt * 0.7
            else:
                self.rect.x -= self.speed * dt
        if keys[pygame.K_d] and not self.rect.x >= self.game_size[0] - self.rect.size[0]:
            if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w]:
                self.rect.x += self.speed * dt * 0.7
            else:
                self.rect.x += self.speed * dt

    def hit(self, amount:float=0.1):
        self.health-=amount
        if self.health < 0: self.kill()
