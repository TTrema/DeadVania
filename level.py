import pygame
from settings import *
from tiles import Tile, Bridge, StaticTile
from player import Player
from support import *
from enemy import Enemy
from debug import debug
from attack import Attack, DiveAttack
from ui import UI
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
import random


class Level:
    def __init__(self):

        self.sprite_type = "enemy"

        """ level setup """
        self.game_paused = False
        self.display_surface = pygame.display.get_surface()

        """ sprite group setup """
        self.visible_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.jumpable_sprites = pygame.sprite.Group()
        self.ani_sprites = [self.active_sprites, self.visible_sprites]

        """ attack sprite """
        self.current_attack = None
        self.can_hit = True
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = CameraGroup()
        self.attacktype = None
        self.start = pygame.time.get_ticks()

        """ create map """
        self.create_map()

        """ user interface """
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        """ particles """
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            # "battle_background": import_csv_layout("./levels/level1/battle_background.csv"),
            "battle_decoration": import_csv_layout("./levels/level1/level1_decoration.csv"),
            "battle_platform": import_csv_layout("./levels/level1/level1_jumpable.csv"),
            "battle_spawn area": import_csv_layout("./levels/level1/level1_enemy.csv"),
            "battle_Tile": import_csv_layout("./levels/level1/level1_tile.csv"),
        }
        terrain_tile_list = import_cut_graphics_size("./levels/Tiles.png", 16)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != "-1":
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        tile_surface = terrain_tile_list[int(col)]
                        if style == "battle_Tile":
                            StaticTile((x, y), [self.visible_sprites, self.collision_sprites], tile_surface)
                        if style == "battle_decoration":
                            StaticTile((x, y), [self.visible_sprites], tile_surface)
                        if style == "battle_platform":
                            StaticTile((x, y), [self.visible_sprites], tile_surface)
                            Bridge((x, y), [self.visible_sprites, self.jumpable_sprites])
                        if style == "battle_background":
                            StaticTile((x, y), [self.visible_sprites], tile_surface)
                        if style == "battle_spawn area":
                            if not bool(self.attackable_sprites):
                                self.enemy = Enemy(
                                    "smallbee",
                                    (800, 300),
                                    [self.ani_sprites, self.attackable_sprites],
                                    self.collision_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.ani_sprites,
                                    self.add_exp,
                                    self.jumpable_sprites,
                                )
        self.player = Player(
            (400, 400), [self.ani_sprites], self.collision_sprites, self.create_attack, self.destroy_attack, self.create_magic, self.jumpable_sprites
        )

    def setup_level(self):
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == "X":
                    Tile((x, y), [self.visible_sprites, self.collision_sprites])
                if col == "J":
                    Bridge((x, y), [self.visible_sprites, self.jumpable_sprites])
                if col == "E":
                    self.enemy = Enemy(
                        "squid",
                        (x, y),
                        [self.ani_sprites, self.attackable_sprites],
                        self.collision_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.ani_sprites,
                        self.add_exp,
                        self.jumpable_sprites,
                    )
                if col == "B":
                    Enemy(
                        "smallbee",
                        (x, y),
                        [self.ani_sprites, self.attackable_sprites],
                        self.collision_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.ani_sprites,
                        self.add_exp,
                        self.jumpable_sprites,
                    )
                if col == "P":
                    self.player = Player(
                        (x, y),
                        [self.ani_sprites],
                        self.collision_sprites,
                        self.create_attack,
                        self.destroy_attack,
                        self.create_magic,
                        self.jumpable_sprites,
                    )

    def create_attack(self):
        if self.player.attack_id == "attack":
            self.current_attack = Attack(self.player, [self.ani_sprites, self.attack_sprites])
        else:
            self.current_attack = DiveAttack(self.player, [self.ani_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == "heal":

            self.magic_player.heal(self.player, strength, cost, [self.ani_sprites])
        else:
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites, self.active_sprites])

    def player_attack_logic(self):

        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    if self.player.attack_id == "divekick":
                        self.player.start_height = self.player.collision_rect.bottom
                        self.player.direction.y = 0
                        self.player.d_jump_on = True
                        self.player.jumping = True

                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            target_sprite.kill()
                        else:
                            if attack_sprite.attacktype not in target_sprite.hit_by_attack:
                                target_sprite.hit_by_attack[attack_sprite.attacktype] = (False, (attack_sprite.startup, attack_sprite.hit_delay))
                            else:
                                target_sprite.get_damage(self.player, attack_sprite.attacktype)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.collision_rect.center, [self.ani_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.ani_sprites])


    def create_enemy(self):
        layout = import_csv_layout("./levels/level0/battle_spawn area.csv")
        available_positions = []

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != "-1":
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    available_positions.append((x, y))

        if len(self.attackable_sprites) < 10:
            random.shuffle(available_positions)
            for i in range(0, 10, 2):
                random_position = available_positions[i]
                self.enemy = Enemy(
                    "worm",
                    random_position,
                    [self.ani_sprites, self.attackable_sprites],
                    self.collision_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.ani_sprites,
                    self.add_exp,
                    self.jumpable_sprites,
                )
                random_position = available_positions[i+1]
                self.enemy = Enemy(
                    "slime",
                    random_position,
                    [self.ani_sprites, self.attackable_sprites],
                    self.collision_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.ani_sprites,
                    self.add_exp,
                    self.jumpable_sprites,
                )
                self.enemy

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def reset(self):
        self.__init__()

    def run(self):
        
        self.display_surface.blit(self.enemy.image, self.enemy.rect)
      
        self.visible_sprites.custom_draw(self.player, self.enemy)
        self.ui.display(self.player)
        debug(self.player.status)
        debug(self.player.attack_id, 40)
        debug(self.player.crouch, 80)
        debug(self.player.collision_rect.y, 120)

        if self.game_paused:

            self.upgrade.display()

        else:

            self.active_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            # self.create_enemy()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        """ center camera setup """
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player, enemy):

        """get the player offset"""
        self.offset.x = player.collision_rect.centerx - self.half_w
        self.offset.y = player.collision_rect.centery - self.half_h

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

            # Draw the sprite's collision rect
        
        monster_rect = enemy.rect.move(-self.offset.x, -self.offset.y)
        monster_rect.inflate_ip(-30, -30)
        
        collision_rect = player.collision_rect.move(-self.offset.x, -self.offset.y)
        if player.status == "crouch":
            collision_rect.inflate_ip(0, -30)
        if player.status == "fall":
            collision_rect.move_ip(0, -15)
        if player.status == "divekick":
            collision_rect.inflate_ip(0, -30)
            collision_rect.move_ip(0, -15)

        pygame.draw.rect(self.display_surface, (255, 0, 0), enemy.rect, 2)
        pygame.draw.rect(self.display_surface, (255, 0, 0), collision_rect, 2)
        

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)


