from pygame.display import update

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
        player.speed = 100 + self.level * 50
class FireRateUpgrade(Upgrade):
    def apply(self, player:Player):
        player.shoot_cooldown = 1 / (self.level + 1)

