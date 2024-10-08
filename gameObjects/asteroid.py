import random
from constant import HEIGHT, WIDTH, WSCALE, outlineColor, fillColor,\
    BOX2D_ASTEROID_USER_DATA
import math
import pygame
import numpy as np
import Box2D

from utils.shake import Shake
from utils.helper import debugDrawBox2DBodies, mapValue, toComponent, toPixelPos, warpBox2DObject


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, world:Box2D.b2World, shake:Shake, xPos:float = None, yPos:float = None, debugDraw:bool = False, halfSize:float = None):
        
        super().__init__()
        self.debugDraw = debugDraw
        self.shake = shake
        self.world = world
        self.box2DBodiesDebugList = []
        # outOfBoundsExtension prevents the asteroid from being remove right after creation
        # because its created out of bounds, 
        # shifts the out of bound margin by outOfBoundsExtension
        self.outOfBoundsExtension = 50 / WSCALE
        creationExtension = 30 / WSCALE
        
        # asteroid constants
        MIN_SIZE = 12
        MAX_SIZE = 30
        MIN_LIFE = 1
        MAX_LIFE = 3
        MIN_SIDES = 7
        MAX_SIDES = 12
        
       
        stroke = 2
        self.breakageThreshold = MIN_SIZE
        lenghtDisplacementRange = 10
        angleDisplacementRange = .05
        
        
        self.asteroidHalfSize =  np.random.randint(MIN_SIZE, MAX_SIZE) if halfSize is None else halfSize
        numSide = np.random.randint(MIN_SIDES, MAX_SIDES)
          # map the asteroid life according to its size
        self.asteroidLife = int(mapValue(MIN_SIZE, MAX_SIZE, MIN_LIFE, MAX_LIFE, self.asteroidHalfSize))
      

        x, y, direction = self.generateInitialStates(creationExtension)
        self.xPos = x if xPos is None else xPos
        self.yPos = y if yPos is None else yPos
        
        speed = 7 + random.random() * 15
        linearVelocity = toComponent(direction) * speed
        angularVelocity = 2 + random.random() * 5
        
        position = (self.xPos, self.yPos)
        
        polygonPoints = self.createPolygonPoints(self.asteroidHalfSize, numSide, lenghtDisplacementRange, angleDisplacementRange)
        self.asteroidBodybox2D = self.createAsteroidBodyBox2D(polygonPoints, self.world, position, linearVelocity, angularVelocity)

         
        self.__asteroidSurface = self.drawAsteroidSurface(polygonPoints, self.asteroidHalfSize, stroke)
        self.image = self.__asteroidSurface
        self.rect = self.__asteroidSurface.get_rect()
        
       
        # worldPoint = self.asteroidBodybox2D.GetWorldPoint((0, 0))
        # impulseDirection = toComponent(direction) * speed
        # self.asteroidBodybox2D.ApplyLinearImpulse(impulseDirection, worldPoint, True)
        # self.asteroidBodybox2D.angularVelocity = 2
        

        
        
        
    def generateInitialStates(self, creationExtension):
        
        pi = math.pi
        worldHeight, worldWidth = HEIGHT / WSCALE, WIDTH / WSCALE
        
        
        return tuple(random.choices([
            (-creationExtension,                           np.random.rand() * worldHeight,   mapValue(0, 1, -0.25 * pi, 0.25 * pi, np.random.rand())),
            (worldWidth + creationExtension,               np.random.rand() * worldHeight,   mapValue(0, 1, 0.75 * pi , 1.25 * pi, np.random.rand())),
            (np.random.rand() * worldWidth,    worldHeight + creationExtension,              mapValue(0, 1, 1.25 * pi , 1.75 * pi, np.random.rand())),
            (np.random.rand() * worldWidth,    -creationExtension,                           mapValue(0, 1, 0.25 * pi , 0.75 * pi, np.random.rand())),
         ],
         weights=[1,1,1,1]).pop())
        
   
        
    def createPolygonPoints(self, asteroidHalfSize, numSide, lenghtDisplacementRange, angleDisplacementRange):
        # give the polygon uneven sides and angles
       
       
        displacement = [(asteroidHalfSize - np.random.randint(0, lenghtDisplacementRange), asteroidHalfSize -np.random.randint(0, lenghtDisplacementRange)) for _ in range(numSide)]
        polyAngles = [np.random.randn() * angleDisplacementRange + x for x in np.linspace(0, math.pi * 2 , numSide)]
        
        # add displacement values to each sides and angles of the polygon
        polygonPoints = [(displacement[i][0] * math.cos(j), displacement[i][1] * math.sin(j)) for i, j in enumerate(polyAngles) if i < numSide - 1]
       
        return polygonPoints
        
        
    def createAsteroidBodyBox2D(self, polygonPoints, world:Box2D.b2World, position, linearVelocity, angularVelocity):
        # scale the polygon points to world dimension
        polygonPoints = [(p[0] / WSCALE, p[1] / WSCALE) for p in polygonPoints]
        # invert the x axis to account for inverted angle rotation when creating the polygon points
        polygonPoints = [(-p[0], p[1]) for p in polygonPoints]
        
        asteroidBody = world.CreateDynamicBody(position = position,
                                               linearVelocity = linearVelocity,
                                               angularVelocity = angularVelocity,
                                               userData = BOX2D_ASTEROID_USER_DATA,
                                            )
        
        asteroidShape = Box2D.b2PolygonShape(vertices = polygonPoints)
        asteroidBody.CreateFixture(
            shape = asteroidShape,
            density = 1,
            friction = .3,
            restitution = .4
        )
        
        self.box2DBodiesDebugList.append(asteroidBody)
        return asteroidBody
        

    def drawAsteroidSurface(self, polygonPoints, asteroidHalfSize, stroke):
        # shift the polygon so that pos 0, 0 is at top left for pygame coordinate

        polygonPointsShifted = [(polygonPoints[i][0] + asteroidHalfSize, polygonPoints[i][1] + asteroidHalfSize) for i in range(len(polygonPoints))]
        asteroidSurface = pygame.Surface((asteroidHalfSize * 2 + stroke , asteroidHalfSize * 2 + stroke), pygame.SRCALPHA)
        pygame.draw.polygon(asteroidSurface, fillColor, polygonPointsShifted)
        pygame.draw.polygon(asteroidSurface, outlineColor, polygonPointsShifted, stroke)
        return asteroidSurface
        
        
    def takeDamage(self):
        self.asteroidLife -= 1
        
    def isAsteroidDead(self):
        return self.asteroidLife <= 0
    
    def canBreakApart(self):
        return self.asteroidHalfSize > self.breakageThreshold * 2
        
    
    def breakApart(self, debugDraw:bool):
        position = self.asteroidBodybox2D.position
        asteroidHalfSize = max(((self.asteroidHalfSize + np.random.randn() * 10)/ 2), self.breakageThreshold)
        asteroidA = Asteroid(self.world, self.shake, *position, debugDraw, asteroidHalfSize)
        asteroidHalfSize = max(((self.asteroidHalfSize + np.random.randn() * 10)/ 2), self.breakageThreshold)
        asteroidB = Asteroid(self.world, self.shake, *position, debugDraw, asteroidHalfSize)
        return asteroidA, asteroidB
        
        
       
    def dispose(self):
        self.__asteroidSurface = None
        self.world.DestroyBody(self.asteroidBodybox2D)
        pass
    

    def update(self, screen:pygame.Surface):
        
        
        
        warpBox2DObject(self.asteroidBodybox2D)  
        position = toPixelPos(self.asteroidBodybox2D.position, WSCALE, HEIGHT) 
        position = tuple(map(self.shake.watch, position))
 
        angleRad = self.asteroidBodybox2D.angle
        self.image = pygame.transform.rotate(self.__asteroidSurface, math.degrees(angleRad - math.pi))
        self.rect = self.image.get_rect(center=position)
        screen.blit(self.image, self.rect.topleft)  
        
        if self.debugDraw:
            debugDrawBox2DBodies(screen, self.box2DBodiesDebugList)
