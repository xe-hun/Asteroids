import numpy as np
import pygame
import Box2D
from effects.worldStar import WorldStar
from gameObjects.rocket import Rocket
from gameStateController import GameStateController
from strategies.targetStrategy import TargetStrategy
from utils.camera import Camera
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
      
        self.camera = Camera(SHAKE_DURATION, SHAKE_INTENSITY, SHAKE_FREQUENCY)
        self.world = Box2D.b2World((0, 0), doSleep=True)
        self.world.contactFilter = CollisionFilter()
        self.world.contactListener = ContactListener()
        self.ship = Ship(self.world, self.projectileIsShot, self.camera, False)
  
        self.cannonFireList = []
        self.rocketFireList = []
        self.asteroids = []
        
        self.obstacle_timer = pygame.USEREVENT + 1
        self.time_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacle_timer, 2000)
        pygame.time.set_timer(self.time_timer, 1000)
        
        self.worldStar = WorldStar()
        
    # def destroy(self):
        
        
    def projectileIsShot(self, projectile:Cannon | Rocket):
      
        if isinstance(projectile, Cannon):
            self.cannonFireList.append(projectile)
            
        if isinstance(projectile, Rocket):
            self.rocketFireList.append(projectile)
        
    def projectileUpdate(self, screen, isLevelInProgress):
        if isLevelInProgress == False:
            return
        
        for i in range(len(self.cannonFireList)-1, -1, -1):
            cannon = self.cannonFireList[i]
          
            cannon.update(screen)
            
            if cannon.isOutOfScreen():
                self.cannonFireList.pop(i)
                
        for i in range(len(self.rocketFireList)-1, -1, -1):
            rocket = self.rocketFireList[i]
            if rocket.hasTarget() == False:
                targetPosition = TargetStrategy(rocket.position, [i.position for i in self.asteroids], 300).targetPosition()
                rocket.setTargetPosition(targetPosition)

            rocket.update(screen)
            
            if rocket.isOutOfScreen():
                self.rocketFireList.pop(i)
                
                
                
                
                
                # projectile.dispose()
                
        # for cannon in self.cannonFireList.copy():
        #     cannon.update(screen)    
            
        #     if cannon.isOutOfScreen():
        #         cannon.dispose()
        #         self.cannonFireList.remove(cannon)
                
    def collisionDetection(self):
        collisionDetected = False
        
        for i in range(len(self.rocketFireList)-1, -1, -1):
            rocket = self.rocketFireList[i]
           
            for j in range(len(self.asteroids)-1, -1, -1):
                asteroid = self.asteroids[j]
                
                if asteroid.rect.colliderect(rocket.rect) and \
                    pygame.sprite.collide_mask(rocket, asteroid):
                    # handle cannon
                    # cannon.dispose()
                    self.rocketFireList.pop(i)
        
        
        
    
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
        asteroid = Asteroid(self.world, self.camera, debugDraw=False)
        self.asteroids.append(asteroid)
        
        
    def asteroidsUpdate(self, screen):
        for i in range(len(self.asteroids)-1, -1, -1):
            asteroid = self.asteroids[i] 
            asteroid.update(screen)
            
    def gameUpdate(self, screen):
        if self.controller.isLevelInProgress():
            self.world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)

        self.worldStar.draw(screen)
        self.collisionDetection()
        
        self.ship.update(screen, self.controller.isLevelInProgress())
        self.asteroidsUpdate(screen)
        self.projectileUpdate(screen, self.controller.isLevelInProgress())
        self.hud.update(screen, self.controller)
        self.controller.controllerUpdate(len(self.asteroids))
        
    def handleGameEvents(self, event:pygame.event.Event):
        
        self.camera.eventUpdate(event)
        
        if event.type == self.obstacle_timer:
                self.spawnAsteroid()
        
        if event.type == self.time_timer:
                # self.gameTime -= 1
            self.controller.gameTimePulse()
        
        # if event.type == pygame.MOUSEBUTTONUP:
        #     pos = toWorldPos(event.pos, WSCALE, HEIGHT)
        #     self.spawnAsteroid(*pos)
        
        self.ship.handleEvents(event)
        
        