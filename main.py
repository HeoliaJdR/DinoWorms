import pygame
import os

pygame.init()
screen = pygame.display.set_mode((300, 200))

wait = True

while wait:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            wait = False

pygame.quit()