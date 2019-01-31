import pygame
from pygame.locals import *
import constants
from Class import sprites


class Characters:
    def __init__(self, hp):
        self.hp = hp
        self.x = 1410
        self.y = 350
        self.posture = 0
        self.spriteSheet = "Imgs/dino_spritesheet_1.png"

    def initCharacter(self):
       self.player = pygame.image.load(self.spriteSheet).convert_alpha()

    def displayCharacter(self, screen):
        screen.blit(self.player, (self.x, self.y), sprites.Sprites.standingSprites[self.posture])



