import pygame, sys
from controls import Controls_Handler
from support import load_save, reset_keys


save, joy_save = load_save()
control_handler = Controls_Handler(save, joy_save)
joysbutton = control_handler.joystick
joy = pygame.joystick.Joystick(0).get_button
actions = {
    "Left": False,
    "Right": False,
    "Up": False,
    "Down": False,
    "Start": False,
    "Select": False,
    "Jump": False,
    "Attack": False,
    "Magic": False,
    "Dodge": False,
    "LB": False,
    "RB": False,
    "Escape": False,
}


def input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.JOYDEVICEADDED:
            joystick = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if event.type == pygame.JOYDEVICEREMOVED:
            joystick = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                actions["Escape"] = True
            if event.key == control_handler.controls["Left"]:
                actions["Left"] = True
            if event.key == control_handler.controls["Right"]:
                actions["Right"] = True
            if event.key == control_handler.controls["Up"]:
                actions["Up"] = True
            if event.key == control_handler.controls["Down"]:
                actions["Down"] = True
            if event.key == control_handler.controls["Attack"]:
                actions["Attack"] = True
            if event.key == control_handler.controls["Jump"]:
                actions["Jump"] = True
            if event.key == control_handler.controls["Dodge"]:
                actions["Dodge"] = True  
            if event.key == control_handler.controls["Magic"]:
                actions["Magic"] = True
            if event.key == control_handler.controls["Start"]:
                actions["Start"] = True
            if event.key == control_handler.controls["Select"]:
                actions["Select"] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                actions["Escape"] = False
            if event.key == control_handler.controls["Left"]:
                actions["Left"] = False
            if event.key == control_handler.controls["Right"]:
                actions["Right"] = False
            if event.key == control_handler.controls["Up"]:
                actions["Up"] = False
            if event.key == control_handler.controls["Down"]:
                actions["Down"] = False
            if event.key == control_handler.controls["Attack"]:
                actions["Attack"] = False
            if event.key == control_handler.controls["Jump"]:
                actions["Jump"] = False
            if event.key == control_handler.controls["Dodge"]:
                actions["Dodge"] = False
            if event.key == control_handler.controls["Magic"]:
                actions["Magic"] = False
            if event.key == control_handler.controls["Select"]:
                actions["Select"] = False
            if event.key == control_handler.controls["Start"]:
                actions["Start"] = False

        if event.type == pygame.JOYHATMOTION:
            hat = pygame.joystick.Joystick(0).get_hat(0)
            if hat[0] == 1:  # right
                actions["Right"] = True
            else:
                actions["Right"] = False
            if hat[0] == -1:  # left
                actions["Left"] = True
            else:
                actions["Left"] = False
            if hat[1] == 1:  # up
                actions["Up"] = True
            else:
                actions["Up"] = False
            if hat[1] == -1:  # down
                actions["Down"] = True
            else:
                actions["Down"] = False

        if event.type == pygame.JOYAXISMOTION:
            if pygame.joystick.Joystick(0).get_axis(0) > 0.5:
                actions["Right"] = True

            elif pygame.joystick.Joystick(0).get_axis(0) < -0.5:
                actions["Left"] = True

            # if pygame.joystick.Joystick(0).get_axis(1) > 0.5:
            #     pass
            #     actions["Down"] = True

            # elif pygame.joystick.Joystick(0).get_axis(1) < -0.5:
            #     pass
            #     actions["Up"] = True
                
        if event.type == pygame.JOYBUTTONDOWN:
            if joy(joysbutton["Attack"]):
                actions["Attack"] = True
            if joy(joysbutton["Jump"]):
                actions["Jump"] = True
            if joy(joysbutton["Dodge"]):
                actions["Dodge"] = True
            if joy(joysbutton["Magic"]):
                actions["Magic"] = True
            if joy(joysbutton["Start"]):
                actions["Start"] = True
            if joy(joysbutton["Select"]):
                actions["Select"] = True

        if event.type == pygame.JOYBUTTONUP:
            
            if event.button == joysbutton["Attack"]:
                actions["Attack"] = False
            if event.button == joysbutton["Jump"]:
                actions["Jump"] = False
            if event.button == joysbutton["Dodge"]:
                actions["Dodge"] = False
            if event.button == joysbutton["Magic"]:
                actions["Magic"] = False
            if event.button == joysbutton["Select"]:
                actions["Select"] = False
            if event.button == joysbutton["Start"]:
                actions["Start"] = False
                
                
