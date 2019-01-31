import pygame
import random
from pygame import gfxdraw

class World:
    def __init__(self, screenHeight, screenWidth):
        self.backgroundSkyImgPath = "Imgs/backgroundSky.jpg"
        self.backgroundGroundImgPath = "Imgs/bg_ship.png"
        self.backgroundMaskImgPath = "Imgs/bg_ship.jpg"
        self.screenH = screenHeight
        self.screenW = screenWidth
        self.pixels = [[1] * screenHeight for i in range(screenWidth)]

    def generatePixel(self):
        self.backgroundMask = pygame.transform.scale(pygame.image.load(self.backgroundMaskImgPath).convert(), (self.screenW, self.screenH))
        for i in range(self.screenW):
            for j in range(self.screenH):
                pixel = self.backgroundMask.get_at((i,j))
                if pixel == (0,0,0,255):
                    self.pixels[i][j] = 0
                else:
                    self.pixels[i][j] = 1

    def fastRegeneratePixel(self, xSrc, ySrc, constArea):
        xStart = 0 if xSrc - constArea < 0 else xSrc - constArea
        xEnd = self.screenW if xSrc + constArea > self.screenH else xSrc + constArea
        yStart = 0 if ySrc - constArea < 0 else ySrc - constArea
        yEnd = self.screenH if ySrc + constArea > self.screenH else ySrc + constArea

        for i in range(xStart, xEnd):
            for j in range(yStart, yEnd):
                pixel = self.backgroundMask.get_at((i,j))
                if pixel == (0,0,0,255):
                    self.pixels[i][j] = 0
                else:
                    self.pixels[i][j] = 1

    def getPixels(self):
        return self.pixels

    def initBackground(self):
        self.backgroundSky = pygame.transform.scale(pygame.image.load(self.backgroundSkyImgPath).convert(), (self.screenW, self.screenH))
        self.backgroundGround = pygame.transform.scale(pygame.image.load(self.backgroundGroundImgPath).convert_alpha(), (self.screenW, self.screenH))
        self.generatePixel()

    def printBackground(self, screen):
        screen.blit(self.backgroundSky, (0, 0))
        screen.blit(self.backgroundGround, (0, 0))

    def destroyCircleArea(self, xSrc, ySrc, constArea):
        pygame.draw.circle(self.backgroundGround, (0, 0, 0, 0), (xSrc, ySrc), constArea)
        pygame.draw.circle(self.backgroundMask, (0, 0, 0, 255), (xSrc, ySrc), constArea)
        self.fastRegeneratePixel(xSrc, ySrc, constArea)

    def destroyLine(self, xSrc, ySrc, constArea):
        pygame.draw.rect(self.backgroundGround, (0, 0, 0, 0), pygame.Rect(xSrc, ySrc, constArea, constArea))
        pygame.draw.rect(self.backgroundMask, (0, 0, 0, 255), pygame.Rect(xSrc, ySrc, constArea, constArea))
        self.fastRegeneratePixel(xSrc, ySrc, constArea)

    def generateWind(self):
        random.seed()
        xWind = random.randint(-10, 10)
        yWind = random.randint(-5, 5)
        self.wind = (xWind, yWind)

     def getWind(self):
         return self.wind