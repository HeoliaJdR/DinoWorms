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
        self.collideRect = {"TopL": 0, "BotL": 0, "TopR": 0, "BotR": 0, "Head": 0, "Feet": 0, "Tail": 0}
        self.displayBoxes = 0
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
        pygame.draw.rect(screen, (0, 0, 0), self.rect["BotR"])
        pygame.draw.rect(screen, (0, 0, 0), self.rect["BotL"])
        pygame.draw.rect(screen, (0, 0, 0), self.rect["TopR"])
        pygame.draw.rect(screen, (0, 0, 0), self.rect["TopL"])
        pygame.draw.rect(screen, (255, 0, 0), self.rect["Head"])
        pygame.draw.rect(screen, (255, 0, 0), self.rect["Feet"])
        pygame.draw.rect(screen, (0, 255, 0), self.rect["Tail"])

    def initCharacter(self):
        self.rect  = {
            "TopL": Rect(self.x - (113 / 4), self.y - (150 / 4), 113 / 4, 150 / 4),
            "BotL": Rect(self.x - (113 / 4), self.y, 113 / 4, 150 / 4),
            "TopR": Rect(self.x, self.y - (150 / 4), 113 / 4, 150 / 4),
            "BotR": Rect(self.x, self.y, 113 / 4, 150 / 4),
            "Head": Rect(self.x - 10, self.y - (150 / 4) - 15, 25, 15),
            "Feet": Rect(self.x - 25, self.y - (150 / 4) + 70, 50, 15),
            "Tail": Rect(self.x - 40, self.y, 15, 15)
        }

        #self.playerMask = pygame.mask.from_surface(self.player)
        # self.generatePixel()

    def updateCollideBoxes(self):
        self.rect["Head"] = Rect(self.x - 10, self.y - (150 / 4) - 15, 25, 15)
        self.rect["Feet"] = Rect(self.x - 25, self.y - (150 / 4) + 70, 50, 15)
        self.rect["Tail"] = Rect(self.x - 40, self.y, 15, 15)
        self.rect["TopR"] = Rect(self.x, self.y - (150 / 4), 113 / 4, 150 / 4)
        self.rect["TopL"] = Rect(self.x - (113 / 4), self.y - (150 / 4), 113 / 4, 150 / 4)
        self.rect["BotR"] = Rect(self.x, self.y, 113 / 4, 150 / 4)
        self.rect["BotL"] = Rect(self.x - (113 / 4), self.y, 113 / 4, 150 / 4)

    def displayCharacter(self, screen, area):
        self.initCharacter()
        if self.displayBoxes == 1:
            self.drawCharacter(screen)
        if self.animConstant == constants.IDLE:
            self.launchAnim = self.animIdle.playAnim(screen, self.origAnim)
            self.firstLoop = 1
        if self.animConstant == constants.WALK:
            self.launchAnim = self.animWalk.playAnim(screen, self.origAnim)
            self.firstLoop = 1

    def moveCharacter(self, screen, area):
        if self.wantsToWalkRight:
            if self.direction == 0:
                # self.player = pygame.transform.flip(self.player, True, True)
                self.direction = 1
            self.isCollided(screen, area, "TopR")
            self.isCollided(screen, area, "BotR")
            self.isCollided(screen, area, "Head")
            if self.collideRect["TopR"] == 1: return
            if self.collideRect["BotR"] == 1: return
            if self.collideRect["Head"] == 1: return
            self.x += 4
            self.origAnim = (self.x, self.y)
            for key in self.collideRect:
                self.collideRect[key] = 0
        if self.wantsToWalkLeft:
            if self.direction == 1:
                # self.player = pygame.transform.flip(self.player, True, True)
                self.direction = 0
            self.isCollided(screen, area, "TopL")
            self.isCollided(screen, area, "BotL")
            self.isCollided(screen, area, "Tail")
            if self.collideRect["TopL"] == 1: return
            if self.collideRect["BotL"] == 1: return
            if self.collideRect["Tail"] == 1: return
            self.x -= 4
            self.origAnim = (self.x, self.y)
            for key in self.collideRect:
                self.collideRect[key] = 0


    def isCollided(self, newWorld, area, place):
        for i in self.rect[place]:
            for j in self.rect[place]:
                if i <= 0 or j <= 0 or i >= newWorld.screenW or j >= newWorld.screenH:
                    self.collideRect[place] = 1
                    break
                if area[i][j] == 1:
                    self.collideRect[place] = 1
                    break
                else:
                    self.collideRect[place] = 0
                    break
        print(self.collideRect)
