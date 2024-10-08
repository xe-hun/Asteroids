
import Box2D
import pygame

from constant import BOX2D_ASTEROID_USER_DATA, BOX2D_SHIP_USER_DATA, SHAKE_EVENT

class CollisionFilter(Box2D.b2ContactFilter):
   
    def ShouldCollide(self, fixtureA, fixtureB):
        bodyA = fixtureA.body
        bodyB = fixtureB.body
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData') and \
            bodyA.userData == BOX2D_ASTEROID_USER_DATA and bodyB.userData == BOX2D_ASTEROID_USER_DATA:
            return False
            
        return super(CollisionFilter, self).ShouldCollide(fixtureA, fixtureB)
    
    
class ContactListener(Box2D.b2ContactListener):
    def EndContact(self, contact):
        if contact.fixtureA.body.userData == BOX2D_SHIP_USER_DATA and\
            contact.fixtureB.body.userData == BOX2D_ASTEROID_USER_DATA or\
                contact.fixtureA.body.userData == BOX2D_ASTEROID_USER_DATA and\
            contact.fixtureB.body.userData == BOX2D_SHIP_USER_DATA:
                pygame.event.post(pygame.event.Event(SHAKE_EVENT))
    
    
    
class RaycastCallback(Box2D.b2RayCastCallback):
    def __init__(self):
        Box2D.b2RayCastCallback.__init__(self)
        self.fixture = None
        self.point = None
        self.normal = None
        self.fraction = 1.0
        
    def ReportFixture(self, fixture, point, normal, fraction):
        if fraction < self.fraction:
            self.fixture = fixture
            self.point = Box2D.b2Vec2(point)
            self.normal = Box2D.b2Vec2(normal)
            self.fraction = fraction
        return 1.0