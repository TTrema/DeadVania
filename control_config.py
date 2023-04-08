import pygame
from support import load_save, reset_keys
from controls import Controls_Handler
from settings import *


################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))
running = True

actions = {"Left": False, "Right": False, "Up": False, "Down": False, "Start": False, "Jump": False}

################################ LOAD THE CURRENT SAVE FILE #################################
save = load_save()
control_handler = Controls_Handler(save)
################################# GAME LOOP ##########################
while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == control_handler.controls["Left"]:
                actions["Left"] = True
            if event.key == control_handler.controls["Right"]:
                actions["Right"] = True
            if event.key == control_handler.controls["Up"]:
                actions["Up"] = True
            if event.key == control_handler.controls["Down"]:
                actions["Down"] = True
            if event.key == control_handler.controls["Start"]:
                actions["Start"] = True
            if event.key == control_handler.controls["Jump"]:
                actions["Jump"] = True

        if event.type == pygame.KEYUP:
            if event.key == control_handler.controls["Left"]:
                actions["Left"] = False
            if event.key == control_handler.controls["Right"]:
                actions["Right"] = False
            if event.key == control_handler.controls["Up"]:
                actions["Up"] = False
            if event.key == control_handler.controls["Down"]:
                actions["Down"] = False
            if event.key == control_handler.controls["Start"]:
                actions["Start"] = False
            if event.key == control_handler.controls["Jump"]:
                actions["Jump"] = False

    ################################# UPDATE THE GAME #################################
    control_handler.update(actions)
    ################################# RENDER WINDOW AND DISPLAY #################################
    window.fill((135, 206, 235))
    canvas.fill((135, 206, 235))
    control_handler.render(canvas)
    window.blit(pygame.transform.scale(canvas, (SCREEN_WIDTH * 1.8, SCREEN_HEIGHT * 1.8)), (180, 0))
    pygame.display.update()
    reset_keys(actions)
