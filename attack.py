import pygame
import time

class Base(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.attacktype = 'weapon_' + str(int(time.time()))
        self.hit_delay = 200
        self.startup = 2
        self.recovery = 4
        self.player = player
        self.image = pygame.Surface((00, 00), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
                  
class Attack(Base):
    def __init__(self, player, groups):
        super().__init__(player, groups)

    def update(self):
        if self.player.attack_id == 'attack':
            if int(self.player.frame_index) >= self.startup:
                self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
                self.image.fill((255, 255, 255))  # Set the color to transparent
                self.image.set_alpha(128)
            if int(self.player.frame_index) >= self.recovery:
                self.kill()

            if self.player.facing_right:
                self.rect = self.image.get_rect(midleft = self.player.collision_rect.midright + pygame.math.Vector2(0,0))
            else: 
                self.rect = self.image.get_rect(midright = self.player.collision_rect.midleft + pygame.math.Vector2(0,0))
        else:
            self.kill()

class DiveAttack(Base):
    def __init__(self, player, groups):
        super().__init__(player, groups)

        self.attacktype = 'divekick' + str(int(time.time()))
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))  # Set the color to transparent
        self.image.set_alpha(128)

    def update(self):
        self.rect = self.image.get_rect(midbottom = self.player.collision_rect.midbottom + pygame.math.Vector2(0,10))
        if not self.player.dive_kick:
            self.kill()
 
