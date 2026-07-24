import pygame.draw
from pygame import Surface, Vector2


class Enemy:
    def __init__(self, start_position:Vector2):
        self.pos = start_position
        self.speed = 100
        self.hit_radius = 40

    def render(self, surface: Surface):
        pygame.draw.circle(surface, "red", self.pos, 40)

    def update(self, player_pos:Vector2, player_hit_radius:float, dt:float):
        self.pos = self.pos.move_towards(player_pos, self.speed*dt)

        dist_to_player = self.pos.distance_to(player_pos)
        if dist_to_player < (self.hit_radius + player_hit_radius):
            exit()
