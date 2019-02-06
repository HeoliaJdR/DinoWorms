import pygame
import constants

class Menu:
    def __init__(self, winSize):
        if not pygame.font.get_init():
            pygame.font.init
        self.menuBackgroundPath = "Imgs/principal_menu.jpg"
        self.menuBackground = pygame.transform.scale(pygame.image.load(self.menuBackgroundPath), (winSize[0] - 200, winSize[1] - 200))
        self.bigFont = pygame.font.Font("Fonts/Quantify.ttf", 48)
        self.menuFont = pygame.font.Font("Fonts/Quantify.ttf", 36)
        self.size = winSize
        self.constMenu = constants.MAIN_MENU
        self.nbDino = 1

    def eventMenu(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if self.constMenu == constants.VICTORY_MENU:
                    return constants.ACTION_BACK_TO_MENU
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if self.constMenu == constants.MAIN_MENU:
                    if mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] > 300 and mousePos[1] < 400:
                        return constants.ACTION_CHOOSE_PLAYER
                    elif mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] > 400 and mousePos[1] < 500:
                        return constants.ACTION_LEAVE
                elif self.constMenu == constants.PAUSE_MENU:
                    if mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] >= 100 and mousePos[1] < 200:
                        return constants.ACTION_CONTINUE
                    elif mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] >= 200 and mousePos[1] < 300:
                        return constants.ACTION_PLAY
                    elif mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] >= 300 and mousePos[1] < 400:
                        return constants.ACTION_BACK_TO_MENU
                    elif mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] >= 400 and mousePos[1] < 500:
                        return constants.ACTION_LEAVE
                elif self.constMenu == constants.PLAYER_MENU:
                    if mousePos[0] > self.size[0]/4 - 100 and mousePos[0] < self.size[0]/4 - 25 and mousePos[1] >= 200 and mousePos[1] < 300:
                        self.nbDino = 1 if self.nbDino - 1 < 1 else self.nbDino - 1
                    elif mousePos[0] > self.size[0] / 4 + 40 and mousePos[0] < self.size[0] / 4 + 140 and mousePos[1] >= 200 and mousePos[1] < 300:
                        self.nbDino = 3 if self.nbDino + 1 > 3 else self.nbDino + 1
                    elif mousePos[0] > self.size[0]/4 - 125 and mousePos[0] < self.size[0]/3 - 125 and mousePos[1] >= 350 and mousePos[1] < 450:
                        return constants.ACTION_PLAY
                    elif mousePos[0] > self.size[0]/4 - 125 and mousePos[0] < self.size[0]/3 - 125 and mousePos[1] >= 450 and mousePos[1] < 550:
                        return constants.ACTION_BACK_TO_MENU
                elif self.constMenu == constants.VICTORY_MENU:
                    return constants.ACTION_BACK_TO_MENU

            if event.type == pygame.QUIT:
                return constants.ACTION_LEAVE
        return constants.ACTION_WAITING

    def printMenuBackGround(self, screen):
        screen.blit(self.menuBackground, (0, 0))

    def chooseMenu(self, screen, team):
        self.printMenuBackGround(screen)
        if self.constMenu == constants.MAIN_MENU:
            self.printMainMenu(screen)
        elif self.constMenu == constants.PAUSE_MENU:
            self.printPauseMenu(screen)
        elif self.constMenu == constants.PLAYER_MENU:
            self.printPlayMenu(screen)
        elif self.constMenu == constants.VICTORY_MENU:
            self.printVictoryMenu(screen, team)

    def printMainMenu(self, screen):
        mainMenu = self.bigFont.render("Bienvenue dans DinoWorms !", True, (255,0,0,255))
        playButton = self.menuFont.render("Jouer", False, (255,0,0,255))
        leaveButton = self.menuFont.render("Quitter", False, (255,0,0,255))

        screen.blit(mainMenu, (self.size[0]/5, 100))
        screen.blit(playButton, (self.size[0] / 4, 300))
        screen.blit(leaveButton, (self.size[0] / 4, 400))

    def printPlayMenu(self, screen):
        dino = self.bigFont.render("Combien de dino par équipe ?", False, (255, 0, 0, 255))
        playButton = self.menuFont.render("Jouer", False, (255,0,0,255))
        backButton = self.menuFont.render("Retourner au menu", False, (255, 0, 0, 255))
        nbPlayer = self.bigFont.render(str(self.nbDino), False, (255, 0, 0, 255))
        leftArrow = pygame.transform.scale(pygame.image.load("Imgs/left_arrow.png"), (100,100))
        rigthArrow = pygame.transform.scale(pygame.image.load("Imgs/right_arrow.png"), (100,100))

        screen.blit(dino, (self.size[0] / 5, 100))
        screen.blit(leftArrow, (self.size[0] / 4 - 125, 200))
        screen.blit(nbPlayer, (self.size[0] / 4, 225))
        screen.blit(rigthArrow, (self.size[0] / 4 + 40, 200))
        screen.blit(playButton, (self.size[0] / 4 - 125, 350))
        screen.blit(backButton, (self.size[0] / 4 - 125, 450))

    def printPauseMenu(self, screen):
        continueMenu = self.menuFont.render("Reprendre", False, (255, 0, 0, 255))
        playButton = self.menuFont.render("Recommencer", False, (255, 0, 0, 255))
        backButton = self.menuFont.render("Retourner au menu", False, (255, 0, 0, 255))
        leaveButton = self.menuFont.render("Quitter", False, (255, 0, 0, 255))

        screen.blit(continueMenu, (self.size[0] / 4, 100))
        screen.blit(playButton, (self.size[0] / 4, 200))
        screen.blit(backButton, (self.size[0] / 4, 300))
        screen.blit(leaveButton, (self.size[0] / 4, 400))

    def printVictoryMenu(self, screen, team):
        victoryStr = "Victoire de la team : " + str(team)
        victoryFont = self.bigFont.render(victoryStr, True, (255, 0, 0))

        screen.blit(victoryFont, (self.size[0] / 2, self.size[1] / 2))