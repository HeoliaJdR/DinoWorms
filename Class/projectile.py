import pygame
import math
import constants

from Class import ball
from Class import animation

class projectile(object):
    def __init__(self, projectileType):
        self.run = True
        self.time = 0
        self.power = 0
        self.angle = 0
        self.shoot = False
        self.loading = 0
        self.golfBall = ball.ball(300, 494, 20, (255, 255, 255))
        self.type = projectileType
        self.projectileImgPath="Imgs/W4_Grenade.png"
        self.touchingPoint=(0,0)
        self.totaltime = 0
        self.line = []
        self.loadup = True

        """ Ajout des animations"""
        self.launchAnim = False
        self.anim = animation.Animation("Imgs/explosion-sprite-sheet-png-3.png", (130, 130), (0, 0), 25, 5, 5, 5, False)
        self.anim.extraParameter(scale=(130 + constants.MEDIUM_CIRCLE, 130 + constants.MEDIUM_CIRCLE))
        self.origAnim = (0, 0)

    def initProjectile(self):
        if self.type == 1:
           self.projectileImgPath = "Imgs/W4_Grenade.png"
        if self.type == 2:
           self.projectileImgPath = "Imgs/rocket.png"

        self.img = pygame.transform.scale(pygame.image.load(self.projectileImgPath).convert_alpha(), (30, 30))

    def redrawWindow(self,win):
        #win.fill((64, 64, 64))
        if not self.shoot:
            self.golfBall.x = 1000
            self.golfBall.y = 600
        if not self.shoot:
            pygame.draw.line(win, (0, 0, 0), self.line[0], self.line[1])
            pygame.draw.rect(win, (0, 0, 0), (0, 0, 100, 10), 1)
            pygame.draw.rect(win,(255,0,0),(0,0,self.power,10),0)


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
            self.totaltime = pygame.time.get_ticks()
            self.go = True

    def printProjectile(self,screen):
        screen.blit(self.img,(self.golfBall.x,self.golfBall.y))

    def getNormal(self,area):
        """point1 = (0, 0)
        point2 = (0, 0)
        for i in range(self.golfBall.x - (self.golfBall.radius - 1)/2,self.golfBall.x + (self.golfBall.radius - 1)/2):
            for j in range(self.golfBall.y - (self.golfBall.radius - 1)/2,self.golfBall.y + (self.golfBall.radius - 1)/2):
                if area[i][j] == 1:
                    point1 = (i, j)
                    break;
        for i in range(self.golfBall.x - (self.golfBall.radius - 1)/2,self.golfBall.x + (self.golfBall.radius - 1)/2):
            for j in range(self.golfBall.y - (self.golfBall.radius - 1)/2,self.golfBall.y + (self.golfBall.radius - 1)/2):
                if area[j][i] == 1:
                    point2 = (j, i)
                    break;
        if point1 == point2:"""
        points = (#area[int(self.touchingPoint[0] - (self.golfBall.radius - 1)/2)][int(self.touchingPoint[1] - (self.golfBall.radius - 1)/2)],
                  area[int(self.touchingPoint[0] - 5)][int(self.touchingPoint[1] - 5)],
                  #area[self.touchingPoint[0]-1][self.touchingPoint[1]],
                  area[int(self.touchingPoint[0])][int(self.touchingPoint[1] - 5)],
                  area[int(self.touchingPoint[0] + 5)][int(self.touchingPoint[1] - 5)],
                  area[int(self.touchingPoint[0] - 5)][int(self.touchingPoint[1])],
                  area[int(self.touchingPoint[0] + 5)][int(self.touchingPoint[1])],
                  area[int(self.touchingPoint[0] - 5)][int(self.touchingPoint[1] + 5)],
                  area[int(self.touchingPoint[0])][int(self.touchingPoint[1] + 5)],
                  area[int(self.touchingPoint[0] + 5)][int(self.touchingPoint[1] + 5)])
        """point (0,1,2
                  3,  4
                  5,6,7)"""
        if (points[0] == 0 and points[1] == 0 and points[2] == 0) and ((points[3] == 1 and points[4] == 1) or (points[5] == 0 and points[6] == 1 and points[7] == 0) or (points[5] == 1 and points[6] == 1 and points[7] == 1)):
            return constants.TOP
        if (points[5] == 0 and points[6] == 0 and points[7] == 0) and ((points[3] == 1 and points[4] == 1) or (points[0] == 0 and points[1] == 1 and points[2] == 0) or (points[0] == 1 and points[1] == 1 and points[2] == 1)):
            return constants.BOT
        if (points[0] == 0 and points[3] == 0 and points[5] == 0) and ((points[1] == 1 and points[6] == 1) or (points[2] == 0 and points[4] == 1 and points[7] == 0) or (points[2] == 1 and points[4] == 1 and points[7] == 1)):
            return constants.LEFT
        if (points[2] == 0 and points[4] == 0 and points[7] == 0) and ((points[1] == 1 and points[6] == 1) or (points[0] == 0 and points[3] == 1 and points[5] == 0) or (points[0] == 1 and points[3] == 1 and points[5] == 1)):
            return constants.RIGHT
        if (points[0] == 0 and points[1] == 0 and points[3] == 0) and ((points[2] == 1 and points[5] == 1) or (points[4] == 1 and points[6] == 1) or (points[5] == 0 and points[6] == 1 and points[7] == 1) or (points[5] == 0 and points[6] == 0 and points[7] == 1 and points[4] == 0 and points[2] == 0)):
            return constants.TOPLEFT
        if (points[1] == 0 and points[2] == 0 and points[4] == 0) and ((points[0] == 1 and points[7] == 1) or (points[3] == 1 and points[6] == 1) or (points[5] == 1 and points[6] == 1 and points[7] == 0) or (points[5] == 1 and points[6] == 0 and points[7] == 0 and points[0] == 0 and points[3] == 0)):
            return constants.TOPRIGHT
        if (points[3] == 0 and points[5] == 0 and points[6] == 0) and ((points[0] == 1 and points[7] == 1) or (points[1] == 1 and points[4] == 1) or (points[0] == 0 and points[1] == 1 and points[2] == 1) or (points[2] == 1 and points[0] == 0 and points[1] == 0 and points[4] == 0 and points[7] == 0)):
            return constants.BOTLEFT
        if (points[4] == 0 and points[6] == 0 and points[7] == 0) and ((points[2] == 1 and points[5] == 1) or (points[1] == 1 and points[3] == 1) or (points[0] == 1 and points[1] == 1 and points[2] == 0) or (points[0] == 0 and points[1] == 0 and points[2] == 1 and points[3] == 0 and points[5] == 0)):
            return constants.BOTRIGHT
        """if (points[6] == 1): return constants.TOP
        if (points[1] == 1): return constants.BOT
        if (points[3] == 1): return constants.RIGHT
        if (points[4] == 1): return constants.LEFT

        return constants.TOP"""

        #print(points)
        #print(area[self.touchingPoint[0]][self.touchingPoint[1]])
        #input()

    def resetBall(self):
        self.shoot = False
        self.power = 0
        self.time = 0
        self.totaltime = 0

    def changeProjectile(self, projType):
        self.type = projType



    def launchBall(self, win, area,newWorld):
        """run = True
        time = 0
        power = 0
        angle = 0
        shoot = False
        loading = 0"""


        if self.launchAnim:
            self.launchAnim = self.anim.playAnim(win, self.origAnim)
            return

        if self.shoot:
            #if self.golfBall.y < 500 - self.golfBall.radius:
            k = 0


            for i in range(self.golfBall.x+1,self.golfBall.x + self.golfBall.radius-1):
                for j in range(self.golfBall.y,self.golfBall.y + self.golfBall.radius-1):
                    if i <= 0 or j <= 0 or i >= newWorld.screenW or j >= newWorld.screenH:
                        self.shoot = False
                        self.power = 0
                        self.time = 0
                        self.totaltime = 0
                        return 0
                    if area[i][j]==1 :
                        self.go = False
                        self.touchingPoint = (i,j)
                        break
            #if area[self.golfBall.x + self.golfBall.radius][self.golfBall.y + self.golfBall.radius*2] == 0 and area[self.golfBall.x][self.golfBall.y + self.golfBall.radius*2] == 0 and area[self.golfBall.x + self.golfBall.radius][self.golfBall.y] == 0 and area[self.golfBall.x][self.golfBall.y] == 0:
            if self.go:
                self.time += 0.15
                po = ball.ball.ballPath(self.x, self.y, self.power, self.angle, self.time, newWorld.getWind())
                self.golfBall.x = po[0]
                self.golfBall.y = po[1]
            else:
                if self.type == 1:
                    """newWorld.destroyCircleArea(self.golfBall.x+ int(self.golfBall.radius/2),self.golfBall.y+ int(self.golfBall.radius/2),constants.MEDIUM_CIRCLE)
                    self.shoot=False
                    self.power = 0
                    self.time = 0"""
                    """shoot = False
                    power = 0
                    time = 0
                    self.golfBall.y = 494"""
                    #starting_x = self.x
                    starting_y= self.y
                    additionnal_power = self.golfBall.y-starting_y
                    normale=self.getNormal(area)
                    #print(normale)
                    self.go = True
                    if normale == constants.LEFT or normale == constants.TOPLEFT or normale == constants.BOTLEFT:
                        self.x = self.golfBall.x - 1
                    elif normale == constants.RIGHT or normale == constants.TOPRIGHT or normale == constants.BOTRIGHT:
                        self.x = self.golfBall.x + 1
                    self.x = self.golfBall.x
                    if normale == constants.TOP or normale == constants.TOPLEFT or normale == constants.TOPRIGHT:
                        self.y = self.golfBall.y-1
                    elif normale == constants.BOT or normale == constants.BOTLEFT or normale == constants.BOTRIGHT:
                        self.y = self.golfBall.y+1
                    if not normale:
                        if area[self.golfBall.x-1][self.golfBall.y] != 1: self.x = self.golfBall.x-1
                        elif area[self.golfBall.x+1][self.golfBall.y] != 1: self.x = self.golfBall.x + 1
                        else: self.x = self.golfBall.x
                        if area[self.golfBall.x][self.golfBall.y-1] != 1: self.y = self.golfBall.y-1
                        elif area[self.golfBall.x][self.golfBall.y + 1] != 1: self.y = self.golfBall.y + 1
                        else: self.y = self.golfBall.y
                    if normale:
                        if self.angle<math.pi/2:
                            if normale == constants.TOP: self.angle = self.angle*0.9
                            if normale == constants.BOT: self.angle = (self.angle +3*math.pi/2)*0.9
                            if normale == constants.LEFT: self.angle = (self.angle + math.pi/2)*1.1
                            if normale == constants.TOPLEFT: self.angle = (self.angle + math.pi / 2) * 1.05
                            if normale == constants.TOPRIGHT: self.angle = self.angle *0.8
                            if normale == constants.BOTLEFT: self.angle = (self.angle + 3*math.pi/2)*0.8
                            if normale == constants.BOTRIGHT: self.angle = (self.angle + 3 * math.pi / 2) * 1.1
                        elif self.angle<math.pi:
                            if normale == constants.TOP: self.angle = self.angle * 1.1
                            if normale == constants.BOT: self.angle = (self.angle + math.pi/2)*1.1
                            if normale == constants.RIGHT: self.angle = (self.angle - math.pi/2)*0.9
                            if normale == constants.TOPLEFT: self.angle = self.angle = self.angle * 1.2
                            if normale == constants.TOPRIGHT: self.angle = (self.angle - math.pi/2)*0.8
                            if normale == constants.BOTLEFT: self.angle = (self.angle + math.pi/4)*1.2
                            if normale == constants.BOTRIGHT: self.angle = (self.angle + math.pi/2)*0.9
                        elif self.angle<3*math.pi/2:
                            if normale == constants.TOP: self.angle = (self.angle - math.pi/2) * 1.1
                            if normale == constants.RIGHT: self.angle = (self.angle + math.pi / 2) * 0.9
                            if normale == constants.TOPLEFT: self.angle = (self.angle - math.pi / 2) * 1.2
                            if normale == constants.TOPRIGHT: self.angle = (self.angle - math.pi) * 1.1
                        else:
                            if normale == constants.TOP: self.angle = (self.angle-3*math.pi/2)*0.9
                            if normale == constants.LEFT: self.angle = (self.angle - math.pi / 2) * 1.1
                            if normale == constants.TOPLEFT: self.angle = (self.angle - math.pi) * 1.1
                            if normale == constants.TOPRIGHT: self.angle = (self.angle-3*math.pi/2)*0.8

                    if self.time>1: self.power = self.power / (self.time/30+1)+additionnal_power/10
                    else: self.power = self.power * 0.8
                    self.time = 0
                    po = ball.ball.ballPath(self.x, self.y, self.power, self.angle, self.time, newWorld.getWind())
                    self.golfBall.x = po[0]
                    self.golfBall.y = po[1]
                    # pos = pygame.mouse.get_pos()
                    # shoot = True
                    # angle = findAngle(pos)
                    # if abs(po[2]) < 0.1 and abs(po[3]) < 0.1:
                    if pygame.time.get_ticks() - self.totaltime >= 3000:
                        self.resetBall()
                        self.launchAnim = True
                        self.anim.extraParameter(function=(
                            newWorld.destroyCircleArea,
                            3,
                            [self.golfBall.x + self.golfBall.radius / 2, self.golfBall.y + self.golfBall.radius / 2,
                             constants.MEDIUM_CIRCLE]
                        ))
                        self.origAnim = (
                            self.golfBall.x + self.golfBall.radius / 2,
                            self.golfBall.y + self.golfBall.radius / 2
                        )
                elif self.type == 2:
                    self.resetBall()
                    self.launchAnim = True
                    self.anim.extraParameter(function=(
                        newWorld.destroyCircleArea,
                        3,
                        [self.golfBall.x + self.golfBall.radius / 2, self.golfBall.y + self.golfBall.radius / 2,
                         constants.MEDIUM_CIRCLE]
                    ))
                    self.origAnim = (
                        self.golfBall.x + self.golfBall.radius / 2,
                        self.golfBall.y + self.golfBall.radius / 2
                    )

        self.line = [(int(self.golfBall.x + self.golfBall.radius), int(self.golfBall.y + self.golfBall.radius)),pygame.mouse.get_pos()]
        self.redrawWindow(win)

        if self.loading == 1:
            if self.loadup == True:
                if self.power < 100:
                    self.power+=1
                else:
                    self.loadup = False
            else:
                if self.power > 0:
                    self.power-=1
                else:
                    self.loadup = True

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
