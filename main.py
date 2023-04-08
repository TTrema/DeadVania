import pygame, sys
from settings import *
from level import Level
from controls import Controls_Handler
from support import load_save



class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.running, self.playing = True, False
        self.main_menu_running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dead Vania")
        self.clock = pygame.time.Clock()

        self.level = Level()

        """ player setup """

        self.player = self.level.player
        self.magic_index = 0

        """ control setup """

        save = load_save()
        self.control_handler = Controls_Handler(save)
        

        self.actions = {"Left": False, "Right": False, "Up": False, "Down": False, "Start": False, "Select": False, 
                   "Jump": False, "Attack" : False, "Magic": False, "Dodge" : False, "LB": False, "RB" : False}

        """ sound """

        main_sound = pygame.mixer.Sound("./audio/main.ogg")
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)


    def run(self):

        while self.playing:
          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == self.control_handler.controls['Start']:
                        self.main_menu_running = True
                        self.playing = False
                        self.main_menu()                     

                    if event.key == self.control_handler.controls['Dodge'] and self.player.on_ground and (not self.player.recovery or self.player.attack_id == "attack"):
                        self.player.recovery = True
                        self.player.attack_time = pygame.time.get_ticks()
                        self.player.attack_id = "backdash"
                        self.player.backdash()

                    if event.key == self.control_handler.controls['Down'] and self.player.attack_id == "backdash":
                        self.player.recovery = False

                    if event.key == self.control_handler.controls['Attack'] and not self.player.recovery:
                        self.player.recovery = True
                        self.player.attack_time = pygame.time.get_ticks()
                        self.player.attack_id = "attack"
                        self.player.create_attack()
                        self.player.weapon_attack_sound.play()

                    if event.key == self.control_handler.controls['Jump'] and pygame.key.get_pressed()[pygame.K_DOWN] and not self.player.d_jump_on and not self.player.recovery:
                        self.player.direction.y = 0
                        self.player.attack_id = "divekick"
                        self.player.divekick()                       
                                                                                                               
                    if event.key == self.control_handler.controls['Jump'] and self.player.status in ["jump", "fall"] and self.player.d_jump_on: 
                        self.player.start_height = self.player.collision_rect.bottom
                        self.player.d_jump_on = False
                        self.player.direction.y = 0
                        self.player.jumping = True    
                        
                    if event.key == self.control_handler.controls['Jump'] and not self.player.recovery and (self.player.on_ground or self.player.status == 'wallhang'): 
                        self.player.start_height = self.player.collision_rect.bottom
                        self.player.start_width = self.player.collision_rect.right

                        if pygame.key.get_pressed()[self.control_handler.controls['Down']]:
                            self.player.jumpdown = True
                        
                        else:

                            if self.player.status == 'wallhang':
                                self.player.walljump = True

                            self.player.jumping = True
        
                    if event.key == self.control_handler.controls['Magic'] and not self.player.recovery:

                        if self.player.hold_up:   
                            self.magic_index = 1
                        else:
                            self.magic_index = 0 
                            
                        style = list(magic_data.keys())[self.magic_index]
                        strength = list(magic_data.values())[self.magic_index]['strength'] + self.player.stats['magic']
                        cost = list(magic_data.values())[self.magic_index]['cost']
                        if self.player.energy >= cost:  
                            self.player.recovery = True
                            self.player.attack_time = pygame.time.get_ticks()                                                  
                            self.player.attack_id = "blaze"
                            self.player.create_magic(style, strength, cost)


                    if event.key == self.control_handler.controls['Select']:
                        self.level.toggle_menu()


                elif event.type == pygame.KEYUP:
                    if event.key == self.control_handler.controls['Jump']:
                        self.player.jumping = False   
                                       

            self.control_handler.update(self.actions)

            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def main_menu(self):
        menu_font = pygame.font.Font('./graphics/font/8-BIT WONDER.TTF', 50)
        menu_options = ["Start", "Options", "Exit"]
        selected = 0

        def handle_events():
            nonlocal selected

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == self.control_handler.controls['Down']:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_UP or event.key == self.control_handler.controls['Up']:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.playing = True
                            self.main_menu_running = False
                            self.run()
                        elif selected == 1:
                            self.options_menu()

                        elif selected == 2:
                            pygame.quit()
                            sys.exit()

            self.control_handler.update(self.actions)

        while self.main_menu_running:
            self.load_and_blit_image('./graphics/menu/layer_1.png', (100, 0))
            self.load_and_blit_image('./graphics/menu/layer_2.png', (0, 0))
            self.load_and_blit_image('./graphics/menu/layer_3.png', (0, 0))


            handle_events()

            for i, option in enumerate(menu_options):
                if i == selected:
                    text = menu_font.render(option, True, "white")
                else:
                    text = menu_font.render(option, True, "gray")
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i*50))
                self.screen.blit(text, text_rect)

            pygame.display.update()
            self.clock.tick(FPS)

    def load_and_blit_image(self, image_path, position):
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(image, position)


    def options_menu(self):
        menu_font = pygame.font.Font('./graphics/font/8-BIT WONDER.TTF', 50)
        menu_options = ["Sound", "Keyboard", "Joystick", "Back"]
        selected = 0

        while True:
            self.load_and_blit_image('./graphics/menu/layer_1.png', (100, 0))
            self.load_and_blit_image('./graphics/menu/layer_2.png', (0, 0))
            self.load_and_blit_image('./graphics/menu/layer_3.png', (0, 0)) 
 
 
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == self.control_handler.controls['Down']:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_UP or event.key == self.control_handler.controls['Up']:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.sound_options()
                        elif selected == 1:
                            # keyboard options
                            import control_config
                        elif selected == 2:
                            # joystick options
                            pass
                        elif selected == 3:
                            return

            
            for i, option in enumerate(menu_options):
                if i == selected:
                    text = menu_font.render(option, True, "white")
                else:
                    text = menu_font.render(option, True, "gray")
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i*50))
                self.screen.blit(text, text_rect)

            pygame.display.update()
            self.clock.tick(FPS)


    def sound_options(self):
        menu_font = pygame.font.Font('./graphics/font/8-BIT WONDER.TTF', 50)
        menu_options = ["Volume Up", "Volume Down", "Back"]
        selected = 0
        volume = pygame.mixer.music.get_volume()

        def handle_events():
            nonlocal selected, volume

            for event in pygame.event.get():
                self.load_and_blit_image('./graphics/menu/layer_1.png', (100, 0))
                self.load_and_blit_image('./graphics/menu/layer_2.png', (0, 0))
                self.load_and_blit_image('./graphics/menu/layer_3.png', (0, 0))
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == self.control_handler.controls['Down']:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_UP or event.key == self.control_handler.controls['Up']:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            volume = min(volume + 0.1, 1.0)
                            pygame.mixer.music.set_volume(volume)
                        elif selected == 1:
                            volume = max(volume - 0.1, 0.0)
                            pygame.mixer.music.set_volume(volume)
                        elif selected == 2:
                            self.main_menu_running = True

            self.control_handler.update(self.actions)

        while self.main_menu_running:

            handle_events()

            for i, option in enumerate(menu_options):
                if i == selected:
                    text = menu_font.render(option + " (" + str(int(volume * 100)) + "%)", True, "white")
                else:
                    text = menu_font.render(option + " (" + str(int(volume * 100)) + "%)", True, "gray")
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i*50))
                self.screen.blit(text, text_rect)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.main_menu()