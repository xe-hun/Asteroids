       
import math
import numpy as np
import pygame
from utils.camera import Camera
from constant import HEIGHT, WIDTH
from utils.helper import angleDiff, dot, norm, rotateVec, scale


class Rocket(pygame.sprite.Sprite):
    def __init__(self, startPosition:tuple, startDirection:tuple, camera:Camera):
        
        super().__init__()
        
        self.camera = camera
        
        self.image = scale(pygame.image.load('images/rocket.png').convert_alpha(), .2)
        self.rect = self.image.get_rect()
        
        self.speed = 5
        self.angle = 0
        self.position = np.array(startPosition)
        self.updatedDirection = startDirection
        self.currentDirection = self.updatedDirection
        self.turnRate = math.radians(4)
        self.rect = self.image.get_rect()
        self.targetPosition = None
        
        
    def toWorldPos(self, vec:tuple):
        return self.position + rotateVec(vec, self.angle)
    
    def hasTarget(self):
        return self.targetPosition != None
        
    def setTargetPosition(self, targetPosition):
        self.targetPosition = targetPosition
        if self.hasTarget():
            self.updatedDirection = norm(np.array(targetPosition) - self.position)

        # if self.currentDirection is None:
        #     self.currentDirection = self.updatedDirection
        
    
    def update(self, screen:pygame.surface.Surface):
    
        if angleDiff(self.currentDirection, self.updatedDirection) < self.turnRate:
            self.currentDirection = self.updatedDirection
        else:
            dotProd = dot(self.currentDirection, rotateVec(self.updatedDirection, math.pi / 2))
                
            if dotProd > 0:
                self.currentDirection = rotateVec(self.currentDirection, -self.turnRate)
            elif dotProd < 0:
                self.currentDirection = rotateVec(self.currentDirection, self.turnRate)
            
        self.velocity = self.currentDirection * self.speed
        self.angle = math.atan2(self.currentDirection[1], self.currentDirection[0])
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        self.draw(screen)
        
        
    
    def draw(self, screen:pygame.surface.Surface):
       
        rotImg = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = rotImg.get_rect(center = (self.position[0], self.position[1]))
        screen.blit(rotImg, self.rect.topleft)
        
        
    def isOutOfScreen(self):
        if self.position[0] > WIDTH or self.position[0] < 0 or \
            self.position[1] > HEIGHT or self.position[1] < 0:
                return True
        else:
            return False
        
    # def warp(self):
    #     if self.position[0] > WIDTH:
    #         self.position[0] = 0
    #     if self.position[0] < 0:
    #         self.position[0] = WIDTH
            
    #     if self.position[1] > HEIGHT:
    #         self.position[1] = 0
    #     if self.position[1] < 0:
    #         self.position[1] = HEIGHT
  
    
    
    