import math
import pygame
import Box2D
from enums.enums import Steering
from gameObjects.rocket import Rocket
from strategies.shootingStrategy import ShootingStrategy
from utils.camera import Camera
from utils.box2DHelperClasses import RaycastCallback
from constant import BOX2D_SHIP_USER_DATA, FPS, HEIGHT, WIDTH,\
                    WSCALE, outlineColor,\
                    fillColor

from gameObjects.cannon import Cannon
from utils.helper import norm, toComponent, toWorldPos,\
                        toPixelPos, debugDrawBox2DBodies,\
                        warpBox2DObject



class Ship():
    
    def __init__(self, world:Box2D.b2Body, ProjectileIsShot:callable, camera:Camera, debugDraw:bool = False):
        
        self.debugDraw = debugDraw
      
        CANNON_FIRE_COOL_DOWN = 2
        CANNON_BURST_RATE = 10
        CANNON_BURST_COUNT = 3
        
        MISSILE_FIRE_COOL_DOWN = 1
        MISSILE_BURST_RATE = 5
        MISSILE_BURST_COUNT = 3
        
        self.cannonFireStrategy = ShootingStrategy(CANNON_FIRE_COOL_DOWN, CANNON_BURST_RATE, CANNON_BURST_COUNT)
        self.missileFireStrategy = ShootingStrategy(MISSILE_FIRE_COOL_DOWN, MISSILE_BURST_RATE, MISSILE_BURST_COUNT)
        
        self.MAXSPEED = 100
        # turn rate in degrees
        self.TURN_RATE = 7
        
        # ship dimensions
        self.shipSizeScale = 0.7
        self.shipWidth = 30 * self.shipSizeScale
        self.shipHeight = 40 * self.shipSizeScale
        self.shipBasePoint = - self.shipWidth / (2 * WSCALE)
        
        # ship flags
        self.registerWeaponShots = ProjectileIsShot
        self.boosting = False
        self.steering = Steering.noSteering
   
        
        # ship parameters
        self.turnForce = 0
        self.boostForce = 500
        self.angleRad = 0
        self.acceleration = .07
        self.friction = .99
        self.xPos = WIDTH // 2
        self.yPos = HEIGHT // 2
        self.speedX = 0
        self.speedY = 0

        
        # anti thrust parameters
        self.antiThrustRange = 20
        self.antiThrustForce = 4000
        
        # building the shop
        # polygon points for ship frame centered on zero
        # ships width is 30 and ships height is 40
        b2Vec2 = Box2D.b2Vec2
        polygonPoints =  [
                          b2Vec2(-15,-20) * self.shipSizeScale,
                          b2Vec2(-8, -15) * self.shipSizeScale,
                          b2Vec2(0, -20) * self.shipSizeScale,
                          b2Vec2(8, -15) * self.shipSizeScale,
                          b2Vec2(15, -20) * self.shipSizeScale,
                          b2Vec2(0, 20) * self.shipSizeScale
                        ]
        # seperate the polygon shapes to mitigate against
        # convex shape for box2D
        polygonPointsSeperated =    [
                                        [
                                            b2Vec2(-15,-20) * self.shipSizeScale,
                                            b2Vec2(-8, -15) * self.shipSizeScale,
                                            b2Vec2(0, 20) * self.shipSizeScale
                                        ],
                                        [
                                            b2Vec2(-8, -15) * self.shipSizeScale,
                                            b2Vec2(0, -20) * self.shipSizeScale,
                                            b2Vec2(8, -15) * self.shipSizeScale,
                                            b2Vec2(0, 20) * self.shipSizeScale
                                        ],    
                                        [   b2Vec2(8, -15) * self.shipSizeScale,
                                            b2Vec2(15, -20) * self.shipSizeScale,
                                            b2Vec2(0, 20) * self.shipSizeScale
                                        ]
                                    ]
                                  
        
        self.shipSurface, self.rect = self.buildShipInPixel(self.xPos, self.yPos,
                                            self.shipWidth, self.shipHeight, list(polygonPoints))
        
        self.image = self.shipSurface
        
        self.world = world
        self.box2DBodiesDebugList = []
        
        shipPositionInWorld = toWorldPos((self.xPos, self.yPos), WSCALE, HEIGHT)
        self.shipBodyBox2D = self.buildShipBodyBox2D(self.world, *shipPositionInWorld, list(polygonPointsSeperated))
        
        self.camera = camera
       

        
    def buildShipBodyBox2D(self, world:Box2D.b2World, xPos, yPos, polygonPointsList):
        
        shipBody = world.CreateDynamicBody( 
                                           position = (xPos, yPos),
                                           userData = BOX2D_SHIP_USER_DATA,
                                           )
        
        for polygonPoints in polygonPointsList:
            # scale down polygon points from pixel space to world space
            polygonPointsInWorldScale = [p / WSCALE for p in polygonPoints]
            
            shipBody.CreateFixture(
                density = 1,
                friction = .3,
                shape = Box2D.b2PolygonShape(vertices = polygonPointsInWorldScale)
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
        
    def handleEvents(self, event: pygame.event):
    
        keys = pygame.key.get_pressed()
        if  keys[pygame.K_DOWN]:
            self.boosting = True
        else:
            self.boosting = False
            
        if keys[pygame.K_UP]:
            self.cannonFireStrategy.shooting = True
        else:
            self.cannonFireStrategy.shooting = False
            
        if keys[pygame.K_SPACE]:
            self.missileFireStrategy.shooting = True
        else:
            self.missileFireStrategy.shooting = False
            
        if keys[pygame.K_LEFT]:
            self.steering = Steering.steeringLeft
        elif keys[pygame.K_RIGHT]:
            self.steering = Steering.steeringRight
        else:
            self.steering = Steering.noSteering
       
       
    def fireCannon(self):
        cannonPosition = toPixelPos(self.shipBodyBox2D.GetWorldPoint((-5/WSCALE, 15/WSCALE)), WSCALE, HEIGHT)
        cannonPosition = tuple(map(self.camera.watch, cannonPosition))
        cannon = Cannon(-self.angleRad - math.pi / 2, cannonPosition, self.camera)
        self.registerWeaponShots(cannon)
        
    def fireMissile(self):
        rocketPosition = toPixelPos(self.shipBodyBox2D.GetWorldPoint((-5/WSCALE, 15/WSCALE)), WSCALE, HEIGHT)
        rocketPosition = tuple(map(self.camera.watch, rocketPosition))
        missile = Rocket(rocketPosition, self.getDirection(), self.camera)
        self.registerWeaponShots(missile)
        
    def getDirection(self):
        return norm(toComponent(-self.angleRad - math.pi / 2))
        
       
    def update(self, screen:pygame.Surface, isLevelInProgress):
        if isLevelInProgress:
            self.steerShip(self.steering)
            
            self.cannonFireStrategy.update(self.fireCannon)
            self.missileFireStrategy.update(self.fireMissile)
        
            self.boostShip(self.shipBodyBox2D, self.boosting, self.boostForce, self.shipBasePoint)
            self.reverseThrust(screen, self.shipBodyBox2D, self.antiThrustRange, self.antiThrustForce, self.shipBasePoint)
            self.capSpeed(self.shipBodyBox2D)
        warpBox2DObject(self.shipBodyBox2D)   
        
        shipPosition = toPixelPos(self.shipBodyBox2D.position, WSCALE, HEIGHT) 
        shipPosition = tuple(map(self.camera.watch, shipPosition))
        
        self.angleRad = self.shipBodyBox2D.angle
        self.image = pygame.transform.rotate(self.shipSurface, math.degrees(self.angleRad - math.pi))
        rect = self.image.get_rect(center=shipPosition)
        screen.blit(self.image, rect.topleft)  
        
        
        if self.debugDraw:
            debugDrawBox2DBodies(screen, self.box2DBodiesDebugList)
        
        
        
    def capSpeed(self, shipBody):
        velocity = shipBody.linearVelocity
        velocityMagnitude = velocity.length
        
        if velocityMagnitude > self.MAXSPEED:
            velocity.Normalize()
            velocity *= self.MAXSPEED
            
        shipBody.linearVelocity = velocity
            
   
    def boostShip(self, shipBody:Box2D.b2Body, boosting:bool, boostForce:int, shipBasePoint:float):
        if boosting == False:
            return
        
        angleRad = shipBody.angle
        forcePoint = shipBody.GetWorldPoint((0, shipBasePoint))
        thrustVector = boostForce * toComponent(angleRad + math.pi / 2)
        shipBody.ApplyForce(thrustVector, forcePoint, True)
      
        
    def reverseThrust(self, screen, shipBody:Box2D.b2Body, antiThrustRange, antiThrustForce, shipBasePoint):
        
      
        thrustDirection = - toComponent(shipBody.angle + math.pi / 2)
        
        rayCastStart = shipBody.GetWorldPoint((0, shipBasePoint))
        rayCastEnd = rayCastStart + (antiThrustRange * thrustDirection)
        # self.debugDrawRayCast(rayCastStart, rayCastEnd, screen)
       
        rayCastCallBack = RaycastCallback()
        self.world.RayCast(rayCastCallBack, rayCastStart, rayCastEnd)
        
        rayCastHit =  rayCastCallBack.fixture and rayCastCallBack.fixture.body != self.shipBodyBox2D
        if self.boosting and rayCastHit:
           
            # apply anti thrust force
            distanceFromShip = (rayCastCallBack.point - rayCastStart).length
            antiThrustRatio = antiThrustForce * (1 - distanceFromShip / antiThrustRange)
            antiThrustMagnitude = antiThrustRatio * thrustDirection
            
            hitBody = rayCastCallBack.fixture.body
            hitBody.ApplyForce(antiThrustMagnitude, rayCastCallBack.point, True)
       
    
    def debugDrawRayCast(self, rayCastStart, rayCastEnd, screen):
        rayCastStartToPixel = toPixelPos(rayCastStart, WSCALE, HEIGHT)
        rayCastEndToPixel = toPixelPos(rayCastEnd, WSCALE, HEIGHT)
        pygame.draw.line(screen, (255, 10, 10), rayCastStartToPixel, rayCastEndToPixel)
       
        
    def steerShip(self, steering:Steering):
        self.turnForce += .2
        self.turnForce = min(self.turnForce, self.TURN_RATE)
        
        if steering == Steering.steeringRight:
            self.shipBodyBox2D.angle -= math.radians(self.turnForce)
        elif steering == Steering.steeringLeft:
            self.shipBodyBox2D.angle += math.radians(self.turnForce)
        elif steering == Steering.noSteering:
            self.turnForce = 0
    
        