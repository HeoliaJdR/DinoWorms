import pygame
import constants
import tkinter as tk
from Class import game
from Class import menu

# Adapt to the monitor size
rootSystem = tk.Tk()

screenWith = rootSystem.winfo_screenwidth()
screenHeight = rootSystem.winfo_screenheight()

#Start Pygame
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((screenWith - 200, screenHeight - 200), pygame.RESIZABLE)

# Init Menu
mainMenu = menu.Menu((screenWith, screenHeight))

wait = True
isFullScreen = False
inMenu = True
leavingMenu = False
endOfGame = constants.CONTINUE_GAME

while wait:
    if inMenu:
        leavingMenu = False
        mainMenu.chooseMenu(screen, endOfGame)
        menuAction = mainMenu.eventMenu()

        if menuAction == constants.ACTION_PLAY:
            inMenu = False
            leavingMenu = True
            newGame = game.Game(mainMenu.nbPlayers, mainMenu.nbDino, (screenWith - 200, screenHeight - 200))
        elif menuAction == constants.ACTION_CONTINUE:
            inMenu = False
            leavingMenu = True
        elif menuAction == constants.ACTION_BACK_TO_MENU:
            mainMenu.constMenu = constants.MAIN_MENU
        elif menuAction == constants.ACTION_LEAVE:
            wait = False
        elif menuAction == constants.ACTION_CHOOSE_PLAYER:
            mainMenu.constMenu = constants.PLAYER_MENU
    else:
        for event in pygame.event.get():
            if leavingMenu:
                leavingMenu = False
                break

            newGame.gameEvent(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inMenu = True
                    mainMenu.constMenu = constants.PAUSE_MENU
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
                if event.key == pygame.K_h:
                    changeWind = True

            if event.type == pygame.QUIT:
                wait = False

        endOfGame = newGame.printElements(screen)
        if endOfGame:
            inMenu = True
            mainMenu.constMenu = constants.VICTORY_MENU

    pygame.display.update()
    pygame.time.delay(int(1000 / constants.FRAME_PER_SECOND))

pygame.quit()