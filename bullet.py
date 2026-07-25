import pygame.image
from pygame import Rect
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, start_position:tuple[int,int], vector:tuple[int,int]):
        super().__init__()

        self.direction_vector = vector
        self.rect = Rect(
            0,0,80,80
        )
        self.rect.center = start_position


        self.initial_image = pygame.image.load("img/banana.png")
        self.initial_image = pygame.transform.scale(self.initial_image, self.rect.size)
        self.image = self.initial_image

        self.rotation = 0

        self.speed = 120

    def update_image(self):
        self.image = pygame.transform.rotate(self.initial_image, self.rotation)
        self.image = pygame.transform.scale(self.image, self.rect.size)


    def update(self, *args, **kwargs):
        dt = kwargs["dt"]
        self.rect.center = (self.rect.center[0]+self.direction_vector[0]*dt*self.speed,self.rect.center[1]+self.direction_vector[1]*dt*self.speed)


        self.rotation += 1
        self.update_image()


