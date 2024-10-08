
import math
import pygame

from constant import HEIGHT, WIDTH, outlineColor
from utils.shake import Shake


class Cannon(pygame.sprite.Sprite):
    def __init__(self, angleRad:float, startPosition:tuple, shake:Shake):
        
        super().__init__()
      
        self.shake = shake
        # 5 pixels
        self.cannonSize = 15
        self.cannonSpeed = 10
        self.cannonThickness = 2
        
        cannonSurface = pygame.Surface((self.cannonSize, self.cannonThickness), pygame.SRCALPHA)
        pygame.draw.line(cannonSurface, outlineColor, (0, 0), (self.cannonSize, 0), self.cannonThickness)
        self.cannonSurfaceR = pygame.transform.rotate(cannonSurface, -math.degrees(angleRad))
        self.image = self.cannonSurfaceR
        self.rect = self.cannonSurfaceR.get_rect()
        self.mask = pygame.mask.from_surface(self.cannonSurfaceR)
        self.directionX = math.cos(angleRad)
        self.directionY = math.sin(angleRad) 
        
    
        self.XPos = startPosition[0]
        self.YPos = startPosition[1]

        
    def update(self, screen:pygame.Surface):
        self.XPos += self.cannonSpeed * self.directionX
        self.YPos += self.cannonSpeed * self.directionY
        
        self.XPos, self.YPos = tuple(map(self.shake.watch, (self.XPos, self.YPos)))
        
        self.rect = self.cannonSurfaceR.get_rect(center = (self.XPos, self.YPos))
        screen.blit(self.cannonSurfaceR, self.rect.topleft)
         
    def isOutOfScreen(self):
        if self.XPos > WIDTH or self.XPos < 0 or \
            self.YPos > HEIGHT or self.YPos < 0:
                return True
        else:
            return False
                
            
         
    def dispose(self):
        self.cannonSurfaceR = None
    