import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {"heal": pygame.mixer.Sound("./audio/heal.wav"), "flame": pygame.mixer.Sound("./audio/Fire.wav")}

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds["heal"].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]

            self.animation_player.create_particles("aura", player.collision_rect.center, groups)
            self.animation_player.create_particles("heal", player.collision_rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):

        if player.energy >= cost:
            self.sounds["flame"].play()
            player.energy -= cost

            if player.facing_right:
                direction = pygame.math.Vector2(1, 0)
            else:
                direction = pygame.math.Vector2(-1, 0)

            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILE_SIZE
                    x = player.rect.centerx + offset_x + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles("flame", (x, y), groups)
