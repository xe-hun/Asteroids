
import Box2D


# import gameObjects.asteroid as asteroid
import gameObjects as g_o


class Box2DHelperClass():
    def __init__(self):
        pass
    
    
    _box2DWorld:Box2D.b2World = None
    
    def init_world():
        
        Box2DHelperClass.dispose_world()
        world = Box2D.b2World((0, 0), doSleep=True)
        world.contactFilter = _CollisionFilter()
        world.contactListener = _ContactListener()
        
        Box2DHelperClass._box2DWorld = world
        return world
    
    def dispose_world():
        world = Box2DHelperClass._box2DWorld
        if world is not None:
            for body in world.bodies:
                world.DestroyBody(body)
        
        Box2DHelperClass._box2DWorld = world = None
        
        
        


class _CollisionFilter(Box2D.b2ContactFilter):
   
    def ShouldCollide(self, fixtureA, fixtureB):
        bodyA = fixtureA.body
        bodyB = fixtureB.body
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData') and \
            isinstance(bodyA.userData, g_o.asteroid.Asteroid) and isinstance(bodyB.userData, g_o.asteroid.Asteroid):
            return False
            
        return super(_CollisionFilter, self).ShouldCollide(fixtureA, fixtureB)
    
    
class _ContactListener(Box2D.b2ContactListener):
    
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