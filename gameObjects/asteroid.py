import random
from constant import HEIGHT, WIDTH, WSCALE, outlineColor, fillColor
import math
import pygame
import numpy as np
import Box2D

from utils.helper import debugDrawBox2DBodies, getBodyBounds, mapValue, toComponent, toPixelPos


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, world:Box2D.b2World, xPos, yPos, debugDraw:bool = False):
        
        super().__init__()
        self.debugDraw = debugDraw
        self.world = world
        
        # asteroid constants
        MIN_SIZE = 20
        MAX_SIZE = 65
        MIN_LIFE = 1
        MAX_LIFE = 8
        MIN_SIDES = 7
        MAX_SIDES = 12
        
        # outOfBoundsExtension prevents the asteroid from being remove right after creation
        # because its created out of bounds, 
        # shifts the out of bound margin by outOfBoundsExtension
        self.outOfBoundsExtension = 50 / WSCALE
        creationExtension = 30 / WSCALE
        
        speed = 1000
        stroke = 2
        
        self.box2DBodiesDebugList = []
        
        asteroidHalfSize = np.random.randint(MIN_SIZE, MAX_SIZE)
        numSide = np.random.randint(MIN_SIDES, MAX_SIDES)
          # map the asteroid life according to its size
        self.asteroidLife = int(mapValue(MIN_SIZE, MAX_SIZE, MIN_LIFE, MAX_LIFE, asteroidHalfSize))
        print(self.asteroidLife)


        xPos, yPos, direction = self.generateInitialStates(creationExtension)
        polygonPoints = self.createPolygonPoints(asteroidHalfSize, numSide)
        self.asteroidBodybox2D = self.createAsteroidBodyBox2D(polygonPoints, self.world, xPos, yPos)

         
        self.__asteroidSurface = self.drawAsteroidSurface(polygonPoints, asteroidHalfSize, stroke)
        # self.mask = pygame.mask.from_surface(self.__asteroidSurface)
        self.image = self.__asteroidSurface
        self.rect = self.__asteroidSurface.get_rect()
        
       
        worldPoint = self.asteroidBodybox2D.GetWorldPoint((0, 0))
        impulseDirection = toComponent(direction) * speed
        self.asteroidBodybox2D.ApplyLinearImpulse(impulseDirection, worldPoint, True)
        self.asteroidBodybox2D.angularVelocity = 2
        
        self.tFlag = True
        
        
        
        
        
    def generateInitialStates(self, creationExtension):
        
        pi = math.pi
        worldHeight, worldWidth = HEIGHT / WSCALE, WIDTH / WSCALE
        
        
        return tuple(random.choices([
            (-creationExtension,                           np.random.rand() * worldHeight,   mapValue(0, 1, -0.25 * pi, 0.25 * pi, np.random.rand())),
            (worldWidth + creationExtension,               np.random.rand() * worldHeight,   mapValue(0, 1, 0.75 * pi , 1.25 * pi, np.random.rand())),
            (np.random.rand() * worldWidth,    worldHeight + creationExtension,              mapValue(0, 1, 1.25 * pi , 1.75 * pi, np.random.rand())),
            (np.random.rand() * worldWidth,    -creationExtension,                           mapValue(0, 1, 0.25 * pi , 0.75 * pi, np.random.rand())),
         ],
         weights=[2,1,3,1]).pop())
        
   
        
    def createPolygonPoints(self, asteroidHalfSize, numSide):
        # give the polygon uneven sides and angles
        lenghtDisplacementRange = 15
        angleDisplacementRange = .02
       
        displacement = [(asteroidHalfSize - np.random.randint(0, lenghtDisplacementRange), asteroidHalfSize -np.random.randint(0, lenghtDisplacementRange)) for _ in range(numSide)]
        polyAngles = [np.random.randn() * angleDisplacementRange + x for x in np.linspace(0, math.pi * 2 , numSide)]
        
        # add displacement values to each sides and angles of the polygon
        polygonPoints = [(displacement[i][0] * math.cos(j), displacement[i][1] * math.sin(j)) for i, j in enumerate(polyAngles) if i < numSide - 1]
       
        return polygonPoints
        # return [((asteroidHalfSize - displacement[i][0]) * math.cos(j) + asteroidHalfSize, (asteroidHalfSize - displacement[i][1]) * math.sin(j) + asteroidHalfSize) for i, j in enumerate(polyAngles) if i < numSide - 1]
        
        
    def createAsteroidBodyBox2D(self, polygonPoints, world:Box2D.b2World, xPos:float, yPos:float):
        # scale the polygon points to world dimension
        polygonPoints = [(p[0] / WSCALE, p[1] / WSCALE) for p in polygonPoints]
        # invert the x axis to account for inverted angle rotation when creating the polygon points
        polygonPoints = [(p[0], -p[1]) for p in polygonPoints]
        
        asteroidBody = world.CreateDynamicBody(position = (xPos, yPos))
        asteroidShape = Box2D.b2PolygonShape(vertices = polygonPoints)
        asteroidBody.CreateFixture(
            shape = asteroidShape,
            density = 1,
            friction = .3,
            restitution = .4
        )
        self.box2DBodiesDebugList.append(asteroidBody)
        return asteroidBody
        # Box2D.b2Body.CreateFix
        

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
        
          
    def isOutOfScreen(self):
        if self.xPos > WIDTH + 40 or self.xPos < -40 or \
            self.yPos > HEIGHT + 40 or self.yPos < -40:
                return True
        else:
            return False
        
       
    def dispose(self):
        self.__asteroidSurface = None
        self.world.DestroyBody(self.asteroidBodybox2D)
        print('disposed')
        pass
    

    def update(self, screen:pygame.Surface):
        
        position = toPixelPos(self.asteroidBodybox2D.position, WSCALE, HEIGHT) 
        angleRad = self.asteroidBodybox2D.angle
        self.image = pygame.transform.rotate(self.__asteroidSurface, math.degrees(angleRad - math.pi))
        self.rect = self.image.get_rect(center=position)
        screen.blit(self.image, self.rect.topleft)  
        
        if self.debugDraw:
            debugDrawBox2DBodies(screen, self.box2DBodiesDebugList)


    def isOutOfBounds(self):
        left, top, right, bottom = getBodyBounds(self.asteroidBodybox2D)
        
        return right < 0 - self.outOfBoundsExtension or left > WIDTH/WSCALE + self.outOfBoundsExtension or top < 0 - self.outOfBoundsExtension or bottom > HEIGHT / WSCALE + self.outOfBoundsExtension

        