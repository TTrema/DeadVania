import pygame
from settings import *
from pygame.math import Vector2 as vector
from support import *
from entity import Entity
from controls import Controls_Handler
from support import load_save
from movement import movement


class Player(Entity):
    def __init__(self, pos, groups, collision_sprites, create_attack, destroy_attack, create_magic, jumpable_sprites):
        super().__init__(groups)
        self.import_character_assets()
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        """ player movement """
        self.previous_status = None

        """ player attack """
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.recovery = False
        self.attack_cooldown = 600
        self.attack_time = None
        self.attack_id = None

        """ magic """
        self.create_magic = create_magic
        self.magic_index = 0
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 200

        """ Player status """
        self.hold_up = False
        self.air_jumping = False
        self.walljump = False
        self.dive_kick = False
        self.player = True
        self.crouch = False
        self.collision_sprites = collision_sprites
        self.jumpable_sprites = jumpable_sprites

        self.collision_rect = pygame.Rect(self.rect.topleft, (50, 70))
        self.old_rect = self.collision_rect.copy()
        self.pos = pygame.math.Vector2(self.collision_rect.topleft)
        self.start_height = 0
        self.start_width = 0

        """ Player stats """

        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 8}
        self.max_stats = {"health": 300, "energy": 140, "attack": 20, "magic": 10, "speed": 10}
        self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 5000
        self.speed = self.stats["speed"]

        """ damage timer """
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability = 500

        """ controls """
        save, joy_save = load_save()
        self.control_handler = Controls_Handler(save, joy_save)

        """ Soun """
        self.weapon_attack_sound = pygame.mixer.Sound("./audio/sword.wav")
        self.weapon_attack_sound.set_volume(0.4)

    def input(self):
        movement(self)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.recovery:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.recovery = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability:
                self.vulnerable = True

    def import_character_assets(self):
        character_path = "./graphics/charactern/"
        self.animations = {
            "idle": [],
            "run": [],
            "jump": [],
            "fall": [],
            "attack": [],
            "blaze": [],
            "backdash": [],
            "crouch": [],
            "wallhang": [],
            "divekick": [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        if self.walljump:
            if self.on_right:
                self.collision_rect.x += -10
                if self.start_width >= self.collision_rect.right + 40:
                    self.walljump = False
            else:
                self.collision_rect.x += 10
                if self.start_width <= self.collision_rect.right - 40:
                    self.walljump = False

        if self.jumping:
            if self.start_height > self.collision_rect.bottom + 110:
                self.jumping = False
            else:
                self.direction.y += -1.5

        if self.recovery:
            self.status = self.attack_id
            self.direction.x = 0
            self.direction.y = 0

        elif self.dive_kick:
            self.status = "divekick"

        else:
            if self.status == "wallhang":
                if not self.jumping:
                    self.direction.y = 0

            if self.direction.y < 0:
                self.status = "jump"

            elif self.crouch and self.on_ground:
                self.status = "crouch"
                self.direction.x = 0

            elif self.direction.y > 1:
                self.status = "fall"

            else:
                if self.direction.x != 0:
                    self.status = "run"
                else:
                    self.status = "idle"

    def animate(self):
        animation = self.animations[self.status]

        if self.status != self.previous_status:
            self.frame_index = 0
            self.previous_status = self.status

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == "jump":
                self.frame_index = 1
            else:
                self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = pygame.transform.scale(image, (int(image.get_width() * (2.5, 2.5)[0]), int(image.get_height() * (2.5, 2.5)[1])))
            self.rect = self.image.get_rect(bottomleft=self.collision_rect.bottomleft)
            offset = -40
        else:
            image = pygame.transform.flip(image, True, False)
            self.image = pygame.transform.scale(image, (int(image.get_width() * (2.5, 2.5)[0]), int(image.get_height() * (2.5, 2.5)[1])))
            self.rect = self.image.get_rect(bottomright=self.collision_rect.bottomright)
            offset = 40

        self.rect.left += offset

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = 15
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = 20
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]

        else:
            self.energy = self.stats["energy"]

    def backdash(self):

        if self.recovery:
            if self.attack_id == "backdash":
                if self.on_ground:
                    if self.facing_right:
                        self.collision_rect.centerx -= 10
                    else:
                        self.collision_rect.centerx += 10
                else:
                    self.recovery = False


    def divekick(self):
        self.direction.y += 20
        self.dive_kick = True
        self.create_attack()

    def update(self):
        self.old_rect = self.collision_rect.copy()
        self.input()
        self.get_status()
        self.move(self.speed)
        self.backdash()
        self.horizontal_collisions('horizontal')
        self.apply_gravity()
        self.horizontal_collisions('vertical')
        self.animate()
        self.energy_recovery()
        self.cooldowns()
