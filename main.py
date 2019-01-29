import os
import pygame
import tkinter as tk

# Adapt to the monitor size
rootSystem = tk.Tk()

screenWith = rootSystem.winfo_screenwidth()
screenHeight = rootSystem.winfo_screenheight()

#Start Pygame
pygame.display.init()
screen = pygame.display.set_mode((screenWith, screenHeight), pygame.FULLSCREEN)

wait = True

while wait:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            wait = False

pygame.quit()