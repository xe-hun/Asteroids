from enum import Enum
from constant import FPS, HEIGHT, WIDTH, outlineColor, fillColor
import math
import pygame

from cannon import Cannon

class Steering(Enum):
    steeringLeft = 1
    steeringRight = 2
    noSteering = 3

class Ship():
    
    
    
    def __init__(self, cannonIsShot:callable):
        self.cannonIsShot = cannonIsShot
        self.shipWidth = 30
        self.shipHeight = 40
        polygonPoints =  ((0,0), (self.shipWidth, 0), (self.shipWidth // 2, self.shipHeight))
        self.shipSurface = pygame.Surface((self.shipWidth + 2, self.shipHeight + 2), pygame.SRCALPHA)
        pygame.draw.polygon(self.shipSurface, fillColor, polygonPoints)
        pygame.draw.polygon(self.shipSurface, outlineColor, polygonPoints, 2)
        self.shipSurface = pygame.transform.rotate(self.shipSurface, 90)
        self.angleRad = 0
        self.acceleration = .07
        self.friction = .99
        self.xPos = WIDTH // 2
        self.yPos = HEIGHT // 2
        self.MAXSPEED = 7
        self.TURN_RATE = math.pi / 180 * 4
        self.boosting = False
        self.steering = Steering.noSteering
        self.speedX = 0
        self.speedY = 0
        # fireRatePerSecond
        self.fireRate = 10
        self.fireRateCounter = 0 
        self.shooting = False
        
    
    def canFire(self):
        if self.fireRateCounter == 0:
            self.fireRateCounter = FPS // self.fireRate
            return True 
        else:
            return False
    
    def wrapTheShip(self):
        if self.xPos > WIDTH:
            self.xPos = 0
        elif self.xPos < 0:
            self.xPos = WIDTH
        elif self.yPos  > HEIGHT:
            self.yPos = 0
        elif self.yPos < 0:
            self.yPos = HEIGHT
    

    def handleEvents(self, event: pygame.event):
    
        keys = pygame.key.get_pressed()
        if  keys[pygame.K_DOWN]:
            self.boosting = True
        else:
            self.boosting = False
            
        if keys[pygame.K_UP]:
            self.shooting = True
        else:
            self.shooting = False
            
        if keys[pygame.K_LEFT]:
            self.steering = Steering.steeringLeft
        elif keys[pygame.K_RIGHT]:
            self.steering = Steering.steeringRight
        else:
            self.steering = Steering.noSteering
       
            
    def updateShipDirection(self):
          
        if self.boosting:
            # accelerate the ship
            self.speedX += self.acceleration * math.cos(self.angleRad)
            self.speedY += self.acceleration * math.sin(self.angleRad)
            
            self.speedX *= self.friction
            self.speedY *= self.friction
            
            
        # update the ship position
        self.xPos += self.speedX
        self.yPos += self.speedY
        
    
    def updateShipSteering(self):
        if self.steering == Steering.steeringLeft:
            self.angleRad -= self.TURN_RATE
        elif self.steering == Steering.steeringRight:
            self.angleRad += self.TURN_RATE
            
    def shootCannon(self):
        if self.shooting:
            if self.canFire():
                shipGunPosX = self.xPos + self.shipHeight / 2 * math.cos(self.angleRad)
                shipGunPosY = self.yPos + self.shipHeight / 2 * math.sin(self.angleRad)
                cannon = Cannon(self.angleRad, (shipGunPosX, shipGunPosY))
                self.cannonIsShot(cannon)
                
        if self.fireRateCounter > 0:
            self.fireRateCounter -= 1
        
       
    def update(self, screen:pygame.Surface):
        
        self.updateShipSteering()
        self.updateShipDirection()
        self.wrapTheShip()
        self.shootCannon()
        
        shipSurfaceR = pygame.transform.rotate(self.shipSurface, -math.degrees(self.angleRad))
        shipRect = shipSurfaceR.get_rect(center=(self.xPos, self.yPos))
        screen.blit(shipSurfaceR, shipRect.topleft)
        