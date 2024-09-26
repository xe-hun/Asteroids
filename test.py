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
        self.ground_body = self.world.CreateStaticBody(
            position = (0, 1),
            shapes=box2D.b2PolygonShape(box =  (50, 5))
        )
        
        self.dynamicBoxBody = self.world.CreateDynamicBody(
            position=(10, 15)
        )
        
        self.dynamic_body_fixture = self.dynamicBoxBody.CreatePolygonFixture(box=(2,1), density=1, friction=.3)
        
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
        centerPos = toWorldPos((WIDTH / 2, HEIGHT), self.PPM, HEIGHT)
        polygonPointsPixel1 = ((0, 0), (7, 5), (15, 40))
        polygonPointsPixel2 = ((7, 5), (15, 0), (23, 5), (15, 40))
        polygonPointsPixel3 = ( (23, 5),(30, 0),(15, 40))
        polygonPointsWorld1 = [toWorldPos(x, self.PPM, HEIGHT).tolist() for x in polygonPointsPixel1]
        polygonPointsWorld2 = [toWorldPos(x, self.PPM, HEIGHT).tolist() for x in polygonPointsPixel2]
        polygonPointsWorld3 = [toWorldPos(x, self.PPM, HEIGHT).tolist() for x in polygonPointsPixel3]
       
        
        
        self.shipBody = self.world.CreateDynamicBody(position=centerPos)
        self.polygonShape1 = box2D.b2.polygonShape(vertices = polygonPointsWorld1)
        self.polygonShape2 = box2D.b2.polygonShape(vertices = polygonPointsWorld2)
        self.polygonShape3 = box2D.b2.polygonShape(vertices = polygonPointsWorld3)
        
        self.shipBodyFixture = self.shipBody.CreateFixture(
            shape = self.polygonShape1,
            density = 1,
            friction = .3
        )
        
        self.shipBodyFixture = self.shipBody.CreateFixture(
            shape = self.polygonShape2,
            density = 1,
            friction = .3
        )
        
        self.shipBodyFixture = self.shipBody.CreateFixture(
            shape = self.polygonShape3,
            density = 1,
            friction = .3
        )
        
        
          
        
       
    def update(self, screen:pygame.surface.Surface):

        self.world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        
        if self.mouseJoint:
            mouseToWorldPosition = toWorldPos(pygame.mouse.get_pos(), self.PPM, HEIGHT)
            self.mouseJoint.target = mouseToWorldPosition

        
        for fixture in self.ground_body.fixtures:
            shape = fixture.shape
            vertices = [(self.ground_body.transform * v) * self.PPM \
                for v in shape.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, (0, 225, 0), vertices)
           
        
        #   # Render dynamic body
        # for fixture in self.dynamicBoxBody.fixtures:
        #     shape = fixture.shape
        #     vertices = [(self.dynamicBoxBody.transform * v) * self.PPM for v in shape.vertices]
        #     vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
        #     pygame.draw.polygon(screen, (255, 0, 0), vertices)
            
        boxPosition = self.dynamicBoxBody.position
        
        boxAngle = self.dynamicBoxBody.angle
        boxSurfaceR = pygame.transform.rotate(self.boxSurface, math.degrees(boxAngle))
        boxRect = boxSurfaceR.get_rect(center=toPixelPos(boxPosition, self.PPM, HEIGHT))
        screen.blit(boxSurfaceR, boxRect.topleft)
        
        # screen.blit(self.shipSurface, self.shipRect)
        
          
           # Render ship body
        for fixture in self.shipBody.fixtures:
            shape = fixture.shape
            vertices = [(self.shipBody.transform * v) * self.PPM for v in shape.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, (111, 255, 255), vertices)
        
        
        shipPosition = self.shipBody.worldCenter
        shipAngle = self.shipBody.angle
        shipSurfaceR = pygame.transform.rotate(self.shipSurface, math.degrees(shipAngle))
        shipRect = shipSurfaceR.get_rect(center=toPixelPos(shipPosition, self.PPM, HEIGHT))
        screen.blit(shipSurfaceR, shipRect.topleft)
        
        # screen.blit(self.shipSurface, self.shipRect)
        
         
        
    def handleEvent(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print('zintol')
            mouseToWorldPosition = toWorldPos(event.pos, self.PPM, HEIGHT)
            if self.getAABB(self.shipBody).lowerBound.x <= mouseToWorldPosition[0] <= self.getAABB(self.shipBody).upperBound.x and \
                self.getAABB(self.shipBody).lowerBound.y <= mouseToWorldPosition[1] <= self.getAABB(self.shipBody).upperBound.y:
            # if self.dynamic_body_fixture.GetAABB(0).lowerBound.x <= mouseToWorldPosition[0] <= self.dynamic_body_fixture.GetAABB(0).upperBound.x and \
            #     self.dynamic_body_fixture.GetAABB(0).lowerBound.y <= mouseToWorldPosition[1] <= self.dynamic_body_fixture.GetAABB(0).upperBound.y:
                    
                    mouseJointDef = box2D.b2MouseJointDef()
                    mouseJointDef.bodyA = self.world.CreateBody()
                    mouseJointDef.bodyB = self.dynamicBoxBody
                    mouseJointDef.target = mouseToWorldPosition
                    # box2D.b2Body.m
                    mouseJointDef.maxForce = 1000.0 * self.dynamicBoxBody.mass
                    self.mouseJoint = self.world.CreateJoint(mouseJointDef)
                    
        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouseJoint:
                self.world.DestroyJoint(self.mouseJoint)
                self.mouseJoint = None
                    
                    
    def getAABB(self, body:box2D.b2Body)->box2D.b2AABB:
        aabb = box2D.b2AABB()
        transform = body.transform
        for fixture in body.fixtures:
            shape = fixture.shape
            
            # if isinstance(shape, box2D.b2CircleShape):
            #     aabb.Combine(aabb, box2D.b2AABB(lowerBound=(shape.pos - (shape.radius, shape.radius)), 
            #                                 upperBound=(shape.pos + (shape.radius, shape.radius))))
            # else:
            
            aabb.Combine(aabb, shape.getAABB(0))
            # width = aabb.upperBound.x - aabb.lowerBound.x
            # height = aabb.upperBound.y - aabb.lowerBound.y
            # return width, height
            # aabb.Combine(aabb, fixture.GetAABB(0))

        return aabb
        
        
   
    
   
        
            
        
        