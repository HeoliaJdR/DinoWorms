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

        self.timer = 0
        self.initPlayers()

        self.activePlayer = 0

    def initPlayers(self):
        self.players = []
        xOrig = 200
        yOrig = 350
        for i in range (self.nbPlayers):
            self.players.append(characters.Characters(100, i%2, xOrig, yOrig, True, "Joueur_" + str(i+1)))
            if i == 0:
                self.players[i].isActivePlayer = True
            #self.players[i].updateYPos(self.world, self.world.getPixels())
            xOrig += 200

    def printElements(self, screen):
        area = self.world.getPixels()
        endOfGame = False

        self.world.printBackground(screen)
        if self.world.needChangeArrow:
            self.world.animWindArrow()

        needEndOfTurn = not self.proj.launchBall(screen, area, self.world, self.players)

        for player in self.players:
            player.moveCharacter(self.world, area)
            needDestroy = not player.displayCharacter(screen, area, self.world)
            player.updateYPos(self.world, area)

            if needDestroy:
                endOfGame = self.destroyPlayer(player)

            if player.isActivePlayer and not self.proj.shoot:
                self.proj.golfBall.changeOrig((player.x, player.y - player.allRect.h))

        if needEndOfTurn:
            self.endOfTurn()

        return endOfGame

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
            if event.key == pygame.K_SPACE:
                if self.players[self.activePlayer].isJumping == False:
                    self.players[self.activePlayer].isJumping = True
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

    def destroyPlayer(self, player):
        isActivePlayer = player.isActivePlayer
        self.players.remove(player)
        self.nbPlayers -= 1
        self.activePlayer = 0 if self.activePlayer >= self.nbPlayers else self.activePlayer
        if isActivePlayer:
            self.players[self.activePlayer].isActivePlayer = True

        return self.verifyTeamIntegrity()

    def verifyTeamIntegrity(self):
        team1 = False
        team2 = False

        for player in self.players:
            if player.team == 0:
                team1 = True
            if player.team == 1:
                team2 = True

        if not team1:
            return constants.VICTORY_TEAM_2
        if not team2:
            return constants.VICTORY_TEAM_1

        return constants.CONTINUE_GAME

    def endOfTurn(self):
        self.world.generateWind()
        self.timer = 0

        if self.players:
            self.players[self.activePlayer].animConstant = constants.IDLE
            self.players[self.activePlayer].wantsToWalkLeft = False
            self.players[self.activePlayer].wantsToWalkRight = False
            self.players[self.activePlayer].isActivePlayer = False
            self.activePlayer += 1
            self.activePlayer = 0 if self.activePlayer >= self.nbPlayers else self.activePlayer

            current_player = self.players[self.activePlayer]
            current_player.isActivePlayer = True

            self.proj.golfBall.changeOrig((current_player.x, current_player.y - current_player.allRect.h))