import math
import Box2D as box2D

import pygame

from constant import HEIGHT
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
        self.world = box2D.b2World(gravity=(0, -10), doSleep=True)
        
        # Create ground
        self.ground_body = self.world.CreateStaticBody(
            position = (0, 1),
            shapes=box2D.b2PolygonShape(box =  (50, 5))
        )
        
        self.dynamicBody = self.world.CreateDynamicBody(
            position=(10, 15)
        )
        
        self.dynamic_body_fixture = self.dynamicBody.CreatePolygonFixture(box=(2,1), density=1, friction=.3)
        
        self.mouseJoint = None
        # self.mouse_world_pos = None
        
        self.bodySurface = pygame.Surface(( WHToPixel(2, 1, self.PPM)), pygame.SRCALPHA)
        pygame.draw.rect(self.bodySurface, (0, 0, 255), (0, 0,  *WHToPixel(2, 1, self.PPM)))
        
       
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
           
        
          # Render dynamic body
        for fixture in self.dynamicBody.fixtures:
            shape = fixture.shape
            vertices = [(self.dynamicBody.transform * v) * self.PPM for v in shape.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, (255, 0, 0), vertices)
        
           
        position = self.dynamicBody.position
        angle = self.dynamicBody.angle
        bodySurfaceR = pygame.transform.rotate(self.bodySurface, math.degrees(angle))
        rect = bodySurfaceR.get_rect(center=toPixelPos(position, self.PPM, HEIGHT))
        screen.blit(bodySurfaceR, rect.topleft)
        
         
        
    def handleEvent(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print('zintol')
            mouseToWorldPosition = toWorldPos(event.pos, self.PPM, HEIGHT)
            if self.dynamic_body_fixture.GetAABB(0).lowerBound.x <= mouseToWorldPosition[0] <= self.dynamic_body_fixture.GetAABB(0).upperBound.x and \
                self.dynamic_body_fixture.GetAABB(0).lowerBound.y <= mouseToWorldPosition[1] <= self.dynamic_body_fixture.GetAABB(0).upperBound.y:
                    
                    mouseJointDef = box2D.b2MouseJointDef()
                    mouseJointDef.bodyA = self.world.CreateBody()
                    mouseJointDef.bodyB = self.dynamicBody
                    mouseJointDef.target = mouseToWorldPosition
                    # box2D.b2Body.m
                    mouseJointDef.maxForce = 1000.0 * self.dynamicBody.mass
                    self.mouseJoint = self.world.CreateJoint(mouseJointDef)
                    
        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouseJoint:
                self.world.DestroyJoint(self.mouseJoint)
                self.mouseJoint = None
                    
                    
    # def getAABB(self, body:box2D.b2Fixture)->box2D.b2AABB:
    #     aabb = box2D.b2AABB()
    #     for fixture in body.fixtures:
    #         aabb.Combine(aabb, fixture.GetAABB(0))

    #     return aabb
        
        
   
    
   
        
            
        
        