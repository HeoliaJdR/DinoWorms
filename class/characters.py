import pygame
from pygame.locals import *
import constants
from Class import spritesheet


class Characters:
    def __init__(self, hp):
        self.hp = hp


def displayDinosaurs(screen):
    """
    dino = pygame.image.load(sprites.Sprites.baseSprite).convert_alpha()
    screen.blit(dino, ((constants.SCREEN_WIDTH - dino.get_rect().size[0]), (constants.SCREEN_HEIGHT - dino.get_rect().size[1])))
    85x77
    """
    sprites = spritesheet.spritesheet("Imgs/dino_spritesheet_1.png")
    image = sprites.image_at((0, 0, 85, 77))
    images = []



