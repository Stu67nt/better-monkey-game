import pygame.image
from pygame import Rect
from pygame.sprite import Sprite

from util import distance


class PlayerBullet(Sprite):
    def __init__(self, start_position:tuple[int,int], vector:tuple[int,int], camera_group):
        super().__init__(camera_group)

        self.direction_vector = vector
        self.rect = Rect(
            0,0,50,50
        )
        self.rect.center = start_position


        self.initial_image = pygame.image.load("img/banana.png")
        self.initial_image = pygame.transform.scale(self.initial_image, self.rect.size)
        self.image = self.initial_image

        self.rotation = 0

        self.speed = 450

    def update_image(self):
        self.image = pygame.transform.rotate(self.initial_image, self.rotation)
        self.image = pygame.transform.scale(self.image, self.rect.size)


    def update(self, *args, **kwargs):
        dt = kwargs["dt"]
        enemies = kwargs["enemies"]
        self.rect.center = (self.rect.center[0]+self.direction_vector[0]*dt*self.speed,self.rect.center[1]+self.direction_vector[1]*dt*self.speed)

        hits = pygame.sprite.spritecollide(self, enemies, dokill=False)
        for e in hits:
            dist = distance(e.rect.center, self.rect.center)
            if dist < (self.rect.width+e.rect.width)/2:
                e.kill()
                self.kill()

        self.rotation += 100*dt
        self.update_image()


