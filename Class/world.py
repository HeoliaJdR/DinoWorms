import pygame
from pygame import gfxdraw


class World:
    def __init__(self, screenHeight, screenWidth):
        self.backgroundSkyImgPath = "Imgs/backgroundSky.jpg"
        self.backgroundGroundImgPath = "Imgs/backgroundGround.png"
        self.backgroundMaskImgPath = "Imgs/backgroundMask.jpg"
        self.screenH = screenHeight
        self.screenW = screenWidth
        self.pixels = [[1] * screenHeight for i in range(screenWidth)]

    def generatePixelDico(self):
        backgroundMask = pygame.transform.scale(pygame.image.load(self.backgroundMaskImgPath).convert(), (self.screenW, self.screenH))
        for i in range(self.screenW):
            for j in range(self.screenH):
                pixel = backgroundMask.get_at((i,j))
                if pixel == (0,0,0,255):
                    self.pixels[i][j] == 0
                else:
                    self.pixels[i][j] == 1

    def getPixels(self):
        return self.pixels

    def initBackground(self):
        self.backgroundSky = pygame.transform.scale(pygame.image.load(self.backgroundSkyImgPath).convert(), (self.screenW, self.screenH))
        self.backgroundGround = pygame.transform.scale(pygame.image.load(self.backgroundGroundImgPath).convert_alpha(), (self.screenW, self.screenH))
        self.generatePixelDico()

    def printBackground(self, screen):
        screen.blit(self.backgroundSky, (0, 0))
        screen.blit(self.backgroundGround, (0, 0))

    def destroyArea(self, xSrc, ySrc):
        stockX = xSrc
        while ySrc < self.screenH:
            while xSrc < stockX + 10:
                self.backgroundGround.set_at((xSrc, ySrc), (0,0,0,0))
                xSrc += 1
            xSrc = stockX
            ySrc += 1