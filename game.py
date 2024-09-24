import math
import os
import random
import numpy as np
import pygame
from gameObjects.asteroid import Asteroid
from gameObjects.cannon import Cannon
from constant import WIDTH, HEIGHT, outlineColor, backgroundColor, FPS
from utils.helper import mapValue
from gameObjects.ship import Ship


class Game():
    def __init__(self):
      
        self.ship = Ship(self.cannonIsShot)
        # self.cannonFireList = set()
        # self.asteroids = set()
        self.cannonFireList = []
        self.asteroids = []
        
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,2000)
        
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
        # for asteroid in self.asteroids.copy():
        for i in range(len(self.asteroids)-1, -1, -1):
            asteroid = self.asteroids[i]
            
            
            if asteroid.rect.colliderect(self.ship.rect) and \
                pygame.sprite.collide_mask(asteroid, self.ship):
                    print('zin')
                    shipMass = 10
                    asteroidMass = 50
                    
                    
                    
                    
                    prevShipSpeed = np.array([self.ship.speedX, self.ship.speedY])
                    prevAsteroidSpeed = np.array([asteroid.speedX, asteroid.speedY])
                    
                    # velocity_exchange = (prevAsteroidSpeed - prevShipSpeed) * (2 * asteroidMass) / (shipMass + asteroidMass)
                    
                    # newShipSpeed = prevShipSpeed + velocity_exchange
                    # newAsteroidSpeed = prevAsteroidSpeed - velocity_exchange
                    
                    newShipSpeed = (prevShipSpeed * (shipMass - asteroidMass) + 2 * asteroidMass * prevAsteroidSpeed) / (shipMass + asteroidMass)
                    newAsteroidSpeed = (prevAsteroidSpeed * (asteroidMass - shipMass) + 2 * shipMass * prevShipSpeed) / (shipMass + asteroidMass)
                    
                    # newShipSpeed *= .7
                    # newAsteroidSpeed *= .7
                    
                    
                    self.ship.SpeedX, self.ship.speedY = newShipSpeed[0], newShipSpeed[1]
                    asteroid.speedX, asteroid.speedY = newAsteroidSpeed[0], newAsteroidSpeed[1]
                    
                 
                    
            
            # for cannon in self.cannonFireList.copy():
            for j in range(len(self.cannonFireList)-1, -1, -1):
                cannon = self.cannonFireList[j]
                               
                if asteroid.rect.colliderect(cannon.rect) and \
                    pygame.sprite.collide_mask(cannon, asteroid):
                    # handle cannon
                    cannon.dispose()
                    # self.cannonFireList.remove(cannon)
                    self.cannonFireList.pop(j)
                    
                    # handle asteroid
                    asteroid.takeDamage()
                    if asteroid.isAsteroidDead():
                        asteroid.dispose()
                        # self.asteroids.remove(asteroid)
                        self.asteroids.pop(i)
                    
                    collisionDetected = True
                    break
            if collisionDetected:
                break
                

   
        
        
    def spawnAsteroid(self):
        
        pi = math.pi
        spawnPosAndAngle = random.choices([
         (-10,                         np.random.rand() * HEIGHT,   mapValue(0, 1, -0.25 * pi, 0.25 * pi, np.random.rand()) ),
         (np.random.rand() * WIDTH,    HEIGHT + 10,                 mapValue(0, 1, 1.25 * pi , 1.75 * pi, np.random.rand()) ),
         (WIDTH + 10,                  np.random.rand() * HEIGHT,   mapValue(0, 1, 0.75 * pi , 1.25 * pi, np.random.rand()) ),
         (np.random.rand() * WIDTH,    -10,                         mapValue(0, 1, 0.25 * pi , 0.75 * pi, np.random.rand()) ),
         None,],
         weights=[1,2,2,1,3])
        
        if(spawnPosAndAngle[0] == None):
            return
        
        
        asteroid = Asteroid(*spawnPosAndAngle)
        self.asteroids.append(asteroid)
        
        
    def asteroidsUpdate(self, screen):
        for asteroid in self.asteroids.copy():
            if asteroid.isOutOfScreen():
                asteroid.dispose()
                self.asteroids.remove(asteroid)
            asteroid.update(screen)
            
    def gameUpdate(self, screen):
        self.collisionDetection()
        self.ship.update(screen)
        self.asteroidsUpdate(screen)
        self.cannonUpdate(screen)
        
    def handleGameEvents(self, event:pygame.event.Event):
        if event.type == self.obstacle_timer:
                self.spawnAsteroid()
        
        self.ship.handleEvents(event)
        
        