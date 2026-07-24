import pygame.draw
from pygame import Surface, Vector2


class Enemy:
    def __init__(self, start_position:Vector2):
        self.pos = start_position
        self.speed = 100

    def render(self, surface: Surface):
        pygame.draw.circle(surface, "red", self.pos, 50)

    def update(self, player_pos:Vector2, dt:float):
        self.pos = self.pos.move_towards(player_pos, self.speed*dt)
