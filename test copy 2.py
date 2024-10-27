from enum import Enum
import math
import Box2D as box2D

import numpy as np
import pygame

from constant import HEIGHT, WIDTH, fill_color, outline_color
from utils.helper import WHToPixel, v_to_component, to_pixel_position, to_box2D_position

class Steering(Enum):
    steeringLeft = 1
    steeringRight = 2
    noSteering = 3


class Test():
    def __init__(self) -> None:
        
        # --- Box2D setup ---
        # Box2D works in meters, so we need a conversion factor:
        self.PPM = 20.0  # pixels per meter
        self.TARGET_FPS = 60
        self.TIME_STEP = 1.0 / self.TARGET_FPS
        self.VELOCITY_ITERATIONS = 10
        self.POSITION_ITERATIONS = 10
        
        # create the world
        self.world = box2D.b2World(gravity=(0, 0), doSleep=True)
        
        # Create ground
        # self.groundBody = self.world.CreateStaticBody(
        #     position = (0, 1),
        #     shapes=box2D.b2PolygonShape(box =  (50, 5))
        # )
        
      
        self.mouseJoint = None
        
        self.boxSurface = pygame.Surface(( WHToPixel(2, 1, self.PPM)), pygame.SRCALPHA)
        pygame.draw.rect(self.boxSurface, (0, 0, 255), (0, 0,  *WHToPixel(2, 1, self.PPM)))
        
        self.createShipPygame()
        self.createShipBox()
        self.creatAsteroidPygame()
        
    def createShipPygame(self):
        
        self.steering = Steering.noSteering
        self.shipAngleRad = 0
        self.boosting = False
        self.xPos = WIDTH // 2
        self.yPos = HEIGHT // 2
        self.shipWidth = 30
        self.shipHeight = 40
        polygonPoints =  ((0,0),
                          (7, 5),
                          (15, 0),
                          (23, 5),
                          (30, 0),
                          (15, 40))
        
        self.shipSurface = pygame.Surface((self.shipWidth + 2, self.shipHeight + 2), pygame.SRCALPHA)
        pygame.draw.polygon(self.shipSurface, fill_color, polygonPoints)
        pygame.draw.polygon(self.shipSurface, outline_color, polygonPoints, 2)
        self.shipRect = self.shipSurface.get_rect(center=(self.xPos, self.yPos))
       
        
    def createShipBox(self):
        
        # self.circleBody = self.world.CreateDynamicBody(position = (0,0))
        # circleShape = box2D.b2CircleShape(5/self.PPM)
        # self.circleBody.Createfixture(shape = circleShape, density = 1, friction = .3)
        
        centerPos = to_box2D_position((WIDTH / 2, HEIGHT/2), self.PPM, HEIGHT)
        polygonPointsPixel1 = ((0, 0), (7, 5), (15, 40))
        polygonPointsPixel2 = ((7, 5), (15, 0), (23, 5), (15, 40))
        polygonPointsPixel3 = ( (23, 5),(30, 0),(15, 40))
        polygonPointsWorld1 = [((i[0] - 15)/self.PPM, (i[1]-20)/self.PPM) for i in polygonPointsPixel1]
        polygonPointsWorld2 = [((i[0] - 15)/self.PPM, (i[1]-20)/self.PPM) for i in polygonPointsPixel2]
        polygonPointsWorld3 = [((i[0] - 15)/self.PPM, (i[1]-20)/self.PPM) for i in polygonPointsPixel3]
       
        
        
        self.shipBody = self.world.CreateDynamicBody(position=box2D.b2Vec2(centerPos))
        polygonShape1 = box2D.b2.polygonShape(vertices = polygonPointsWorld1)
        polygonShape2 = box2D.b2PolygonShape(vertices = polygonPointsWorld2)
        polygonShape3 = box2D.b2.polygonShape(vertices = polygonPointsWorld3)
        
     
        
        self.shipBody.CreateFixture(
            shape = polygonShape1,
            density = 1,
            friction = .3
        )
        
        self.shipBody.CreateFixture(
            shape = polygonShape2,
            density = 1,
            friction = .3
        )
        
        self.shipBody.CreateFixture(
            shape = polygonShape3,
            density = 1,
            friction = .3
        )
        
        self.shipBody.fixedRotation = True
        
        
        # self.dynamicBoxBody = self.world.CreateDynamicBody(
        #     position=(10, 15)
        # )
        
        # self.dynamic_body_fixture = self.dynamicBoxBody.CreatePolygonFixture(box=(2,1), density=1, friction=.3)
        
        
    def creatAsteroidPygame(self):
        asteroidHalfSizeSize = np.random.randint(35, 45)
        # asteroidHalfSizeSize = 40
        # numSide = np.random.randint(MIN_SIDES, MAX_SIDES)
        numSide = np.random.randint(5, 12)
      
        
        # map the asteroid life according to its size
        # self.asteroidLife = int(mapValue(MIN_SIZE, MAX_SIZE, MIN_LIFE, MAX_LIFE, asteroidHalfSizeSize))
        # self.asteroidLife = 4
        # print(self.asteroidLife)


        pertubations = [(np.random.randint(0, 10), np.random.randint(0, 10)) for _ in range(numSide)]
        polyAngles = [np.random.randn() * .05 + x for x in np.linspace(0, math.pi * 2 , numSide)]
        stroke = 2
        
        polygonPoints =  [((asteroidHalfSizeSize - pertubations[i][0]) * math.cos(j) + asteroidHalfSizeSize, (asteroidHalfSizeSize - pertubations[i][1]) * math.sin(j) + asteroidHalfSizeSize) for i, j in enumerate(polyAngles) if i < numSide - 1]
        
        self.asteroidSurface = pygame.Surface((asteroidHalfSizeSize * 2 + stroke , asteroidHalfSizeSize * 2 + stroke), pygame.SRCALPHA)
        pygame.draw.polygon(self.asteroidSurface, fill_color, polygonPoints)
        pygame.draw.polygon(self.asteroidSurface, outline_color, polygonPoints, stroke)
        
        self.asteroidBox2DBody = self.world.CreateDynamicBody(
            position = to_box2D_position((WIDTH / 5, HEIGHT / 5), self.PPM, HEIGHT)
        )
        asteroidShape = box2D.b2PolygonShape(vertices = [ (-(i[0] - asteroidHalfSizeSize) / self.PPM, (i[1] - asteroidHalfSizeSize) / self.PPM) for i in polygonPoints])
        self.asteroidBox2DBody.CreateFixture(
            shape = asteroidShape,
            density = 1,
            friction = .3,
            
        )
        
        
    # def createAsteroidBox2D(self):
    #     asteroidHalfSizeSize = np.random.randint(35, 45)
    #     # asteroidHalfSizeSize = 40
    #     # numSide = np.random.randint(MIN_SIDES, MAX_SIDES)
    #     numSide = np.random.randint(5, 12)
        
    #     # map the asteroid life according to its size
    #     # self.asteroidLife = int(mapValue(MIN_SIZE, MAX_SIZE, MIN_LIFE, MAX_LIFE, asteroidHalfSizeSize))
    #     # self.asteroidLife = 4
    #     # print(self.asteroidLife)


    #     pertubations = [(np.random.randint(0, 10), np.random.randint(0, 10)) for _ in range(numSide)]
    #     polyAngles = [np.random.randn() * .05 + x for x in np.linspace(0, math.pi * 2 , numSide)]
    #     stroke = 2
        
    #     polygonPoints =  [((asteroidHalfSizeSize - pertubations[i][0]) * math.cos(j) + asteroidHalfSizeSize, (asteroidHalfSizeSize - pertubations[i][1]) * math.sin(j) + asteroidHalfSizeSize) for i, j in enumerate(polyAngles) if i < numSide - 1]
        
          
        
       
    def update(self, screen:pygame.surface.Surface):

        self.world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        
        if self.mouseJoint:
            mouseToWorldPosition = to_box2D_position(pygame.mouse.get_pos(), self.PPM, HEIGHT)
            self.mouseJoint.target = mouseToWorldPosition
            
        self.warpShipInWorld(self.shipBody)
        
        if self.boosting:
            self.boostShip()
        
        self.steerShip()
        self.capSpeed()
        # print(self.steering)
        
      
        
        
        # boxAngle = self.dynamicBoxBody.angle
        # boxSurfaceR = pygame.transform.rotate(self.boxSurface, math.degrees(boxAngle))
        # boxRect = boxSurfaceR.get_rect(center=toPixelPos(boxPosition, self.PPM, HEIGHT))
        # screen.blit(boxSurfaceR, boxRect.topleft)
        
        # screen.blit(self.shipSurface, self.shipRect)
        
        
       
        
        
        #   # Render dynamic body
        # for fixture in self.dynamicBoxBody.fixtures:
        #     shape = fixture.shape
        #     vertices = [(self.dynamicBoxBody.transform * v) * self.PPM for v in shape.vertices]
        #     vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
        #     pygame.draw.polygon(screen, (255, 0, 0), vertices)
            
          
        shipPosition = self.shipBody.position
        shipAngle = self.shipBody.angle - math.pi
        shipSurfaceR = pygame.transform.rotate(self.shipSurface, math.degrees(shipAngle))
        shipRect = shipSurfaceR.get_rect(center=to_pixel_position(shipPosition, self.PPM, HEIGHT))
        screen.blit(shipSurfaceR, shipRect.topleft)
        
        asteroidPosition = self.asteroidBox2DBody.position
        asteroidAngle = self.asteroidBox2DBody.angle - math.pi
        asteroidSurfaceR = pygame.transform.rotate(self.asteroidSurface, math.degrees(asteroidAngle))
        asteroidRect = asteroidSurfaceR.get_rect(center=to_pixel_position(asteroidPosition, self.PPM, HEIGHT))
        screen.blit(asteroidSurfaceR, asteroidRect.topleft)
        
        
           #   # Render dynamic body
        for fixture in self.asteroidBox2DBody.fixtures:
            shape = fixture.shape
            vertices = [(self.asteroidBox2DBody.transform * v) * self.PPM for v in shape.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, (180, 100, 10,), vertices)
            
     
            
        
          
        #    # Render ship body
        # for fixture in self.shipBody.fixtures:
        #     shape = fixture.shape
        #     vertices = [(self.shipBody.transform * v) * self.PPM for v in shape.vertices]
        #     vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
        #     pygame.draw.polygon(screen, (90, 100, 10), vertices)
            
        # pygame.draw.circle(screen, (255, 100, 0), tuple(toPixelPos(self.shipBody.GetWorldPoint((0, 0)), self.PPM, HEIGHT)), 5)
        forcePoint = self.shipBody.GetWorldPoint((0, -15/self.PPM))
        forceVector = v_to_component(self.shipBody.angle + math.pi / 2)
        p = to_pixel_position(forcePoint, self.PPM, HEIGHT)
        # pygame.draw.line(screen, (40, 200, 0), p, (p + np.array(forceVector) * self.PPM * 2) , 2)

            
    def steerShip(self):
        if self.steering == Steering.steeringRight:
            self.shipBody.angle -= math.radians(3)
        elif self.steering == Steering.steeringLeft:
            self.shipBody.angle += math.radians(3)
            
    def capSpeed(self):
        maxVelocity = 10
        # self.shipBody.linearVelocity(self.shipBody.linearVelocity.Clamp(maxVelocity))
        velocity = self.shipBody.linearVelocity
        velocityMagnitude = velocity.length
        
        if velocityMagnitude > maxVelocity:
            velocity.Normalize()
            velocity *= maxVelocity
            
        self.shipBody.linearVelocity = velocity
            
        # box2D.b2Vec2.norm
            
        
            
   
   
    def boostShip(self):
        maxVelocity = 5
        forcePoint = self.shipBody.GetWorldPoint((0, -15/self.PPM))
        forceVector = 8 * v_to_component(self.shipBody.angle + math.pi / 2)
        
      

        self.shipBody.ApplyForce(forceVector, forcePoint, True)
        
        
    def warpShipInWorld(self, body:box2D.b2Body):
        left, top, right, bottom = self.getBodyBounds(body)
        
        position = body.position
        bodyWidth = right - left
        bodyHeight = top - bottom
        if right < 0:
            body.position = ((WIDTH - 1) / self.PPM + (bodyWidth ) / 2, position.y)
        elif left > WIDTH/self.PPM:
            body.position = ((-bodyWidth + 1)/ 2, position.y)
        
        if top < 0:
            body.position = (position.x, (HEIGHT - 1) / self.PPM + (bodyHeight) / 2)
        elif bottom > HEIGHT / self.PPM:
            body.position = (position.x, (-bodyHeight + 1) / 2)


        
    def getBodyBounds(self, body:box2D.b2Body):
        # body = fixture.body
        bounds = [fixture.shape.getAABB(body.transform, 0) for fixture in body.fixtures]
        left = min(bound.lowerBound.x for bound in bounds)
        right = max(bound.upperBound.x for bound in bounds)
        top = max(bound.upperBound.y for bound in bounds)
        bottom = min(bound.lowerBound.y for bound in bounds)
        return (left, top, right, bottom)
        
    def handleEvent(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseToWorldPosition = to_box2D_position(event.pos, self.PPM, HEIGHT)
            if self.pointInBody(self.shipBody, mouseToWorldPosition):
                mouseJointDef = box2D.b2MouseJointDef()
                # mouseJointDef.bodyA = self.groundBody
                mouseJointDef.bodyA = self.world.CreateBody()
                mouseJointDef.bodyB = self.shipBody
                mouseJointDef.target = mouseToWorldPosition
                mouseJointDef.maxForce = 1000.0 * self.shipBody.mass
                self.mouseJoint = self.world.CreateJoint(mouseJointDef)
                
            #   keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_DOWN:
                self.boosting = True
            if event.key == pygame.K_LEFT:
                self.steering = Steering.steeringLeft
            if event.key == pygame.K_RIGHT:
                self.steering = Steering.steeringRight
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.boosting = False
            if event.key == pygame.K_LEFT and self.steering == Steering.steeringLeft:
                self.steering = Steering.noSteering
            if event.key == pygame.K_RIGHT and self.steering == Steering.steeringRight:
                self.steering = Steering.noSteering
                
                
        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouseJoint:
                self.world.DestroyJoint(self.mouseJoint)
                self.mouseJoint = None
                
    def pointInBody(self, body:box2D.b2Body, point):
        for fixture in body.fixtures:
            if fixture.TestPoint(point):
                return True
            
        return False
                    
   
        
            
        
        