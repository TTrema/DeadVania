import pygame
from math import sin
import time


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

        """ setup """
        self.jumpdown_timer = 0
        self.gravity = 0.8
        self.jump_speed = 16

        """ status """

        self.status = "idle"   
        self.facing_right = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False   
        self.d_jump_on = False   
        self.jumping = False
        self.jumpdown = False
        self.can_fly = False
        self.player = False
        

    def move(self, speed):
        self.collision_rect.x += self.direction.x * speed

    def horizontal_collisions(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.collision_rect):
                if direction == 'horizontal':
                    if self.status == 'backdash' and not self.facing_right or self.collision_rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.collision_rect.right = sprite.rect.left
                        self.pos.x = self.collision_rect.x
                        self.on_right = True 
                        if self.player == True:
                            if not self.on_ground and self.status != 'divekick':
                                self.status = "wallhang" 
                                self.d_jump_on = True          
                    else: 
                        self.on_right = False    
                                                                     
                    if self.status == 'backdash' and self.facing_right or self.collision_rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.collision_rect.left = sprite.rect.right
                        self.pos.x = self.collision_rect.x
                        if self.player == True:                                  
                            if not self.on_ground and self.status != 'divekick':
                                self.status = "wallhang" 
                                self.d_jump_on = True  
                                                            
                if direction == 'vertical':
                    if self.collision_rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.collision_rect.bottom = sprite.rect.top
                        self.pos.y = self.collision_rect.y 
                        self.direction.y = 0
                        self.on_ground = True
                        self.d_jump_on = True
                        self.dive_kick = False
                    else:
                        self.on_ground = False                 
                        
                    if self.collision_rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.collision_rect.top = sprite.rect.bottom
                        self.pos.y = self.collision_rect.y
                        self.direction.y = 0
                        self.jumping = False      
 
        if not self.can_fly:
            for sprite in self.jumpable_sprites.sprites():
                if sprite.rect.colliderect(self.collision_rect):
                    if not self.jumpdown:
                        if self.collision_rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            if self.collision_rect.bottom <= sprite.rect.top + 30:
                                self.collision_rect.bottom = sprite.rect.top
                                self.direction.y = 0
                                self.on_ground = True
                                self.d_jump_on = True
                                self.dive_kick = False
                            else:
                                self.on_ground = False
                                
                    

            if self.jumpdown and pygame.time.get_ticks() - self.jumpdown_timer >= 20:
                self.jumpdown = False
 
                    
        if self.on_ground and self.direction.y != 0:
            self.on_ground = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
        


