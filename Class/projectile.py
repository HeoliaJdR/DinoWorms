import pygame
import math
import constants
from Class import ball

class projectile(object):
    def __init__(self):
        self.run = True
        self.time = 0
        self.power = 0
        self.angle = 0
        self.shoot = False
        self.loading = 0
        self.golfBall = ball.ball(300, 494, 5, (255, 255, 255))
        self.grenadepath="Imgs/W4_Grenade.png"

    def initProjectile(self):
        self.img = pygame.transform.scale(pygame.image.load(self.grenadepath).convert_alpha(),(30,30))

    def redrawWindow(self,win):
        #win.fill((64, 64, 64))
        if not self.shoot:
            self.golfBall.x = 500
            self.golfBall.y = 495
        #self.golfBall.draw(win)
        #pygame.draw.line(win, (0, 0, 0), line[0], line[1])
        #pygame.display.update()

    def findAngle(self,pos):
        sX = self.golfBall.x
        sY = self.golfBall.y
        try:
            self.angle = math.atan((sY - pos[1]) / (sX - pos[0]))
        except:
            self.angle = math.pi / 2

        if pos[1] < sY and pos[0] > sX:
            self.angle = abs(self.angle)
        elif pos[1] < sY and pos[0] < sX:
            self.angle = math.pi - self.angle
        elif pos[1] > sY and pos[0] < sX:
            self.angle = math.pi + abs(self.angle)
        elif pos[1] > sY and pos[0] > sX:
            self.angle = (math.pi * 2) - self.angle
        """print(self.angle)
        print(pos[0],pos[1])"""
        return self.angle

    def enableLoading(self):
        if not self.shoot:
            self.loading = 1
    def releaseProjectile(self):
        if not self.shoot:
            self.x = self.golfBall.x
            self.y = self.golfBall.y
            pos = pygame.mouse.get_pos()
            self.shoot = True
            self.angle = self.findAngle(pos)
            self.loading = 0

    def printProjectile(self,screen):
        screen.blit(self.img,(self.golfBall.x,self.golfBall.y))

    def launchBall(self,win, area):


        """run = True
        time = 0
        power = 0
        angle = 0
        shoot = False
        loading = 0"""

        if self.shoot:
            #if self.golfBall.y < 500 - self.golfBall.radius:
            if area[self.golfBall.x + self.golfBall.radius][self.golfBall.y + self.golfBall.radius*2] == 0:
                self.time += 0.1
                po = ball.ball.ballPath(self.x, self.y, self.power, self.angle, self.time)
                self.golfBall.x = po[0]
                self.golfBall.y = po[1]
            else:
                """shoot = False
                power = 0
                time = 0
                self.golfBall.y = 494"""
                self.x = self.golfBall.x
                self.y = self.golfBall.y-1
                if self.angle<math.pi/2:
                    self.angle = self.angle*0.9
                elif self.angle<math.pi:
                    self.angle = self.angle * 1.1
                elif self.angle<3*math.pi/2:
                    self.angle = self.angle - math.pi/4
                else: self.angle = self.angle*0.9-3*math.pi/2

                self.power = self.power * 0.8
                self.time = 0
                po = ball.ball.ballPath(self.x, self.y, self.power, self.angle, self.time)
                self.golfBall.x = po[0]
                self.golfBall.y = po[1]

                #pos = pygame.mouse.get_pos()
                #shoot = True
                #angle = findAngle(pos)
            if abs(po[2]) < 0.1 and abs(po[3]) < 0.1:
                self.shoot = False
                self.power = 0
                self.time = 0
                self.golfBall.y = 494

        line = [(self.golfBall.x, self.golfBall.y), pygame.mouse.get_pos()]
        self.redrawWindow(win)

        if self.loading == 1:
            self.power+=0.4

        """for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.shoot:
                    self.loading = 1

            if event.type == pygame.MOUSEBUTTONUP:
                if not self.shoot:
                    self.x = self.golfBall.x
                    self.y = self.golfBall.y
                    pos = pygame.mouse.get_pos()
                    self.shoot = True
                    self.angle = self.findAngle(pos)
                    self.loading = 0
                    #print(self.power)"""
        self.printProjectile(win)
