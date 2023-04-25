import pygame, sys
from settings import *
from level import Level
from controls import Controls_Handler
from support import load_save, reset_keys
from input import input, actions
from pygame._sdl2 import controller

controller.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


global screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED)

newgame = True



class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.main_menu = MainMenu
        self.running, self.playing = True, False
        self.screen = screen
        pygame.display.set_caption("Dead Vania")
        self.clock = pygame.time.Clock()
        self.newgame = True
        self.level = Level()

        """ player setup """

        self.player = self.level.player
        self.magic_index = 0

        """ control setup """

        save, joy_save = load_save()
        self.control_handler = Controls_Handler(save, joy_save)
        self.control = self.control_handler.controls
        self.joystick = self.control_handler.joystick
        

        

        """ sound """

        main_sound = pygame.mixer.Sound("./audio/main.ogg")
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def run(self):
        self.playing = True
        self.newgame = False
               
        while self.playing:
            if self.level.stage_clear_flag == True:
                self.reset()
                self.playing = False
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                """ Joystick setup """
                                           
                self.keypress = pygame.key.get_pressed()                           
                if len(joysticks) > 0:
                    self.joy = pygame.joystick.Joystick(0).get_button
                    self.hat_0 = pygame.joystick.Joystick(0).get_hat(0)[0]
                    self.hat_1 = pygame.joystick.Joystick(0).get_hat(0)[1]
                    self.axis_0 = pygame.joystick.Joystick(0).get_axis(0)
                    self.axis_1 = pygame.joystick.Joystick(0).get_axis(1)
                else:
                    self.joy, self.hat_0, self.hat_1, self.axis_0, self.axis_1 = None, 0, 0, 0, 0
                    

                    

                """ keyboard inputs """

                if event.type == pygame.KEYDOWN:
                    if event.key == self.control_handler.controls["Start"]:
                        self.playing = False

                    if event.key == self.control_handler.controls["Dodge"]:
                        self.backdash()

                    if event.key == self.control_handler.controls["Down"] and self.player.attack_id == "backdash":
                        self.player.recovery = False

                    if event.key == self.control_handler.controls["Attack"]:
                        self.attack()

                    if event.key == self.control_handler.controls["Jump"] and self.keypress[self.control_handler.controls["Down"]]:
                        self.dive_kick()

                    if event.key == self.control_handler.controls["Jump"]:
                        self.double_jump()

                    if event.key == self.control_handler.controls["Jump"]:   
                        self.jump()

                    if event.key == self.control_handler.controls["Magic"]:
                        self.magic()

                    if event.key == self.control_handler.controls["Select"]:
                        self.level.toggle_menu()

                elif event.type == pygame.KEYUP:
                    if event.key == self.control_handler.controls["Jump"]:
                        self.player.jumping = False


                """ joystick inputs """


                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joy(self.joystick["Start"]):
                        self.playing = False

                    elif self.joy(self.joystick["Dodge"]):
                        self.backdash()

                    elif self.joy(self.joystick["Attack"]):
                        self.attack()

                    if self.joy(self.joystick["Jump"]) and (self.hat_1 == -1 or self.axis_1 > 0.2):
                        self.dive_kick()

                    if self.joy(self.joystick["Jump"]):
                        self.double_jump()

                    if self.joy(self.joystick["Jump"]):
                        self.jump()

                    if self.joy(self.joystick["Magic"]):
                        self.magic()

                    if self.joy(self.joystick["Select"]):
                        self.level.toggle_menu()

                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == self.joystick["Jump"]:
                        self.player.jumping = False


                if event.type == pygame.JOYHATMOTION:
                    if self.hat_1 == -1 and self.player.attack_id == "backdash":  # down
                        self.player.recovery = False
         
                        
                if event.type == pygame.JOYAXISMOTION:
                    if pygame.joystick.Joystick(0).get_axis(1) > 0.5 and self.player.attack_id == "backdash":
                        self.player.recovery = False

            self.screen.fill((135, 206, 235))
            self.level.run()                
            self.check_game_over()
            pygame.display.update()
            self.clock.tick(FPS)

    """ commands """

    def backdash(self):
        if self.player.on_ground and (not self.player.recovery or self.player.attack_id == "attack"):
            self.player.recovery = True
            self.player.attack_time = pygame.time.get_ticks()
            self.player.attack_id = "backdash"
            self.player.backdash()

    def attack(self):
        if not self.player.recovery:
            self.player.recovery = True
            self.player.attack_time = pygame.time.get_ticks()
            self.player.attack_id = "attack"
            self.player.create_attack()
            self.player.weapon_attack_sound.play()

    def jump(self):

        if not self.player.recovery and (self.player.on_ground or self.player.status == "wallhang"):
            self.player.start_height = self.player.collision_rect.bottom
            self.player.start_width = self.player.collision_rect.right
  

            if self.hat_1 == -1 or self.axis_1 > 0.2 or self.keypress[self.player.control_handler.controls["Down"]]:
                self.player.jumpdown = True
                
            else:

                if self.player.status == "wallhang":
                    self.player.walljump = True
                              
                self.player.jumping = True

    def double_jump(self):
        if self.player.status in ["jump", "fall"] and self.player.d_jump_on:
            self.player.start_height = self.player.collision_rect.bottom
            self.player.d_jump_on = False
            self.player.direction.y = 0
            self.player.jumping = True

    def dive_kick(self):
        if not self.player.d_jump_on and not self.player.recovery:
            self.player.direction.y = 0
            self.player.attack_id = "divekick"
            self.player.divekick()

    def magic(self):
        if not self.player.recovery:
            if self.player.hold_up:
                self.magic_index = 1
            else:
                self.magic_index = 0

            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]["strength"] + self.player.stats["magic"]
            cost = list(magic_data.values())[self.magic_index]["cost"]
            if self.player.energy >= cost:
                self.player.recovery = True
                self.player.attack_time = pygame.time.get_ticks()
                self.player.attack_id = "blaze"
                self.player.create_magic(style, strength, cost)

    def check_game_over(self):
        if self.player.health <= 0:
            self.player.health = 100           
            self.reset()
            self.playing = False
                     
    def reset(self):
        self.level = Level()
        self.player = self.level.player
        self.magic_index = 0
        self.newgame = True

        """ control setup """

        save, joy_save = load_save()
        self.control_handler = Controls_Handler(save, joy_save)
        self.control = self.control_handler.controls
        self.joystick = self.control_handler.joystick


