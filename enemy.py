import pygame.draw
from pygame import Surface, Vector2


class Enemy:
    def __init__(self, start_position:Vector2):
        self.pos = start_position

    def render(self, surface: Surface):
        pygame.draw.circle(surface, "red", self.pos, 20)

    def update(self, player_pos:Vector2):
        pass
