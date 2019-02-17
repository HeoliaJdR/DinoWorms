import pygame
from pygame.locals import *
import constants
import math
from Class import sprites
from Class import animation

class Characters:
    def __init__(self, hp, team, x, y, loop, name):
        self.hp = hp
        self.time = 0
        self.team = team
        self.x = x
        self.y = y
        self.teleport = 1
        self.line = []
        self.posture = 0
        self.direction = 0
        self.previousDiff = 0
        self.loop = loop
        self.firstLoop = 0
        self.collideRect = {
            "TopL": 0,
            "BotL": 0,
            "TopR": 0,
            "BotR": 0,
            "Head": 0,
            "FeetL": 0,
            "FeetR": 0,
            "Tail": 0
        }
        self.name = name
        self.canGoDown = 1
        self.displayBoxes = 0
        self.isJumping = False
        #self.player = None
        #self.spriteSheet = "Imgs/dinoGreen.png"
        self.animConstant = constants.IDLE
        self.wantsToWalkRight = False
        self.wantsToWalkLeft = False
        self.rect = {
            "TopL": Rect(self.x - (113 / 4), self.y - (150 / 4), 113 / 4, 150 / 4),
            "BotL": Rect(self.x - (113 / 4), self.y, 113 / 4, 90 / 4),
            "TopR": Rect(self.x, self.y - (150 / 4), 113 / 4, 150 / 4),
            "BotR": Rect(self.x, self.y, 113 / 4, 90 / 4),
            "Head": Rect(self.x - 10, self.y - (150 / 4) - 15, 25, 15),
            "FeetL": Rect(self.x - 35, self.y - (150 / 4) + 70, 50, 15),
            "FeetR": Rect(self.x + 35, self.y - (150 / 4) + 70, 50, 15),
            "Tail": Rect(self.x - 40, self.y, 15, 15)
        }
        self.allRect = self.rect["Tail"]
        for rect in self.rect.values():
            self.allRect = self.allRect.union(rect)
        self.size = (100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE)

        self.isActivePlayer = False

        """ Ajout des animations"""
        self.launchAnim = False
        self.animWalk = animation.Animation("Imgs/dinoGreenWalk.png", (680, 475), (0, 0), 10, 3, 4, 60, True)
        self.animWalk.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.animIdle = animation.Animation("Imgs/dinoGreenIdle.png", (680, 475), (0, 0), 10, 3, 4, 60, True)
        self.animIdle.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.animDead = animation.Animation("Imgs/dinoGreenDead.png", (680, 470), (0, 0), 8, 3, 3, 140, False)
        self.animDead.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.origAnim = (self.x, self.y)

    def drawCharacter(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect["BotR"])
        pygame.draw.rect(screen, (0, 0, 0), self.rect["BotL"])
        pygame.draw.rect(screen, (0, 0, 0), self.rect["TopR"])
        pygame.draw.rect(screen, (0, 0, 0), self.rect["TopL"])
        pygame.draw.rect(screen, (255, 0, 0), self.rect["Head"])
        pygame.draw.rect(screen, (255, 0, 0), self.rect["FeetL"])
        pygame.draw.rect(screen, (255, 0, 0), self.rect["FeetR"])
        pygame.draw.rect(screen, (0, 255, 0), self.rect["Tail"])

    def jumpCharacter(self, world, area):
        if self.isJumping:
            self.isCollided(world, area, "Head", 0)
            if self.collideRect["Head"] == 1:
                self.isJumping = False
                self.canGoDown = 1
                return
            if self.wantsToWalkRight:
                self.x += 3
            if self.wantsToWalkLeft:
                self.x -= 3
            self.time += 0.5
            self.y -= 25
        if self.time > 2:
            self.isJumping = False
            self.time = 0
            self.canGoDown = 1

    def teleportCharacter(self):
        if self.teleport == 1:
            mousePos = pygame.mouse.get_pos()
            #print(mousePos[0])
            self.x = mousePos[0]
            self.y = mousePos[1]
            for key in self.collideRect:
                self.collideRect[key] = 0
            self.canGoDown = 1
            self.teleport = 0

    def checkSlope(self, world, area):
        counter = 0
        if self.wantsToWalkLeft:
            newX = self.rect["FeetL"].x
            newY = self.rect["FeetL"].y + 16
            counter = 0
            for i in range(1, 15):
                if newY + i < world.screenH:
                    if area[newX][newY+i] == 0:
                        counter -= 1
                    if area[newX][newY-i] == 1:
                        counter += 1
        if self.wantsToWalkRight:
            newX = self.rect["FeetR"].x
            newY = self.rect["FeetR"].y + 16
            for i in range(1, 15):
                #print("Rect in : " + str(self.rect["FeetR"]))
                if newY+i < world.screenH:
                    if area[newX][newY+i] == 0:
                        counter += 1
                    if area[newX][newY-i] == 1:
                        counter -= 1
        #print(counter)
        return counter

    def updateYPos(self, world, area):
        self.isCollided(world, area, "FeetL", 7)
        self.isCollided(world, area, "FeetR", 7)
        if self.canGoDown == 1:
            self.y += constants.GRAVITY
        self.updateCollideBoxes()
        self.origAnim = (self.x, self.y)

    def updateCollideBoxes(self):
        self.rect = {
            "TopL": Rect(self.x - (113 / 4), self.y - (150 / 4), 113 / 4, 150 / 4),
            "BotL": Rect(self.x - (113 / 4), self.y, 113 / 4, 90 / 4),
            "TopR": Rect(self.x, self.y - (150 / 4), 113 / 4, 150 / 4),
            "BotR": Rect(self.x, self.y, 113 / 4, 90 / 4),
            "Head": Rect(self.x - 10, self.y - (150 / 4) - 15, 25, 15),
            "FeetL": Rect(self.x - 15, self.y - (150 / 4) + 70, 15, 15),
            "FeetR": Rect(self.x + 15, self.y - (150 / 4) + 70, 15, 15),
            "Tail": Rect(self.x - 40, self.y, 15, 15)
        }

        self.allRect = self.rect["Tail"]
        for rect in self.rect.values():
            self.allRect = self.allRect.union(rect)

    def displayCharacter(self, screen, area, world):
        """if self.isJumping == True:
            self.time += 0.5
            pos = self.jumpCharacter()
            #self.x = pos[0]
            self.y = pos[1]
            self.canGoDown = 1
            if self.time > 3:
                self.isJumping = False
                self.time = 0
                self.displayCharacter(screen, area, world)
        """
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 25, self.y - 100, self.hp, 10), 0)
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 25, self.y - 100, 100, 10), 1)
        if self.displayBoxes == 1:
            self.drawCharacter(screen)
        if self.animConstant == constants.IDLE:
            endAnim = self.launchAnim = self.animIdle.playAnim(screen, self.origAnim)
            self.firstLoop = 1
        if self.animConstant == constants.WALK:
            endAnim = self.launchAnim = self.animWalk.playAnim(screen, self.origAnim)
            self.firstLoop = 1
        if self.animConstant == constants.DEAD:
            endAnim = self.launchAnim = self.animDead.playAnim(screen, self.origAnim)

        return endAnim

    def moveCharacter(self, world, area):
        if self.wantsToWalkRight:
            if self.direction == 0:
                # self.player = pygame.transform.flip(self.player, True, True)
                self.direction = 1
            self.isCollided(world, area, "TopR", 4)
            self.isCollided(world, area, "BotR", 4)
            self.isCollided(world, area, "Head", 4)
            #print(self.collideRect)
            if self.collideRect["Head"] == 1: return
            if self.collideRect["TopR"] == 1: return
            if self.collideRect["BotR"] == 1: return
            self.updateCollideBoxes()
            moveY = self.checkSlope(world, area)
            if moveY > 0:
                self.y += moveY
            elif moveY < 0:
                self.y += moveY
            else:
                self.y = self.y
            self.x += 3
            self.origAnim = (self.x, self.y)
            for key in self.collideRect:
                self.collideRect[key] = 0
        if self.wantsToWalkLeft:
            if self.direction == 1:
                # self.player = pygame.transform.flip(self.player, True, True)
                self.direction = 0
            self.isCollided(world, area, "TopL", 4)
            self.isCollided(world, area, "BotL", 4)
            self.isCollided(world, area, "Tail", 4)
            self.isCollided(world, area, "Head", 4)
            if self.collideRect["Head"] == 1: return
            if self.collideRect["TopL"] == 1: return
            if self.collideRect["BotL"] == 1: return
            if self.collideRect["Tail"] == 1: return
            self.updateCollideBoxes()
            moveY = self.checkSlope(world, area)
            if moveY > 0:
                self.y -= moveY
            elif moveY < 0:
                self.y -= moveY
            else:
                self.y = self.y
            self.x -= 3
            self.origAnim = (self.x, self.y)
            for key in self.collideRect:
                if key != "FeetL" or key != "FeetR":
                    #print(key)
                    self.collideRect[key] = 0

    def isCollided(self, newWorld, area, place, rangePrevision):
        for i in range(self.rect[place].y, self.rect[place].y + self.rect[place].height):
            for j in range(self.rect[place].x, self.rect[place].x + self.rect[place].width):
                if i <= 0 or j <= 0 or i + 15 >= newWorld.screenH - 15 or j + rangePrevision >= newWorld.screenW - 15:
                    if i + 15 >= newWorld.screenH - 10:
                        self.loseHp(100)
                        return
                    self.collideRect[place] = 1
                    if place == "FeetL" or place == "FeetR":
                        self.canGoDown = 0
                    break
                if area[j][i] == 1:
                    self.collideRect[place] = 1
                    if place == "FeetL" or place == "FeetR":
                        #print("Rect in : " + str(self.rect[place]) + "J = " + str(j) + " ; I = " + str(i))
                        #print(str(newWorld.screenW) + " " + str(newWorld.screenH))
                        self.canGoDown = 0
                    break
                else:
                    self.collideRect[place] = 0
                    break

    def loseHp(self, hp):
        self.hp -= hp

        if self.hp <= 0:
            self.animConstant = constants.DEAD
