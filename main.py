import pygame
from pygame.locals import *
import constants
import tkinter as tk
from Class import characters
from Class import world

# Adapt to the monitor size
rootSystem = tk.Tk()

screenWith = rootSystem.winfo_screenwidth()
screenHeight = rootSystem.winfo_screenheight()

#Start Pygame
pygame.display.init()
screen = pygame.display.set_mode((screenWith, screenHeight), pygame.FULLSCREEN)

#Start World
newWorld = world.World(screenHeight, screenWith)
newWorld.initBackground()
newWorld.printBackground(screen)
"""

#Start Pygame
pygame.display.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.FULLSCREEN)

characters.displayDinosaurs(screen)

>>>>>>> [+] Characters + Sprite (Not Working Yet)
"""
pygame.display.flip()

wait = True

while wait:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == K_f:
            wait = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            newWorld.destroyArea(event.pos[0], event.pos[1])
            newWorld.printBackground(screen)
            pygame.display.flip()


pygame.quit()