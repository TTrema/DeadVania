import pygame
from pygame._sdl2 import controller

controller.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]





def movement(player):
    keypress = pygame.key.get_pressed()
    
    if len(joysticks) > 0:
        joy = pygame.joystick.Joystick(0).get_button
        hat_0 = pygame.joystick.Joystick(0).get_hat(0)[0]
        hat_1 = pygame.joystick.Joystick(0).get_hat(0)[1]
        axis_0 = pygame.joystick.Joystick(0).get_axis(0)
        axis_1 = pygame.joystick.Joystick(0).get_axis(1)
        
    else:
        joy, hat_0, hat_1, axis_0, axis_1 = None, 0, 0, 0, 0

    """ keyboar """

    if hat_1 or axis_1 < -0.2 or keypress[player.control_handler.controls["Up"]]:
        player.hold_up = True
    else:
        player.hold_up = False

    if hat_1 == -1 or axis_1 > 0.2 or keypress[player.control_handler.controls["Down"]]:

        player.crouch = True
        if (player.status == "fall" or "divekck") and not player.on_ground:
            pass
    else:
        player.crouch = False

    if (hat_0 == 1 or axis_0 > 0.2 or keypress[player.control_handler.controls["Right"]]) and not player.recovery:
        player.direction.x = 1
        player.facing_right = True

    elif (hat_0 == -1 or axis_0 < -0.2 or keypress[player.control_handler.controls["Left"]]) and not player.recovery:
        player.direction.x = -1
        player.facing_right = False
    else:
        player.direction.x = 0

        # """ left-stick """

        # if axis_0 > 0.2 and not player.recovery:
        #     player.direction.x = 1
        #     player.facing_right = True

        # elif axis_0 < -0.2 and not player.recovery:
        #     player.direction.x = -1
        #     player.facing_right = False
        # else:
        #     player.direction.x = 0

        # """ d-pad """

        # if hat_0[1] == 1:
        #     player.hold_up = True
        # else:
        #     player.hold_up = False

        # if hat_0[1] == -1:
        #     if player.status == "fall" or "divekck":
        #         player.jumpdown = True
        #     player.crouch = True
        # else:
        #     player.crouch = False

        # if hat_0[0] == 1 and not player.recovery:
        #     player.direction.x = 1
        #     player.facing_right = True

        # elif hat_0[0] == -1 and not player.recovery:
        #     player.direction.x = -1
        #     player.facing_right = False
        # else:
        player.direction.x = 0


def Up(player):
    pass


def Down(player):
    pass


def right(player):
    pass


def Left(player):
    pass
