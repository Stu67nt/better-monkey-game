import pygame.draw
from pygame import Surface, Vector2
from pygame.sprite import Sprite
from util import move_towards

from player import Player


class Enemy(Sprite):
    def __init__(self, start_position):
        super().__init__()

        self.hit_radius = 40


        self.rect = pygame.Rect(0,0,self.hit_radius*2, self.hit_radius*2)

        self.image = pygame.image.load("img/monkey.gif")
        self.image = pygame.transform.scale(self.image, self.rect.size)

        self.rect.center = start_position
        self.speed = 100



    def render(self, surface: Surface):
        pygame.draw.circle(surface, "red", self.rect.center, 40)

    def update(self, *args, **kwargs):
        self.rect.center = move_towards(self.rect.center, kwargs["player"].rect.center, self.speed, kwargs["dt"])

        #dist_to_player = self.rect.distance_to(player.pos)
        #if dist_to_player < (self.hit_radius + player.hit_radius):
        #    self.kill()
