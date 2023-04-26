import pygame
from settings import *
from data.entity import Entity
from data.support import *
import time
from data.particles import AnimationPlayer


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, collision_sprites, damage_player, trigger_death_particles, sprite_groups, add_exp, jumpable_sprites):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.sprite_groups = sprite_groups
        self.groups = groups

        """ graphic setup """
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]     
        self.animation_player = AnimationPlayer

        """ movement """
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = self.rect
        self.old_rect = self.collision_rect.copy()
        self.pos = pygame.math.Vector2(self.collision_rect.topleft)
        self.collision_sprites = collision_sprites
        self.jumpable_sprites = jumpable_sprites



        """ stats """
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]
        self.size = monster_info["size"]
        self.offset = monster_info["offset"]
        self.rect_size = monster_info["rect"]
        self.can_fly = bool(monster_info.get("fly", False))
        self.gravity = 1
    
        """ player interaction """
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.hit_by_attack = {}
        self.damage_font = pygame.font.SysFont("comicsansms", 32)
        self.add_exp = add_exp
        self.delay_attack = 0

        """ invincibility timer """
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        """ sound """
        self.death_sound = pygame.mixer.Sound("./audio/death.wav")
        self.hit_sound = pygame.mixer.Sound("./audio/hit.wav")
        self.attack_sound = pygame.mixer.Sound(monster_info["attack_sound"])
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.4)

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}
        main_path = f"./graphics/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)


    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):


        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):

        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            if self.monster_name == 'worm':
                self.damage_player(self.attack_damage, self.attack_type)
                self.attack_sound.play()

            else:
                self.damage_player(self.attack_damage, self.attack_type)
                self.attack_sound.play()
        elif self.status == "move":
            if self.can_fly:
                self.direction = self.get_player_distance_direction(player)[1]
            else:  
                if self.on_ground:        
                    self.direction.x = round(self.get_player_distance_direction(player)[1][0])
                
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
  

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * (self.size, self.size)[0]), int(self.image.get_height() * (self.size, self.size)[1])))
            self.rect = self.image.get_rect(midbottom=self.collision_rect.midbottom)
        else:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * (self.size, self.size)[0]), int(self.image.get_height() * (self.size, self.size)[1])))
            self.rect = self.image.get_rect(midbottom=self.collision_rect.midbottom)
            
       
        

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        keys_to_delete = []
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        for attack_type, (hit, delay) in self.hit_by_attack.items():
            if hit and current_time - self.hit_time >= delay[1]:
                keys_to_delete.append(attack_type)

        for key in keys_to_delete:
            del self.hit_by_attack[key]

    def get_damage(self, player, attack_type):

        attack_id = self.hit_by_attack[attack_type]
        if not attack_id[0]:
            if "weapon" in attack_type:
                damage_amount = player.get_full_weapon_damage()           
            elif "divekick" in attack_type:
                damage_amount = 2
            else:
                damage_amount = player.get_full_magic_damage()

            self.health -= damage_amount
            self.hit_sound.play()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            self.hit_by_attack[attack_type] = (True, attack_id[1])
            if player.dive_kick:
                player.dive_kick = False 

            # Create and display damage number sprite
            damage_text = self.damage_font.render(str(int(damage_amount)), True, (255, 0, 0))
            damage_sprite = DamageNumberSprite((self.rect.centerx, self.rect.top), damage_text)
            for sprite_group in self.sprite_groups:
                sprite_group.add(damage_sprite)

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction.x *= -self.resistance

    def fly(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.collision_rect.x += self.direction.x * speed
        self.collision_rect.y += self.direction.y * speed

    def update(self):
        self.old_rect = self.collision_rect.copy()

        self.hit_reaction()

        if self.can_fly:
            self.fly(self.speed)
        else:
            self.move(self.speed) 
                                      
        self.animate()
        self.check_death()
        self.cooldowns()
        if not self.can_fly:
            self.horizontal_collisions('horizontal')  
            self.apply_gravity()  
            self.horizontal_collisions('vertical')
        else:
            self.horizontal_collisions('vertical')
            self.horizontal_collisions('horizontal')
            
        if self.direction.x < 0:
            self.facing_right = False
        if self.direction.x > 0:
            self.facing_right = True

    
        

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)


class DamageNumberSprite(pygame.sprite.Sprite):
    def __init__(self, pos, damage_text):
        super().__init__()
        self.image = damage_text
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = -2  # Set vertical speed for upward movement of damage number
        self.timer = 60  # Set timer to 60 frames (1 second at 60 FPS)

    def animate(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top < 0 or self.timer <= 0:
            self.kill()
        else:
            self.timer -= 1


    def update(self):
        self.animate()