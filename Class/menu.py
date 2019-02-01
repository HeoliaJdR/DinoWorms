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

    def eventMenu(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if self.constMenu == constants.MAIN_MENU:
                    if mousePos[0] > self.size[0]/4 and mousePos[0] < self.size[0]/3 and mousePos[1] > 300 and mousePos[1] < 400:
                        return constants.ACTION_PLAY
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

            if event.type == pygame.QUIT:
                return constants.ACTION_LEAVE
        return constants.ACTION_WAITING

    def printMenuBackGround(self, screen):
        screen.blit(self.menuBackground, (0, 0))

    def chooseMenu(self, screen):
        self.printMenuBackGround(screen)
        if self.constMenu == constants.MAIN_MENU:
            self.printMainMenu(screen)
        elif self.constMenu == constants.PAUSE_MENU:
            self.printPauseMenu(screen)

    def printMainMenu(self, screen):
        mainMenu = self.bigFont.render("Bienvenue dans DinoWorms !", True, (255,0,0,255))
        playButton = self.menuFont.render("Jouer", False, (255,0,0,255))
        leaveButton = self.menuFont.render("Quitter", False, (255,0,0,255))

        screen.blit(mainMenu, (self.size[0]/5, 100))
        screen.blit(playButton, (self.size[0] / 4, 300))
        screen.blit(leaveButton, (self.size[0] / 4, 400))

    def printPauseMenu(self, screen):
        continueMenu = self.menuFont.render("Reprendre", False, (255, 0, 0, 255))
        playButton = self.menuFont.render("Recommencer", False, (255, 0, 0, 255))
        backButton = self.menuFont.render("Retourner au menu", False, (255, 0, 0, 255))
        leaveButton = self.menuFont.render("Quitter", False, (255, 0, 0, 255))

        screen.blit(continueMenu, (self.size[0] / 4, 100))
        screen.blit(playButton, (self.size[0] / 4, 200))
        screen.blit(backButton, (self.size[0] / 4, 300))
        screen.blit(leaveButton, (self.size[0] / 4, 400))