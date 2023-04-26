import pygame
from settings import *
from data.support import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(TILE_COLOR)
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

class StaticTile(Tile):
    def __init__(self, pos, groups, surface):
        super().__init__(pos, groups)
        self.image = surface

class Bridge(Tile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.image = pygame.Surface((TILE_SIZE, 1))
        self.rect = self.image.get_rect(topleft = pos)

        
class AnimatedTile(Tile):
    def __init__(self, pos, groups, path):
        super().__init__(pos, groups)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Palm(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))