import Box2D as box2D

import pygame


class Test():
    def __init__(self) -> None:
        # create the world
        self.world = box2D.b2World(gravity=(0, -10), doSleep=True)
        
        # Create ground
        ground_body = self.world.CreateStaticBody(
            position = (0, -10),
            shapes=box2D.polygonShape(box =  (50, 5))
        )
        
        dynamic_body = self.world.CreateDynamicBody(
            position=(10, 15)
        )
        
        box = dynamic_body.CreatePolygonFixture(box=(2,1), density=1, friction=.3)
        
        # # Create a dynamic body
        # body_def = box2D.b2BodyDef()
        # body_def.type = box2D.b2_dynamicBody
        # body_def.position = (0, 4)
        # # body_def.fixedRotation = True
        # body = self.world.CreateBody(body_def)
        
        # # create a box shape
        # box_shape = box2D.b2PolygonShape()
        # box_shape.SetAsBox(1, 1)
       
        
       
        
        # create a fixture
        
        # fixture = body.CreateFixture(shape=box_shape, density = 1, friction = .3)
    
    def update(self, screen:pygame.surface.Surface):
        vel_iterations = 10
        pos_iterations = 10
        self.world.Step(1.0/60, vel_iterations, pos_iterations)
        
        