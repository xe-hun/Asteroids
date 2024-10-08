import numpy as np
import pygame
import Box2D
from gameStateController import GameStateController
from utils.shake import Shake
from utils.box2DHelperClasses import CollisionFilter, ContactListener
from gameObjects.asteroid import Asteroid
from gameObjects.cannon import Cannon
from constant import MAX_ASTEROID_ON_SCREEN, MAX_ASTEROID_PER_LEVEL, SHAKE_DURATION, SHAKE_FREQUENCY, SHAKE_INTENSITY, WIDTH, HEIGHT, WSCALE, outlineColor, backgroundColor, FPS
from pages.hud import Hud
from gameObjects.ship import Ship


class Game():
    
    def __init__(self, controller:GameStateController):
        
        self.controller = controller
        self.hud = Hud(controller.getLevel())
        
        self.VELOCITY_ITERATIONS = 10
        self.POSITION_ITERATIONS = 10

        self.maxAsteroidPerLevel = MAX_ASTEROID_PER_LEVEL        
        self.numAsteroidSpawned = 0
      
        self.shake = Shake(SHAKE_DURATION, SHAKE_INTENSITY, SHAKE_FREQUENCY)
        self.world = Box2D.b2World((0, 0), doSleep=True)
        self.world.contactFilter = CollisionFilter()
        self.world.contactListener = ContactListener()
        self.ship = Ship(self.world, self.cannonIsShot, self.shake, False)
  
        self.cannonFireList = []
        self.asteroids = []
        
        self.obstacle_timer = pygame.USEREVENT + 1
        self.time_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacle_timer, 2000)
        pygame.time.set_timer(self.time_timer, 1000)
        
    # def destroy(self):
        
        
    def cannonIsShot(self, cannon:Cannon):
        self.cannonFireList.append(cannon)
        
    def cannonUpdate(self, screen):
        for cannon in self.cannonFireList.copy():
            cannon.update(screen)    
            
            if cannon.isOutOfScreen():
                cannon.dispose()
                self.cannonFireList.remove(cannon)
                
    def collisionDetection(self):
        collisionDetected = False
        
    
        for i in range(len(self.cannonFireList)-1, -1, -1):
            cannon = self.cannonFireList[i]
           
            for j in range(len(self.asteroids)-1, -1, -1):
                asteroid = self.asteroids[j]
                               
                if asteroid.rect.colliderect(cannon.rect) and \
                    pygame.sprite.collide_mask(cannon, asteroid):
                    # handle cannon
                    cannon.dispose()
                    self.cannonFireList.pop(i)
                    
                    # handle asteroid
                    asteroid.takeDamage()
                    if asteroid.isAsteroidDead():
                        self.asteroids.pop(j)
                        self.controller.reportAsteroidDestroyed()
                        if asteroid.canBreakApart():
                            asteroidA, asteroidB = asteroid.breakApart(debugDraw=False)
                            self.asteroids.append(asteroidA)
                            self.asteroids.append(asteroidB)
                        asteroid.dispose()
                    
                    collisionDetected = True
                    break
            if collisionDetected:
                break
                
        
    def spawnAsteroid(self):
        if np.random.rand() < .2 or len(self.asteroids) > MAX_ASTEROID_ON_SCREEN\
            or self.controller.shouldSpawnedAsteroid() == False or self.controller.isLevelInProgress() == False:
            return
        
        self.controller.reportAsteroidSpawned()
        asteroid = Asteroid(self.world, self.shake, debugDraw=False)
        self.asteroids.append(asteroid)
        
        
    def asteroidsUpdate(self, screen):
        for i in range(len(self.asteroids)-1, -1, -1):
            asteroid = self.asteroids[i] 
            asteroid.update(screen)
            
    def gameUpdate(self, screen):
        self.world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)

        self.collisionDetection()
        self.ship.update(screen)
        self.asteroidsUpdate(screen)
        self.cannonUpdate(screen)
        self.hud.update(screen, self.controller)
        self.controller.controllerUpdate(len(self.asteroids))
        
    def handleGameEvents(self, event:pygame.event.Event):
        
        self.shake.eventUpdate(event)
        
        if event.type == self.obstacle_timer:
                self.spawnAsteroid()
        
        if event.type == self.time_timer:
                # self.gameTime -= 1
            self.controller.gameTimePulse()
        
        # if event.type == pygame.MOUSEBUTTONUP:
        #     pos = toWorldPos(event.pos, WSCALE, HEIGHT)
        #     self.spawnAsteroid(*pos)
        
        self.ship.handleEvents(event)
        
        