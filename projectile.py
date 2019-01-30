import pygame
import math
from Class import ball

wScreen = 1200
hScreen = 500

win = pygame.display.set_mode((wScreen, hScreen))
pygame.display.set_caption('Projectile Motion')

def redrawWindow():
    win.fill((64, 64, 64))
    if not shoot:
        golfBall.x = 10
        golfBall.y = 494
    golfBall.draw(win)
    #pygame.draw.line(win, (0, 0, 0), line[0], line[1])
    pygame.display.update()



def findAngle(pos):
    sX = golfBall.x
    sY = golfBall.y
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


golfBall = ball.ball(300, 494, 5, (255, 255, 255))

run = True
time = 0
power = 0
angle = 0
shoot = False
loading = 0

while run:

    if shoot:
        if golfBall.y < 500 - golfBall.radius:
            time += 0.01
            po = ball.ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]
        else:
            """shoot = False
            power = 0
            time = 0
            golfBall.y = 494"""
            x = golfBall.x
            y = golfBall.y-1
            angle = angle*0.9
            power = power * 0.8
            time = 0
            po = ball.ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]

            #pos = pygame.mouse.get_pos()
            #shoot = True
            #angle = findAngle(pos)
        if po[2] < 0.1 and po[3] < 0.1:
            shoot = False
            power = 0
            time = 0
            golfBall.y = 494

    line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    redrawWindow()

    if loading == 1:
        power+=0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                loading = 1

        if event.type == pygame.MOUSEBUTTONUP:
            if not shoot:
                x = golfBall.x
                y = golfBall.y
                pos = pygame.mouse.get_pos()
                shoot = True
                angle = findAngle(pos)
                loading = 0
pygame.quit()