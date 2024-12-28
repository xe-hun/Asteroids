
import Box2D
import pygame


# import gameObjects.asteroid as asteroid
import gameObjects as g_o

class CollisionFilter(Box2D.b2ContactFilter):
   
    def ShouldCollide(self, fixtureA, fixtureB):
        bodyA = fixtureA.body
        bodyB = fixtureB.body
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData') and \
            isinstance(bodyA.userData, g_o.asteroid.Asteroid) and isinstance(bodyB.userData, g_o.asteroid.Asteroid):
            return False
            
        return super(CollisionFilter, self).ShouldCollide(fixtureA, fixtureB)
    
    
class ContactListener(Box2D.b2ContactListener):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.impulse = 0
        
    def check_fixture_type(self, contact: Box2D.b2Contact):
        fixture_A_is_ship = isinstance(contact.fixtureA.body.userData, g_o.ship.Ship)
        fixture_B_is_ship = isinstance(contact.fixtureB.body.userData, g_o.ship.Ship)
        fixture_A_is_asteroid = isinstance(contact.fixtureA.body.userData, g_o.asteroid.Asteroid)
        fixture_B_is_asteroid = isinstance(contact.fixtureB.body.userData, g_o.asteroid.Asteroid)
        return fixture_A_is_ship, fixture_B_is_ship, fixture_A_is_asteroid, fixture_B_is_asteroid
        
    def BeginContact(self, contact:Box2D.b2Contact):
        fixture_A_is_ship, fixture_B_is_ship,\
        fixture_A_is_asteroid, fixture_B_is_asteroid = self.check_fixture_type(contact)
        
        if fixture_A_is_ship and fixture_B_is_asteroid:
            contact.fixtureA.body.userData.collision_begins()
        
        if fixture_A_is_asteroid and fixture_B_is_ship:
            contact.fixtureB.body.userData.collision_begins()
        
    
    def EndContact(self, contact:Box2D.b2Contact):
        
        fixture_A_is_ship, fixture_B_is_ship,\
        fixture_A_is_asteroid, fixture_B_is_asteroid = self.check_fixture_type(contact)
        
        if fixture_A_is_ship and fixture_B_is_asteroid:
            contact.fixtureA.body.userData.collision_ends()
        
        if fixture_A_is_asteroid and fixture_B_is_ship:
            contact.fixtureB.body.userData.collision_ends()
                
    def PostSolve(self, contact:Box2D.b2Contact, impulse:Box2D.b2ContactImpulse):
        
        fixture_A_is_ship, fixture_B_is_ship,\
        fixture_A_is_asteroid, fixture_B_is_asteroid = self.check_fixture_type(contact)
        
        if fixture_A_is_ship and fixture_B_is_asteroid:
            contact.fixtureA.body.userData.get_collision_impulse((impulse.normalImpulses[0]))
        
        if fixture_A_is_asteroid and fixture_B_is_ship:
            contact.fixtureB.body.userData.get_collision_impulse((impulse.normalImpulses[0]))
               
                
                
                
    # def EndContact(self, contact:Box2D.b2Contact):
        
    #     if isinstance(contact.fixtureA.body.userData, g_o.ship.Ship) and\
    #         isinstance(contact.fixtureB.body.userData, g_o.asteroid.Asteroid):
    #             # data = (contact.fixtureB.body.userData, impulse.normalImpulses[0])
    #             data = 0
    #             pygame.event.post(pygame.event.Event(SHAKE_EVENT, data = data))
    #             print(self.impulse)

    #     elif isinstance(contact.fixtureA.body.userData, g_o.asteroid.Asteroid) and\
    #         isinstance(contact.fixtureB.body.userData, g_o.ship.Ship):
    #             data = 0
    #             # data = (contact.fixtureA.body.userData, impulse.normalImpulses[0])
    #             pygame.event.post(pygame.event.Event(SHAKE_EVENT, data = data))    
    #             print(self.impulse) 
                
    # def PostSolve(self, contact:Box2D.b2Contact, impulse:Box2D.b2ContactImpulse):
        
    #       if isinstance(contact.fixtureA.body.userData, g_o.ship.Ship) and\
    #         isinstance(contact.fixtureB.body.userData, g_o.asteroid.Asteroid)\
    #            or isinstance(contact.fixtureA.body.userData, g_o.asteroid.Asteroid) and\
    #         isinstance(contact.fixtureB.body.userData, g_o.ship.Ship):
    #             self.impulse = impulse.normalImpulses
                
                
                
                # def EndContact(self, contact):
    #     if isinstance(contact.fixtureA.body.userData, g_o.ship.Ship) and\
    #         isinstance(contact.fixtureB.body.userData, g_o.asteroid.Asteroid):
    #             # Box2D.b2Contact().
    #             pygame.event.post(pygame.event.Event(SHAKE_EVENT, data = contact.fixtureB.body.userData))

    #     elif isinstance(contact.fixtureA.body.userData, g_o.asteroid.Asteroid) and\
    #         isinstance(contact.fixtureB.body.userData, g_o.ship.Ship):
    #             pygame.event.post(pygame.event.Event(SHAKE_EVENT, data = contact.fixtureA.body.userData))
    
    
    
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