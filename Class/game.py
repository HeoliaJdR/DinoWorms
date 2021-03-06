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

        self.lastTeamPlayed = 0;
        self.lastPlayerTeam1 = -1
        self.lastPlayerTeam2 = -1
        self.lastPlayerTeam3 = -1

    def initPlayers(self):
        self.players = []
        self.team = []
        xOrig = 50
        yOrig = 350
        for i in range (self.nbDinos):
            self.players.append(characters.Characters(100, i%self.nbPlayers, xOrig, yOrig, True, "Joueur_" + str(i+1)))
            if i == 0:
                self.players[i].isActivePlayer = True
            xOrig += 175

    def printElements(self, screen):
        area = self.world.getPixels()
        endOfGame = False

        self.world.printBackground(screen)
        if self.world.needChangeArrow:
            self.world.animWindArrow()

        needEndOfTurn = not self.proj.launchBall(screen, area, self.world, self.players)

        for player in self.players:
            if not player.isDead or player.playDeadAnim:
                player.moveCharacter(self.world, area)
                needDestroy = not player.displayCharacter(screen)
                player.updateYPos(self.world, area)
                player.jumpCharacter(self.world, area)

                if player.isActivePlayer and player.hasFallen:
                    needDestroy = True
                    needEndOfTurn = True

                if needDestroy:
                    endOfGame = self.destroyPlayer(player)

            mousePosX,mousePosY = pygame.mouse.get_pos()

            if player.isActivePlayer and not self.proj.shoot and mousePosX > player.x:
                self.proj.golfBall.changeOrig((player.x + 30, player.y - 20))
                if not player.lookRight:
                    player.flipAnim()
                    player.lookRight = True
            elif player.isActivePlayer and not self.proj.shoot:
                self.proj.golfBall.changeOrig((player.x - 70, player.y - 20))
                if player.lookRight:
                    player.flipAnim()
                    player.lookRight = False

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
        player.isDead = True

        return self.verifyTeamIntegrity()

    def verifyTeamIntegrity(self):
        differentTeam = False
        lastTeam = 0;

        for i in range(self.nbDinos):
            if not self.players[i].isDead:
                differentTeam = False
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

    def findNextPlayer(self):
        playerFind = False

        potentialPlayerFind = False

        for j in range(self.nbPlayers):
            nextTeam = self.lastTeamPlayed + 1 + j if j + self.lastTeamPlayed + 1 < self.nbPlayers else j + self.lastTeamPlayed + 1 - self.nbPlayers

            for i in range(self.nbDinos):
                nextPlayer = i + self.activePlayer if i + self.activePlayer < self.nbDinos else self.activePlayer + i - self.nbDinos

                if(self.players[nextPlayer].team == nextTeam and not self.players[nextPlayer].isDead):
                    self.activePlayer = nextPlayer
                    self.lastTeamPlayed = nextTeam

                    if self.lastPlayerTeam1 == nextPlayer or self.lastPlayerTeam2 == nextPlayer  or self.lastPlayerTeam3 == nextPlayer:
                        potentialPlayerFind = True
                    else:
                        playerFind = True
                        break

            if playerFind or potentialPlayerFind:
                break

        if nextTeam == 1:
            self.lastPlayerTeam1 = nextPlayer
        elif nextTeam == 2:
            self.lastPlayerTeam2 = nextPlayer
        else:
            self.lastPlayerTeam3 = nextPlayer

    def endOfTurn(self):
        self.world.generateWind()
        self.timer = 0

        if self.players:
            if self.players[self.activePlayer].hp > 0:
                self.players[self.activePlayer].animConstant = constants.IDLE

            self.players[self.activePlayer].wantsToWalkLeft = False
            self.players[self.activePlayer].wantsToWalkRight = False
            self.players[self.activePlayer].isActivePlayer = False

            self.findNextPlayer()

            current_player = self.players[self.activePlayer]
            current_player.isActivePlayer = True