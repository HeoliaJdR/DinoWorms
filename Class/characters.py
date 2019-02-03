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
        self.touchingPoint = (0, 0)
        self.canMove = [0, 0]
        #self.player = None
        self.spriteSheet = "Imgs/dinoGreen.png"

        """ Ajout des animations"""
        self.launchAnim = False
        self.anim = animation.Animation("Imgs/dinoGreen.png", (680, 630), (0, 0), 10, 3, 4, 60, self.loop)
        self.anim.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.origAnim = (self.x, self.y)

    def drawCharacter(self, screen):
        print("oui")

    def initCharacter(self):
        self.player = pygame.transform.scale(pygame.image.load(self.spriteSheet).convert_alpha(), (300, 300))
        self.rect = Rect(self.x, self.y, 150, 113)
        self.playerMask = pygame.mask.from_surface(self.player)
        #self.generatePixel()

    """
    def generatePixel(self):
        self.spriteSheetMask = pygame.transform.scale(pygame.image.load(self.spriteSheet).convert(), (300, 300))
        for i in range(680):
            for j in range(630):
                pixel = self.spriteSheetMask.get_at((i, j))
                if pixel == (0, 0, 0, 0):
                    self.pixels[i][j] = 0
                else:
                    self.pixels[i][j] = 1
    """

    def displayCharacter(self, screen):
        if self.loop or self.firstLoop == 0:
            self.launchAnim = self.anim.playAnim(screen, self.origAnim)
            self.firstLoop = 1
        #print("Test \n" + str(area))

    def getCollision(self, world, area, canMove):
        #print(self.anim.currentRect, self.rect)
        #print(self.x, self.y)
        print(self.canMove)
        for i in self.rect:
            for j in self.rect:
                if i <= 0 or j <= 0 or i >= world.screenW or j >= world.screenH:
                    print("Hors jeu")
                    self.canMove[canMove] = 1
                    return 1, canMove
                if area[i][j] == 1:
                    print("touché")
                    self.canMove[canMove] = 1
                    return 1, canMove
                else:
                    print("enjeu")
                    return 0



    def moveCharacter(self, screen, key, world, area):
        while pygame.KEYDOWN:
            if key == pygame.K_d:
                if self.direction == 0:
                    self.player = pygame.transform.flip(self.player, True, True)
                    pygame.display.update()
                    self.direction = 1
                if self.getCollision(world, area, 1) == 0 and self.canMove[1] == 0:
                    self.canMove[0] = 0
                    self.x += 10
                    self.rect = Rect(self.x, self.y, 150, 113)
                    self.origAnim = (self.x, self.y)
            if key == pygame.K_a:
                if self.direction == 1:
                    self.player = pygame.transform.flip(self.player, True, True)
                    pygame.display.update()
                    self.direction = 0
                if self.getCollision(world, area, 0) == 0 and self.canMove[0] == 0:
                    self.canMove[1] = 0
                    self.x -= 10
                    self.rect = Rect(self.x, self.y, 150, 113)
                    self.origAnim = (self.x, self.y)
            if pygame.KEYUP:
                break


