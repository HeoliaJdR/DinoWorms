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
        self.trajectory=[]
        self.drawTrajectories=False
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.inDisplay = True
        self.verifyCollision = False

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

    def redrawWindow(self, win):
        if not self.shoot:
            pygame.draw.line(win, (0, 0, 0), self.line[0], self.line[1])
            pygame.draw.rect(win, (0, 0, 0), (self.golfBall.x - 50, self.golfBall.y + 50, 100, 10), 1)
            pygame.draw.rect(win,(255,0,0),(self.golfBall.x - 50, self.golfBall.y + 50, self.power,10),0)

        for point in self.trajectory:
            pygame.draw.rect(win, (0, 0, 0), (point[0], point[1], 3, 3), 0)


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
        if self.shoot:
            screen.blit(self.img,(self.golfBall.x,self.golfBall.y))

    def getNormal(self,area, range):
        if self.touchingPoint[0] - range < 0: return constants.RIGHT
        elif self.touchingPoint[0] + range > len(area)-1: return  constants.LEFT
        elif self.touchingPoint[1] - range < 0: return constants.TOP
        elif self.touchingPoint[1] + range > len(area)-1: return constants.BOT

        points = (#area[int(self.touchingPoint[0] - (self.golfBall.radius - 1)/2)][int(self.touchingPoint[1] - (self.golfBall.radius - 1)/2)],
                  area[int(self.touchingPoint[0] - range)][int(self.touchingPoint[1] - range)],
                  #area[self.touchingPoint[0]-1][self.touchingPoint[1]],
                  area[int(self.touchingPoint[0])][int(self.touchingPoint[1] - range)],
                  area[int(self.touchingPoint[0] + range)][int(self.touchingPoint[1] - range)],
                  area[int(self.touchingPoint[0] - range)][int(self.touchingPoint[1])],
                  area[int(self.touchingPoint[0] + range)][int(self.touchingPoint[1])],
                  area[int(self.touchingPoint[0] - range)][int(self.touchingPoint[1] + range)],
                  area[int(self.touchingPoint[0])][int(self.touchingPoint[1] + range)],
                  area[int(self.touchingPoint[0] + range)][int(self.touchingPoint[1] + range)])

        if points[1] == 0 and ((points[3] == 1 and points[4] == 1) or (points[5] == 0 and points[6] == 1 and points[7] == 0) or (points[5] == 1 and points[6] == 1 and points[7] == 1)):
            return constants.TOP
        if points[6] == 0 and ((points[3] == 1 and points[4] == 1) or (points[0] == 0 and points[1] == 1 and points[2] == 0) or (points[0] == 1 and points[1] == 1 and points[2] == 1)):
            return constants.BOT
        if points[3] == 0 and ((points[1] == 1 and points[6] == 1) or (points[2] == 0 and points[4] == 1 and points[7] == 0) or (points[2] == 1 and points[4] == 1 and points[7] == 1)):
            return constants.LEFT
        if points[4] == 0 and ((points[1] == 1 and points[6] == 1) or (points[0] == 0 and points[3] == 1 and points[5] == 0) or (points[0] == 1 and points[3] == 1 and points[5] == 1)):
            return constants.RIGHT
        if points[0] == 0 and ((points[2] == 1 and points[5] == 1) or (points[4] == 1 and points[6] == 1) or (points[5] == 0 and points[6] == 1 and points[7] == 1) or (points[5] == 0 and points[6] == 0 and points[7] == 1 and points[4] == 0 and points[2] == 0) or (points[2] == 0 and points[4] == 1 and points[7] == 1)):
            return constants.TOPLEFT
        if points[2] == 0 and ((points[0] == 1 and points[7] == 1) or (points[3] == 1 and points[6] == 1) or (points[5] == 1 and points[6] == 1 and points[7] == 0) or (points[5] == 1 and points[6] == 0 and points[7] == 0 and points[0] == 0 and points[3] == 0) or (points[0] == 0 and points[3] == 1 and points[5] == 1)):
            return constants.TOPRIGHT
        if points[5] == 0 and ((points[0] == 1 and points[7] == 1) or (points[1] == 1 and points[4] == 1) or (points[0] == 0 and points[1] == 1 and points[2] == 1) or (points[2] == 1 and points[0] == 0 and points[1] == 0 and points[4] == 0 and points[7] == 0) or (points[2] == 1 and points[4] == 1 and points[7] == 0)):
            return constants.BOTLEFT
        if points[7] == 0 and ((points[2] == 1 and points[5] == 1) or (points[1] == 1 and points[3] == 1) or (points[0] == 1 and points[1] == 1 and points[2] == 0) or (points[0] == 0 and points[1] == 0 and points[2] == 1 and points[3] == 0 and points[5] == 0) or (points[0] == 1 and points[3] == 1 and points[5] == 0)):
            return constants.BOTRIGHT

        return self.getNormal(area,range+1)

    def resetBall(self):
        self.shoot = False
        self.power = 0
        self.time = 0
        self.totaltime = pygame.time.get_ticks()

    def changeProjectile(self, projType):
        if not self.shoot:
            self.type = projType

    def enableTrajectory(self):
        self.drawTrajectories = not self.drawTrajectories

    def cleanTrajectory(self):
        self.trajectory = []

    def launchBall(self, win, area,newWorld, players):
        if self.drawTrajectories:
            self.trajectory.append((int(self.golfBall.x+self.golfBall.radius/2), int(self.golfBall.y+self.golfBall.radius/2)))

        if self.launchAnim:
            self.launchAnim = self.anim.playAnim(win, self.origAnim)
            return self.launchAnim

        if self.verifyCollision:
            self.verifyCollision = False
            self.collisionWithPlayer(players)

        if self.shoot:
            for i in range(self.golfBall.x+1,self.golfBall.x + self.golfBall.radius-1):
                for j in range(int(self.golfBall.y), int(self.golfBall.y + self.golfBall.radius-1)):
                    if i <= 0 or j <= 0 or i >= newWorld.screenW or j >= newWorld.screenH:
                        self.inDisplay = False
                        break
                    else: self.inDisplay = True
                    if area[i][j]==1 :
                        self.go = False
                        self.touchingPoint = (i,j)
                        break
            self.go = False if self.go == False else not self.collisionWithPlayer(players, True)
            if self.go:
                self.time += 0.15
                po = ball.ball.ballPath(self.x, self.y, self.power, self.angle, self.time, newWorld.getWind())
                self.golfBall.x = po[0]
                self.golfBall.y = po[1]
            else:
                if self.type == 1:
                    #starting_x = self.x
                    starting_y= self.y
                    additionnal_power = self.golfBall.y-starting_y
                    normale=self.getNormal(area,1)
                    #print(normale)
                    self.go = True
                    if normale == constants.LEFT or normale == constants.TOPLEFT or normale == constants.BOTLEFT:
                        self.x = self.golfBall.x - 1
                    elif normale == constants.RIGHT or normale == constants.TOPRIGHT or normale == constants.BOTRIGHT or normale == constants.TOP or normale == constants.BOT:
                        self.x = self.golfBall.x + 1
                    if normale == constants.TOP or normale == constants.TOPLEFT or normale == constants.TOPRIGHT or normale == constants.LEFT or normale == constants.RIGHT:
                        self.y = self.golfBall.y-1
                    elif normale == constants.BOT or normale == constants.BOTLEFT or normale == constants.BOTRIGHT:
                        self.y = self.golfBall.y+1
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
                elif self.type == 2:
                    self.resetBall()
                    self.launchAnim = True
                    self.verifyCollision = True
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
            if self.type == 1 and pygame.time.get_ticks() - self.totaltime >= 3000:
                self.resetBall()
                self.launchAnim = True
                self.verifyCollision = True
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
        if self.type == 1 and pygame.time.get_ticks() - self.totaltime <= 1000 and self.shoot:
            label = self.font.render("3", 1, (255, 0, 0))
            win.blit(label, (self.golfBall.x - 10, self.golfBall.y - 10))
        elif self.type == 1 and pygame.time.get_ticks() - self.totaltime <= 2000 and self.shoot:
            label = self.font.render("2", 1, (255, 0, 0))
            win.blit(label, (self.golfBall.x - 10, self.golfBall.y - 10))
        elif self.type == 1 and pygame.time.get_ticks() - self.totaltime <= 3000 and self.shoot:
            label = self.font.render("1", 1, (255, 0, 0))
            win.blit(label, (self.golfBall.x - 10, self.golfBall.y - 10))

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

        if self.inDisplay:
            self.printProjectile(win)
        elif self.shoot and self.type == 2 and pygame.time.get_ticks() - self.totaltime >= 3000:
            self.resetBall()
            return False

        return True

    def collisionWithPlayer(self, players, verifyExplosion = False):
        areaCircle = math.pow(constants.MEDIUM_CIRCLE, 2)
        isCollision = False;
        rectProj = pygame.Rect(self.golfBall.x, self.golfBall.y, self.golfBall.radius, self.golfBall.radius)

        for player in players:
            if verifyExplosion:
                if rectProj.colliderect(player.allRect):
                    isCollision = True
            else:
                if (math.pow((player.allRect.x - self.origAnim[0]), 2) + math.pow((player.allRect.y - self.origAnim[1]), 2) <  areaCircle or
                    math.pow((player.allRect.x  - self.origAnim[0]), 2) + math.pow((player.allRect.y + player.allRect.h - self.origAnim[1]), 2) < areaCircle or
                    math.pow((player.allRect.x + player.allRect.w  - self.origAnim[0]), 2) + math.pow((player.allRect.y - self.origAnim[1]), 2) < areaCircle or
                    math.pow((player.allRect.x + player.allRect.w  - self.origAnim[0]), 2) + math.pow((player.allRect.y + player.allRect.h - self.origAnim[1]), 2) < areaCircle
                ):
                    isCollision = True
                    player.loseHp(50)

        return isCollision