class MainMenu:
    def __init__(self):
        save, joy_save = load_save()
        self.control_handler = Controls_Handler(save, joy_save)
        self.game = Game()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.playing = False
        self.menu_font = pygame.font.Font("./graphics/font/8-BIT WONDER.TTF", 50)
        self.menu_options = ["Start", "Options", "Exit"]
        self.selected = 0

    def load_and_blit_image(self, image_path, position):
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(image, position)

    def run(self):
        self.selected = 0

        while True:
            if not self.game.newgame:
                self.menu_options = ["Return", "Options", "Exit"]
            else:
                self.menu_options = ["Start", "Options", "Exit"]
            self.display_menu_options(self.menu_options, self.selected)
            reset_keys(actions)

            input()

            if actions["Down"]:
                self.selected = (self.selected + 1) % len(self.menu_options)
            elif actions["Up"]:
                self.selected = (self.selected - 1) % len(self.menu_options)
            elif actions["Jump"] or actions["Start"]:
                if self.selected == 0:
                    self.playing = True
                    self.newgame = False
                    self.game.run()
                    self.main_menu_running = False
                elif self.selected == 1:
                    self.options_menu()
                elif self.selected == 2:
                    answer = self.ask_yes_no_question("Are you sure you want to quit?")

                    # If the user clicks "Yes", quit the game
                    if answer:
                        pygame.quit()
                        sys.exit()

            self.update_menu()

    def update_menu(self):
        pygame.display.update()
        self.clock.tick(FPS)

    def options_menu(self):
        self.menu_options = ["Keyboard", "Back"]
        self.selected = 0
        running = True

        while running:
            self.display_menu_options(self.menu_options, self.selected)
            pygame.display.update()
            reset_keys(actions)
            input()
            if actions["Attack"] or actions["Escape"]:
                running = False

            if actions["Down"]:
                self.selected = (self.selected + 1) % len(self.menu_options)
            elif actions["Up"]:
                self.selected = (self.selected - 1) % len(self.menu_options)
            elif actions["Jump"] or actions["Start"]:
                if self.selected == 0:
                    self.Keyboard()

                elif self.selected == 1:
                    running = False

            self.update_menu()
            
            
    def game_over(self):
        self.menu_options = ["yes", "No"]
        self.selected = 0
        running = True

        while running:
            self.display_menu_options(self.menu_options, self.selected)
            pygame.display.update()
            reset_keys(actions)
            input()
            if actions["Attack"] or actions["Escape"]:
                running = False

            if actions["Down"]:
                self.selected = (self.selected + 1) % len(self.menu_options)
            elif actions["Up"]:
                self.selected = (self.selected - 1) % len(self.menu_options)
            elif actions["Jump"] or actions["Start"]:
                if self.selected == 0:
                    pass

                elif self.selected == 1:
                    pass

            self.update_menu()            

    def Keyboard(self):
        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        window = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))
        running = True

        while running:
            reset_keys(actions)
            input()
            if actions["Attack"] or actions["Escape"]:
                running = False

            self.control_handler.update(actions)
            window.fill((135, 206, 235))
            canvas.fill((135, 206, 235))
            self.control_handler.render(canvas)
            window.blit(pygame.transform.scale(canvas, (SCREEN_WIDTH * 1.8, SCREEN_HEIGHT * 1.8)), (180, 0))
            pygame.display.update()
            reset_keys(actions)

    def display_menu_options(self, options, selected):
        self.load_and_blit_image("./graphics/menu/layer_1.png", (0, 0))
        self.load_and_blit_image("./graphics/menu/layer_2.png", (0, 0))
        self.menu_options = options
        self.selected = selected

        for i, option in enumerate(self.menu_options):
            if i == self.selected:
                text = self.menu_font.render(option, True, "white")
            else:
                text = self.menu_font.render(option, True, "gray")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)

    def ask_yes_no_question(self, question):
        self.menu_font = pygame.font.Font("./graphics/font/8-BIT WONDER.TTF", 40)
        text = self.menu_font.render(question, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

        yes_text = self.menu_font.render("Yes", True, (255, 255, 255))
        yes_rect = yes_text.get_rect(center=(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50))
        no_text = self.menu_font.render("No", True, (255, 255, 255))
        no_rect = no_text.get_rect(center=(SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT / 2 + 50))

        while True:
            self.load_and_blit_image("./graphics/menu/layer_1.png", (0, 0))
            self.load_and_blit_image("./graphics/menu/layer_2.png", (0, 0))

            self.screen.blit(text, text_rect)
            self.screen.blit(yes_text, yes_rect)
            self.screen.blit(no_text, no_rect)
            pygame.display.flip()

            # Wait for user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_rect.collidepoint(mouse_pos):
                        return True
                    elif no_rect.collidepoint(mouse_pos):
                        return False


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
