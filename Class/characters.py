import pygame
from pygame.locals import *
import constants
from Class import sprites
from Class import animation

class Characters:
    def __init__(self, hp, team, x, y, loop):
        self.hp = hp
        self.team = team
        self.x = x
        self.y = y
        self.posture = 0
        self.direction = 0
        self.loop = loop
        self.firstLoop = 0
        #self.player = None
        #self.spriteSheet = "Imgs/dinoGreen.png"
        self.animConstant = constants.IDLE
        self.wantsToWalkRight = False
        self.wantsToWalkLeft = False

        """ Ajout des animations"""
        self.launchAnim = False
        self.animWalk = animation.Animation("Imgs/dinoGreenWalk.png", (680, 475), (0, 0), 10, 3, 4, 60, True)
        self.animWalk.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.animIdle = animation.Animation("Imgs/dinoGreenIdle.png", (680, 475), (0, 0), 10, 3, 4, 60, True)
        self.animIdle.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.origAnim = (self.x, self.y)

    def drawCharacter(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rectBotRight)
        pygame.draw.rect(screen, (0, 0, 0), self.rectBotLeft)
        pygame.draw.rect(screen, (0, 0, 0), self.rectTopRight)
        pygame.draw.rect(screen, (0, 0, 0), self.rectTopLeft)
        pygame.draw.rect(screen, (255, 0, 0), self.rectTop)
        pygame.draw.rect(screen, (255, 0, 0), self.rectBot)
        pygame.draw.rect(screen, (0, 255, 0), self.rectTail)

    def initCharacter(self):
        #self.player = pygame.transform.scale(pygame.image.load(self.animIdle.spriteSheet).convert_alpha(), (300, 300))
        self.rectTop = Rect(self.x - 10, self.y - (150 / 4) - 15, 25, 15)
        self.rectBot = Rect(self.x - 25, self.y - (150 / 4) + 70, 50, 15)
        self.rectTail = Rect(self.x - 40, self.y, 15, 15)
        self.rectTopRight = Rect(self.x, self.y - (150 / 4), 113 / 4, 150 / 4)
        self.rectTopLeft = Rect(self.x - (113 / 4), self.y - (150 / 4), 113 / 4, 150 / 4)
        self.rectBotRight = Rect(self.x, self.y, 113 / 4, 150 / 4)
        self.rectBotLeft = Rect(self.x - (113 / 4), self.y, 113 / 4, 150 / 4)

        #self.playerMask = pygame.mask.from_surface(self.player)
        # self.generatePixel()

    def updateCollideBoxes(self):
        self.rectTop = Rect(self.x - 10, self.y - (150 / 4) - 15, 25, 15)
        self.rectBot = Rect(self.x - 25, self.y - (150 / 4) + 70, 50, 15)
        self.rectTail = Rect(self.x - 40, self.y, 15, 15)
        self.rectTopRight = Rect(self.x, self.y - (150 / 4), 113 / 4, 150 / 4)
        self.rectTopLeft = Rect(self.x - (113 / 4), self.y - (150 / 4), 113 / 4, 150 / 4)
        self.rectBotRight = Rect(self.x, self.y, 113 / 4, 150 / 4)
        self.rectBotLeft = Rect(self.x - (113 / 4), self.y, 113 / 4, 150 / 4)

    def displayCharacter(self, screen, area):
        self.initCharacter()
        self.drawCharacter(screen)
        if self.animConstant == constants.IDLE:
            self.launchAnim = self.animIdle.playAnim(screen, self.origAnim)
            self.firstLoop = 1
        if self.animConstant == constants.WALK:
            self.launchAnim = self.animWalk.playAnim(screen, self.origAnim)
            self.firstLoop = 1

    def moveCharacter(self):
        if self.wantsToWalkRight:
            if self.direction == 0:
                # self.player = pygame.transform.flip(self.player, True, True)
                self.direction = 1
            self.x += 4
            self.origAnim = (self.x, self.y)
        if self.wantsToWalkLeft:
            if self.direction == 1:
                # self.player = pygame.transform.flip(self.player, True, True)
                self.direction = 0
            self.x -= 4
            self.origAnim = (self.x, self.y)