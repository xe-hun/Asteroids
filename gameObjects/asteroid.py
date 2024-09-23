from constant import HEIGHT, WIDTH, outlineColor, fillColor
import math
import pygame
import numpy as np





class Asteroid():
    def __init__(self, spawnPositionAndAngle:tuple):
       
        asteroidHalfSizeSize = 40 - np.random.randn() * 5
        stroke = 2
        numSide = 8

        pertubations = [(np.random.rand() * 15, np.random.rand() * 15) for _ in range(numSide)]
        polyAngles = [np.random.randn() * .02 + x for x in np.linspace(0, math.pi * 2 , numSide)]
        
        polygonPoints =  [((asteroidHalfSizeSize - pertubations[i][0]) * math.cos(j) + asteroidHalfSizeSize, (asteroidHalfSizeSize - pertubations[i][1]) * math.sin(j) + asteroidHalfSizeSize) for i, j in enumerate(polyAngles) if i < numSide - 1]
        
        self.__asteroidSurface = pygame.Surface((asteroidHalfSizeSize * 2 + stroke , asteroidHalfSizeSize * 2 + stroke), pygame.SRCALPHA)
        pygame.draw.polygon(self.__asteroidSurface, fillColor, polygonPoints)
        pygame.draw.polygon(self.__asteroidSurface, outlineColor, polygonPoints, stroke)
        self.asteroidRect = self.__asteroidSurface.get_rect()
        self.xPos = spawnPositionAndAngle[0]
        self.yPos = spawnPositionAndAngle[1]
        self.directionAngleRad = spawnPositionAndAngle[2]
        # self.directionAngleRad = 0
      
      
        self.speed = np.random.rand() + .1
        self.rotationAngle = 0
        self.ROTATION_RATE = 2 * np.random.randn()
        
          
    def isOutOfScreen(self):
        if self.xPos > WIDTH + 40 or self.xPos < -40 or \
            self.yPos > HEIGHT + 40 or self.yPos < -40:
                return True
        else:
            return False
        
       
    def dispose(self):
        print('disposed')
        pass
        # self.cannonSurfaceR = None
    

    def update(self, screen:pygame.Surface):
        
        self.xPos += self.speed * math.cos(self.directionAngleRad)
        self.yPos += self.speed * math.sin(self.directionAngleRad)         
        
        self.rotationAngle += self.ROTATION_RATE
        asteroidSurfaceR = pygame.transform.rotate(self.__asteroidSurface, self.rotationAngle)
        self.asteroidRect = asteroidSurfaceR.get_rect(center=(self.xPos, self.yPos))
        screen.blit(asteroidSurfaceR, self.asteroidRect.topleft)
        