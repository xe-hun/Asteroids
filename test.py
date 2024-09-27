import math
import Box2D as box2D

import numpy as np
import pygame

from constant import HEIGHT, WIDTH, fillColor, outlineColor
from utils.helper import WHToPixel, toPixelPos, toWorldPos


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
        # self.mouse_world_pos = None
        
        self.boxSurface = pygame.Surface(( WHToPixel(2, 1, self.PPM)), pygame.SRCALPHA)
        pygame.draw.rect(self.boxSurface, (0, 0, 255), (0, 0,  *WHToPixel(2, 1, self.PPM)))
        
        self.createShipPygame()
        self.createShipBox()
        
    def createShipPygame(self):
        
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
        pygame.draw.polygon(self.shipSurface, fillColor, polygonPoints)
        pygame.draw.polygon(self.shipSurface, outlineColor, polygonPoints, 2)
        # self.shipSurface = pygame.transform.rotate(self.shipSurface, 90)
        self.shipRect = self.shipSurface.get_rect(center=(self.xPos, self.yPos))
        self.image = self.shipSurface
        
    def createShipBox(self):
        centerPos = toWorldPos((WIDTH / 2, HEIGHT/2), self.PPM, HEIGHT)
        polygonPointsPixel1 = ((0, 0), (7, 5), (15, 40))
        polygonPointsPixel2 = ((7, 5), (15, 0), (23, 5), (15, 40))
        polygonPointsPixel3 = ( (23, 5),(30, 0),(15, 40))
        polygonPointsWorld1 = [(x[0]/self.PPM, x[1]/self.PPM) for x in polygonPointsPixel1]
        # polygonPointsWorld2 = [toWorldPos(x, self.PPM, HEIGHT).tolist() for x in polygonPointsPixel2]
        polygonPointsWorld2 = [(x[0]/self.PPM, x[1]/self.PPM) for x in polygonPointsPixel2]
        polygonPointsWorld3 = [(x[0]/self.PPM, x[1]/self.PPM) for x in polygonPointsPixel3]
       
        
        
        self.shipBody = self.world.CreateDynamicBody(position=box2D.b2Vec2(centerPos))
        self.polygonShape1 = box2D.b2.polygonShape(vertices = polygonPointsWorld1)
        self.polygonShape2 = box2D.b2PolygonShape(vertices = polygonPointsWorld2)
        self.polygonShape3 = box2D.b2.polygonShape(vertices = polygonPointsWorld3)
        
        # shipBodyDef = box2D.b2BodyDef()
        # shipBodyDef.type = box2D.b2_dynamicBody
        # shipBodyDef.position = (10, 10)
        # self.shipBody = self.world.CreateBody(shipBodyDef)
        
        # shipFixture1 = box2D.b2FixtureDef()
        # shipFixture1.shape = self.polygonShape2
        # shipFixture1.density = 1.0
        # shipFixture1.friction = .3
        
        
        
        # self.shipBody.CreateFixture(shipFixture1)
        
        
        self.shipBody.CreateFixture(
            shape = self.polygonShape1,
            density = 1,
            friction = .3
        )
        
        self.shipBody.CreateFixture(
            shape = self.polygonShape2,
            density = 1,
            friction = .3
        )
        
        self.shipBody.CreateFixture(
            shape = self.polygonShape3,
            density = 1,
            friction = .3
        )
        
        
        # self.dynamicBoxBody = self.world.CreateDynamicBody(
        #     position=(10, 15)
        # )
        
        # self.dynamic_body_fixture = self.dynamicBoxBody.CreatePolygonFixture(box=(2,1), density=1, friction=.3)
        
        
        
          
        
       
    def update(self, screen:pygame.surface.Surface):

        self.world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        
        if self.mouseJoint:
            mouseToWorldPosition = toWorldPos(pygame.mouse.get_pos(), self.PPM, HEIGHT)
            self.mouseJoint.target = mouseToWorldPosition
            
        # self.warpShipInWorld(self.shipBody)

        
        # for fixture in self.groundBody.fixtures:
        #     shape = fixture.shape
        #     vertices = [(self.groundBody.transform * v) * self.PPM \
        #         for v in shape.vertices]
        #     vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
        #     pygame.draw.polygon(screen, (0, 225, 0), vertices)
           
        
        # boxPosition = self.dynamicBoxBody.position
        
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
            
          
           # Render ship body
        for fixture in self.shipBody.fixtures:
            shape = fixture.shape
            vertices = [(self.shipBody.transform * v) * self.PPM for v in shape.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, (111, 255, 255), vertices)
            
        # print(self.shipBody.transform.position[1])
        print(self.shipBody.position)
        
        
        shipPosition = self.shipBody.position
        shipAngle = self.shipBody.angle
        shipSurfaceR = pygame.transform.rotate(self.shipSurface, math.degrees(shipAngle))
        shipRect = shipSurfaceR.get_rect(center=toPixelPos(shipPosition, self.PPM, HEIGHT))
        screen.blit(shipSurfaceR, shipRect.topleft)
        
        # screen.blit(self.shipSurface, self.shipRect)
        
    def warpShipInWorld(self, body:box2D.b2Body):
        left, top, right, bottom = self.getBodyBounds(body)
        
        position = body.position
        bodyWidth = right - left
        bodyHeight = bottom - top
        # if right < 0:
        if position.x < 0:
            # body.position = (WIDTH / self.PPM + (bodyWidth) / 2, position.y)
            body.position = (WIDTH / self.PPM, position.y)
        # elif left > WIDTH/self.PPM:
        elif position.x > WIDTH/self.PPM:
            # body.position = (-bodyWidth / 2, position.y)
            body.position = (0, position.y)
        
        # if bottom < 0:
        if position.y < 0:
            # body.position = (position.x, HEIGHT / self.PPM + (bodyHeight) / 2)
            body.position = (position.x, HEIGHT / self.PPM)
        # elif top > HEIGHT / self.PPM:
        elif position.y > HEIGHT / self.PPM:
            # body.position = (position.x, -bodyHeight / 2)
            body.position = (position.x, 0)

        
    # def getBodyBounds(self, fixture):
    #     body = fixture.body
    #     vertices = [body.transform * v for v in body.shape.vertices]
    #     xCoords = [v[0] for v in vertices]
    #     yCoords = [v[1] for v in vertices]
    #     return (min(xCoords), min(yCoords), max(xCoords), max(yCoords))
        
        
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
            mouseToWorldPosition = toWorldPos(event.pos, self.PPM, HEIGHT)
            if self.pointInBody(self.shipBody, mouseToWorldPosition):
                mouseJointDef = box2D.b2MouseJointDef()
                # mouseJointDef.bodyA = self.groundBody
                mouseJointDef.bodyA = self.world.CreateBody()
                mouseJointDef.bodyB = self.shipBody
                mouseJointDef.target = mouseToWorldPosition
                mouseJointDef.maxForce = 1000.0 * self.shipBody.mass
                self.mouseJoint = self.world.CreateJoint(mouseJointDef)
                    
        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouseJoint:
                self.world.DestroyJoint(self.mouseJoint)
                self.mouseJoint = None
                
    def pointInBody(self, body:box2D.b2Body, point):
        for fixture in body.fixtures:
            if fixture.TestPoint(point):
                return True
            
        return False
                    
   
        
            
        
        