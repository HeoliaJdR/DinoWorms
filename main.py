import pygame
from pygame.locals import *
import constants
import tkinter as tk
from Class import characters
from Class import world
from Class import projectile
from Class import sprites

# Adapt to the monitor size
rootSystem = tk.Tk()

screenWith = rootSystem.winfo_screenwidth()
screenHeight = rootSystem.winfo_screenheight()

#Start Pygame
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((screenWith - 200, screenHeight - 200), pygame.RESIZABLE)

#Start World
newWorld = world.World(screenHeight - 200, screenWith - 200)
newWorld.initBackground()
newWorld.printBackground(screen)

#init projectile(test)
proj = projectile.projectile()
proj.initProjectile()

player = characters.Characters(100)
player.initCharacter()


"""
#Start Pygame
pygame.display.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.FULLSCREEN)

characters.displayDinosaurs(screen)

>>>>>>> [+] Characters + Sprite (Not Working Yet)
"""
pygame.display.flip()

wait = True
mouseIsDown = False
isFullScreen = False
changeWind = True

while wait:
    newWorld.printBackground(screen)
    player.displayCharacter(screen)
    if(changeWind):
        newWorld.generateWind()
        changeWind = False
    proj.launchBall(screen,newWorld.getPixels())
    pygame.display.update()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                 wait = False
            if event.key == pygame.K_f:
                if isFullScreen:
                    isFullScreen = False
                    tempScreen = pygame.transform.scale(screen.convert(), (screenWith - 200, screenHeight - 200))
                    pygame.display.quit()
                    pygame.display.init()
                    screen = pygame.display.set_mode((screenWith - 200, screenHeight - 200), pygame.RESIZABLE)
                    screen.blit(tempScreen, (0, 0))
                else:
                    isFullScreen = True
                    tempScreen = pygame.transform.scale(screen.convert(), (screenWith, screenHeight))
                    pygame.display.quit()
                    pygame.display.init()
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screen.blit(tempScreen, (0, 0))
                pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            proj.enableLoading()
        if event.type == pygame.MOUSEBUTTONUP:
            proj.releaseProjectile()

        if event.type == pygame.QUIT:
            wait = False

    #pygame.time.delay(50)
    pygame.display.update()

pygame.quit()