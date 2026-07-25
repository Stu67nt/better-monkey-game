import pygame.draw
from pygame import Surface, Vector2
from pygame.sprite import Sprite
from util import move_towards, distance
import os
import random
from player import Player


class Enemy(Sprite):
    def __init__(self, start_position, camera_group):
        super().__init__(camera_group)

        self.hit_radius = 40


        self.rect = pygame.Rect(0,0,self.hit_radius*2, self.hit_radius*2)

        self.image = pygame.image.load(f"assets\\img\\monke\\{self.select_sprite()}")
        self.image = pygame.transform.scale(self.image, self.rect.size)

        self.rect.center = start_position
        self.speed = 100

        self.suicide_counter = 500

    def select_sprite(self):
        choices = os.listdir("assets\\img\\monke")
        return random.choice(choices)

    def render(self, surface: Surface):
        pygame.draw.circle(surface, "red", self.rect.center, 40)

    def update(self, *args, **kwargs):
        player = kwargs["player"]
        self.rect.center = move_towards(self.rect.center, player.rect.center, self.speed, kwargs["dt"])

        dist_to_player = distance(player.rect.center, self.rect.center)
        if dist_to_player < (self.hit_radius + player.hit_radius):
            self.kill()

        self.suicide_counter -= 1
        if self.suicide_counter <= 0:
            self.kill()
        #dist_to_player = distance(player.rect.center, self.rect.center)
        #if dist_to_player < (self.hit_radius + player.hit_radius):
        #    player.hit()
