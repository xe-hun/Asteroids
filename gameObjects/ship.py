from enum import Enum

import numpy as np
from constant import FPS, HEIGHT, WIDTH,\
                    WSCALE, outlineColor,\
                    fillColor
import math
import pygame
import Box2D

                  
from gameObjects.cannon import Cannon
from utils.helper import toComponent, toWorldPos,\
                        toPixelPos, debugDrawBox2DBodies,\
                        warpBox2DObject

class Steering(Enum):
    steeringLeft = 1
    steeringRight = 2
    noSteering = 3

class Ship():
    
    def __init__(self, world:Box2D.b2Body, CannonIsShot:callable, debugDraw:bool = False):
        
        self.debugDraw = debugDraw
        # ship constants 
        self.FIRE_RATE = 2
        self.BURST_RATE = 10
        self.BURST_COUNT = 3
        self.MAXSPEED = 100
        # turn rate in degrees
        self.TURN_RATE = 7
        
        # ship dimensions
        self.shipWidth = 30
        self.shipHeight = 40
        
        # ship flags
        self.cannonIsShot = CannonIsShot
        self.boosting = False
        self.steering = Steering.noSteering
        self.bursting = False
        self.shooting = False
        
        # ship parameters
        self.turnForce = 0
        self.boostForce = 900
        self.angleRad = 0
        self.acceleration = .07
        self.friction = .99
        self.xPos = WIDTH // 2
        self.yPos = HEIGHT // 2
        self.speedX = 0
        self.speedY = 0
        self.burstCounter = FPS // self.BURST_RATE * self.BURST_COUNT
        self.fireRateCounter = 0 
        
        
        # polygonPoints =  ((0,0),
        #                   (7, 5),
        #                   (15, 0),
        #                   (23, 5),
        #                   (30, 0),
        #                   (15, 40))
        
        # building the shop
        # polygon points for ship frame centered on zero
        # ships width is 30 and ships height is 40
        polygonPoints =  [(-15,-20), (-8, -15), (0, -20),
                          (8, -15), (15, -20), (0, 20)]
        # seperate the polygon shapes to mitigate against
        # convex shape for box2D
        polygonPointsSeperated = [[(-15,-20), (-8, -15), (0, 20)],
                                  [(-8, -15), (0, -20),(8, -15), (0, 20)],
                                  [ (8, -15), (15, -20), (0, 20)]]
                                  
        
        self.shipSurface, self.rect = self.buildShipInPixel(self.xPos, self.yPos,
                                            self.shipWidth, self.shipHeight, polygonPoints)
        
        self.image = self.shipSurface
        
        self.world = world
        self.box2DBodiesDebugList = []
        
        shipPositionInWorld = toWorldPos((self.xPos, self.yPos), WSCALE, HEIGHT)
        self.shipBodyBox2D = self.buildShipBodyBox2D(self.world, *shipPositionInWorld, polygonPointsSeperated)
        
    # def initializeBox2DWorld(self):
       
    #     return Box2D.b2World((0, 0))
    
        
    def buildShipBodyBox2D(self, world:Box2D.b2World, xPos, yPos, polygonPointsList):
        
        shipBody = world.CreateDynamicBody( position = (xPos, yPos))
        
        for polygonPoints in polygonPointsList:
            # scale down polygon points from pixel space to world space
            polygonPointsInWorldScale = [Box2D.b2Vec2(p) / WSCALE for p in polygonPoints]
            
            # print([(p[0] + 15, p[1] + 20) for p in polygonPoints])
       
            shipBody.CreateFixture(
                density = 1,
                friction = .3,
                shape = Box2D.b2PolygonShape(vertices = polygonPointsInWorldScale),
            )
        
        self.box2DBodiesDebugList.append(shipBody)
        shipBody.fixedRotation = True
        shipBody.inertia = 50
        # Box2D.b2Body.angularDamping = 500
        return shipBody
    
        
    def buildShipInPixel(self, xPos, yPos, shipWidth, shipHeight, polygonPoints):
        # shift the polygon points by half width and half ship height to make top left 0,0 for pygame coordinate
        strokeSize = 2
        polygonPointsShifted = [(i[0] + shipWidth / 2 , i[1] + shipHeight / 2 ) for i in polygonPoints]
        
        shipSurface = pygame.Surface((shipWidth + strokeSize, shipHeight + strokeSize), pygame.SRCALPHA)
        pygame.draw.polygon(shipSurface, fillColor, polygonPointsShifted)
        pygame.draw.polygon(shipSurface, outlineColor, polygonPointsShifted, strokeSize)
        rect = shipSurface.get_rect(center=(xPos, yPos))

        
        return shipSurface, rect
        
    
    def canFire(self):
        if self.fireRateCounter == 0:
            self.fireRateCounter = FPS / self.FIRE_RATE
            return True 
        else:
            return False
    

    def handleEvents(self, event: pygame.event):
    
        keys = pygame.key.get_pressed()
        if  keys[pygame.K_DOWN]:
            self.boosting = True
        else:
            self.boosting = False
            
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.shooting = True
        else:
            self.shooting = False
            
        if keys[pygame.K_LEFT]:
            self.steering = Steering.steeringLeft
        elif keys[pygame.K_RIGHT]:
            self.steering = Steering.steeringRight
        else:
            self.steering = Steering.noSteering
       
            
            
    def shootCannon(self, shipGunPosX, shipGunPosY):
      
        if self.shooting and self.canFire():
            self.bursting = True
            
        if self.bursting:
            if self.burstCounter % (FPS // self.BURST_RATE) == 0:
                cannon = Cannon(-self.angleRad - math.pi / 2, (shipGunPosX, shipGunPosY))
                self.cannonIsShot(cannon)
            self.burstCounter -= 1
            
        if self.burstCounter <= 0:
            self.burstCounter = FPS // self.BURST_RATE * self.BURST_COUNT
            self.bursting = False
            
        if self.fireRateCounter > 0 and self.bursting == False:
            self.fireRateCounter -= 1
       
       
    def update(self, screen:pygame.Surface):
        
        self.steerShip(self.steering)
        
        cannonPosition = toPixelPos(self.shipBodyBox2D.GetWorldPoint((-5/WSCALE, 15/WSCALE)), WSCALE, HEIGHT)
        self.shootCannon(*cannonPosition)
        
        self.boostShip(self.shipBodyBox2D, self.boosting, self.boostForce)
        
        self.capSpeed(self.shipBodyBox2D)
        warpBox2DObject(self.shipBodyBox2D)   
        
        shipPosition = toPixelPos(self.shipBodyBox2D.position, WSCALE, HEIGHT) 
        self.angleRad = self.shipBodyBox2D.angle
        self.image = pygame.transform.rotate(self.shipSurface, math.degrees(self.angleRad - math.pi))
        rect = self.image.get_rect(center=shipPosition)
        screen.blit(self.image, rect.topleft)      
        
        # boxLocal = [(-12, -20), (12, -20), (12, -80), (-12, -80)]
        # boxLocal = [(b[0]/WSCALE, b[1]/WSCALE) for b in boxLocal]
        
        # boxGlobal = [ self.shipBodyBox2D.GetWorldPoint(b) for b in boxLocal]
        
      
        # boxGlobal = [toPixelPos(b, WSCALE, HEIGHT) for b in boxGlobal]
        # pygame.draw.polygon(screen, (100,100,10), boxGlobal, 1)
        
        
             
        
        
        if self.debugDraw:
            debugDrawBox2DBodies(screen, self.box2DBodiesDebugList)
        
        
        
    def capSpeed(self, shipBody):
        velocity = shipBody.linearVelocity
        velocityMagnitude = velocity.length
        
        if velocityMagnitude > self.MAXSPEED:
            velocity.Normalize()
            velocity *= self.MAXSPEED
            
        shipBody.linearVelocity = velocity
            
   
    def boostShip(self, shipBody:Box2D.b2Body, boosting:bool, boostForce:int):
        if boosting == False:
            return
        
        angleRad = shipBody.angle
        forcePoint = shipBody.GetWorldPoint((0, -15/WSCALE))
        forceVector = boostForce * toComponent(angleRad + math.pi / 2)
        shipBody.ApplyForce(forceVector, forcePoint, True)

        
        
    def steerShip(self, steering:Steering):
        self.turnForce += .2
        self.turnForce = min(self.turnForce, self.TURN_RATE)
        
        if steering == Steering.steeringRight:
            self.shipBodyBox2D.angle -= math.radians(self.turnForce)
        elif steering == Steering.steeringLeft:
            self.shipBodyBox2D.angle += math.radians(self.turnForce)
        elif steering == Steering.noSteering:
            self.turnForce = 0
    
    # def drawShip(self, screen:pygame.Surface, angleRad:float, position:tuple, shipSurface:pygame.Surface):
    #     image = pygame.transform.rotate(shipSurface, math.degrees(angleRad - math.pi))
    #     rect = self.image.get_rect(center=position)
    #     screen.blit(self.image, self.rect.topleft)
        
    #     return rect, image
    
        