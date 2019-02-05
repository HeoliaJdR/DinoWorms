import pygame
import constants
from Class import world
from Class import characters
from Class import projectile

class Game:
    def __init__(self, nbPlayers, screenSize):
        self.nbPlayers = nbPlayers

        self.world = world.World(screenSize[1], screenSize[0])
        self.world.initBackground()
        self.world.generateWind()

        self.proj = projectile.projectile(2)
        self.proj.initProjectile()

        self.activePlayer = 0

        self.timer = 0
        self.initPlayers()

    def initPlayers(self):
        self.players = [None] * self.nbPlayers
        xOrig = 200
        yOrig = 350
        for i in range (self.nbPlayers):
            self.players[i] = characters.Characters(100, 0, xOrig, yOrig, True, "Joueur_" + str(i+1))
            self.players[i].updateYPos(self.world, self.world.getPixels())
            xOrig += 200

    def printElements(self, screen):
        area = self.world.getPixels()

        self.world.printBackground(screen)
        if self.world.needChangeArrow:
            self.world.animWindArrow()

        needEndOfTurn = not self.proj.launchBall(screen, area, self.world)

        for i in range(self.nbPlayers):
            #print("Nom : " + self.players[i].name)
            player = self.players[i]
            player.moveCharacter(self.world, area)
            player.displayCharacter(screen, area, self.world)
            self.players[i].updateYPos(self.world, self.world.getPixels())

            if i == self.activePlayer and not self.proj.shoot:
                self.proj.golfBall.changeOrig((player.x, player.y))

        if needEndOfTurn:
            self.endOfTurn()

    def gameEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.proj.changeProjectile(1)
                self.proj.initProjectile()
            if event.key == pygame.K_2:
                self.proj.changeProjectile(2)
                self.proj.initProjectile()
            if event.key == pygame.K_9:
                self.proj.enableTrajectory()
            if event.key == pygame.K_0:
                self.proj.cleanTrajectory()
            if event.key == pygame.K_c:
                self.endOfTurn()

            if event.key == pygame.K_d:
                self.players[self.activePlayer].wantsToWalkRight = True
                self.players[self.activePlayer].animConstant = constants.WALK
            if event.key == pygame.K_a:
                self.players[self.activePlayer].wantsToWalkLeft = True
                self.players[self.activePlayer].animConstant = constants.WALK

            if event.key == pygame.K_BACKSPACE:
                self.players[self.activePlayer].displayBoxes = 1
            if event.key == pygame.K_TAB:
                self.players[self.activePlayer].displayBoxes = 0

        if event.type == pygame.KEYUP:
            self.players[self.activePlayer].wantsToWalkRight = False
            self.players[self.activePlayer].wantsToWalkLeft = False
            self.players[self.activePlayer].animConstant = constants.IDLE
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.proj.enableLoading()
        if event.type == pygame.MOUSEBUTTONUP:
            self.proj.releaseProjectile()

    def endOfTurn(self):
        self.world.generateWind()
        self.timer = 0
        self.players[self.activePlayer].animConstant = constants.IDLE
        self.players[self.activePlayer].wantsToWalkLeft = False
        self.players[self.activePlayer].wantsToWalkRight = False
        self.activePlayer += 1
        self.activePlayer = 0 if self.activePlayer >= self.nbPlayers else self.activePlayer

        player = self.players[self.activePlayer]

        self.proj.golfBall.changeOrig((player.x, player.y))