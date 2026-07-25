import pygame.draw
from pygame import Surface, Rect
from pygame.display import update
from pygame.sprite import Sprite

from player import Player


# UPGRADE system
# each upgrade has a level,
#
#
#




class Upgrades:
    SPEED = 0
    FIRE_RATE = 1



    def __init__(self):
        self.upgrades = [
            SpeedUpgrade(),
            FireRateUpgrade()
        ]

    def apply(self, player:Player):
        for upgrade in self.upgrades:
            upgrade.apply(player)

    def update(self, player:Player):




class Upgrade:
    def __init__(self, level=0):
        self.level = 0
    def apply(self, player:Player):
        pass
    def next_level(self):
        self.level += 1
    def update_level(self, new_level:int):
        self.level = new_level

class SpeedUpgrade(Upgrade):
    def apply(self, player:Player):
        player.speed = 400 + self.level * 50
class FireRateUpgrade(Upgrade):
    def apply(self, player:Player):
        player.initial_shoot_cooldown = 0.2 / (self.level + 1)

class Powerup(Sprite):

    UPGRADE_TYPE = Upgrades.SPEED
    def __init__(self, upgrades, camera):
        super().__init__(camera)
        self.upgrade = upgrades.upgrades[self.UPGRADE_TYPE]

        self.rect = Rect(0,0,70,70)

        self.image = pygame.image.load("assets/img/powerups/speed.png")
        self.image = pygame.transform.scale(self.image, self.rect.size)
    def update(self, *args, **kwargs):
        player = kwargs["player"]

        hits = pygame.sprite.spritecollide(player, )