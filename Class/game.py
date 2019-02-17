import pygame
import constants
from Class import world
from Class import characters
from Class import projectile

class Game:
    def __init__(self, nbPlayers, nbDinos, screenSize):
        self.nbPlayers = nbPlayers
        self.nbDinos = nbDinos * nbPlayers

        self.world = world.World(screenSize[1], screenSize[0])
        self.world.initBackground()
        self.world.generateWind()

        self.proj = projectile.projectile(2)
        self.proj.initProjectile()

        self.timer = 0
        self.initPlayers()

        self.activePlayer = 0
        self.teamLastTurn = 0

    def initPlayers(self):
        self.players = []
        xOrig = 50
        yOrig = 350
        for i in range (self.nbDinos):
            self.players.append(characters.Characters(100, i%self.nbPlayers, xOrig, yOrig, True, "Joueur_" + str(i+1)))
            if i == 0:
                self.players[i].isActivePlayer = True
            #self.players[i].updateYPos(self.world, self.world.getPixels())
            xOrig += 175

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
            player.jumpCharacter(self.world, area)

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
            if event.key == pygame.K_t:
                self.players[self.activePlayer].teleportCharacter()
            if event.key == pygame.K_SPACE:
                if self.players[self.activePlayer].isJumping == False and self.players[self.activePlayer].stillJumping != True:
                    self.players[self.activePlayer].isJumping = True
                    self.players[self.activePlayer].stillJumping = True
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
        self.nbDinos -= 1
        self.activePlayer = 0 if self.activePlayer >= self.nbDinos else self.activePlayer
        if isActivePlayer:
            self.players[self.activePlayer].isActivePlayer = True

        return self.verifyTeamIntegrity()

    def verifyTeamIntegrity(self):
        differentTeam = False
        lastTeam = 0;

        for i in range(self.nbDinos):
            differentTeam = False
            print(self.players[i].name + " : " + str(self.players[i].team))
            if(i == 0):
                lastTeam = self.players[i].team;
            elif(lastTeam != self.players[i].team):
                differentTeam = True
                break

        if not differentTeam:
            if lastTeam == 0:
                return constants.VICTORY_TEAM_1
            if lastTeam == 1:
                return constants.VICTORY_TEAM_2
            if lastTeam == 2:
                return constants.VICTORY_TEAM_3

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
            self.activePlayer = 0 if self.activePlayer >= self.nbDinos else self.activePlayer

            current_player = self.players[self.activePlayer]
            current_player.isActivePlayer = True

            self.proj.golfBall.changeOrig((current_player.x, current_player.y - current_player.allRect.h))