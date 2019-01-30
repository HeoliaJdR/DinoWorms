import pygame
import math

class ball(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)

    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        #print(power)
        angle = ang
        velx = math.cos(angle) * power #-22
        vely = math.sin(angle) * power #-17

        distX = velx * time #-22
        distY = (vely * time) + ((-9.8 * (time ** 2)) / 2) #-1.749

        newx = round(distX + startx)
        newy = round(starty - distY)

        return (int(newx), int(newy), velx*time, vely)