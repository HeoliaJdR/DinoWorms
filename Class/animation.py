import pygame


class Animation:

    def __init__(self, spriteSheetPath, sizeRect, firstRect, totalFrame, numberFramesPerLine, numberLinesFrame = 1, delayBetweenFrame = 5, isLoopAnim = False):
        self.spriteSheet = pygame.image.load(spriteSheetPath).convert_alpha()
        self.sizeRect = sizeRect
        self.firstRect = firstRect
        self.currentRect = (firstRect[0], firstRect[1], sizeRect[0], sizeRect[1])
        self.frame = 0
        self.line = 0
        self.numberFramesPerLine = numberFramesPerLine
        self.totalFrame = totalFrame
        self.numberLinesFrame = numberLinesFrame
        self.isLoopAnim = isLoopAnim
        self.isEndAnim = False
        self.currentTicks = 0
        self.delayBetweenFrame = delayBetweenFrame
        self.currentFrame = 1

    def extraParameter(self, **kwargs):
        try:
            scaleSpriteSheet = (
                kwargs["scale"][0] * self.numberFramesPerLine,
                kwargs["scale"][1] * self.numberLinesFrame
            )
            self.spriteSheet = pygame.transform.scale(self.spriteSheet, scaleSpriteSheet)
            self.sizeRect = kwargs["scale"]
        except Exception:
                pass

        try:
            self.function = kwargs["function"][0]
            self.frameActivate = kwargs["function"][1]
            self.param = kwargs["function"][2]
        except Exception:
                pass

    def playAnim(self, screen, orig):
        if self.currentTicks == 0 or pygame.time.get_ticks() - self.currentTicks > self.delayBetweenFrame:
            self.currentTicks = pygame.time.get_ticks()

            if self.currentFrame > self.totalFrame:
                if self.isLoopAnim:
                    self.frame = 0
                    self.currentFrame = 1
                    self.line = 0
                else:
                    self.isEndAnim = True
                    self.frame = 0
                    self.currentFrame = 1
                    self.line = 0
                    return False

            if self.frame + 1 > self.numberFramesPerLine:
                self.line += 1
                self.frame = 0

            try:
                if self.currentFrame == self.frameActivate:
                    self.function(self.param[0], self.param[1], self.param[2])
            except Exception:
                pass

            self.currentRect = (self.firstRect[0] + (self.sizeRect[0] * self.frame), self.firstRect[1] + (self.sizeRect[1] * self.line), self.sizeRect[0], self.sizeRect[1])
            self.frame += 1
            self.currentFrame += 1

        orig = (orig[0] - (self.sizeRect[0]/2), orig[1] - (self.sizeRect[1]/2))
        screen.blit(self.spriteSheet, orig, self.currentRect)
        return True
