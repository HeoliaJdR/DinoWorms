import os
import pygame
from pygame.locals import *
import tkinter as tk

# Adapt to the monitor size
rootSystem = tk.Tk()

screenWith = rootSystem.winfo_screenwidth()
screenHeight = rootSystem.winfo_screenheight()

#Start Pygame
pygame.display.init()
screen = pygame.display.set_mode((screenWith, screenHeight), pygame.FULLSCREEN)

dinoPath = "Imgs/soloDino.png"
dino = pygame.image.load(dinoPath).convert_alpha()
screen.blit(dino, (0,0))


pygame.display.flip()
wait = True

while wait:
    for event in pygame.event.get():
        if event.type == QUIT:
            wait = False

pygame.quit()