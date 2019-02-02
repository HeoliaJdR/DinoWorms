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
        self.spriteSheet = "Imgs/dinoGreen.png"

        """ Ajout des animations"""
        self.launchAnim = False
        self.anim = animation.Animation("Imgs/dinoGreen.png", (680, 630), (0, 0), 10, 3, 4, 60, self.loop)
        self.anim.extraParameter(scale=(100 + constants.MEDIUM_CIRCLE, 63 + constants.MEDIUM_CIRCLE))
        self.origAnim = (self.x, self.y)

    def initCharacter(self):
       self.player = pygame.transform.scale(pygame.image.load(self.spriteSheet).convert_alpha(), (300, 300))

    def displayCharacter(self, screen, area):
        if self.loop or self.firstLoop == 0:
            self.launchAnim = self.anim.playAnim(screen, self.origAnim)
            self.firstLoop = 1
        #print("Test \n" + str(area))

    def moveCharacter(self, screen, key):
        if key == pygame.K_d:
            if self.direction == 0:
                self.player = pygame.transform.flip(self.player, True, True)
                pygame.display.update()
                self.direction = 1
            self.x += 4
            self.origAnim = (self.x, self.y)
            print(self.x)
        if key == pygame.K_a:
            if self.direction == 1:
                self.player = pygame.transform.flip(self.player, True, True)
                pygame.display.update()
                self.direction = 0
            self.x -= 4
            self.origAnim = (self.x, self.y)
            print(self.x)
