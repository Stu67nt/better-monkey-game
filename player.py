import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # self.image = pygame.image.load("").convert_alpha()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


    def death(self):
        self.kill()