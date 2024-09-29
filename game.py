import math
import os
import random
import numpy as np
import pygame
import Box2D
from gameObjects.asteroid import Asteroid
from gameObjects.cannon import Cannon
from constant import WIDTH, HEIGHT, WSCALE, outlineColor, backgroundColor, FPS
from utils.helper import getBodyBounds, mapValue, toWorldPos
from gameObjects.ship import Ship


class Game():
    def __init__(self):
        
          
        self.VELOCITY_ITERATIONS = 10
        self.POSITION_ITERATIONS = 10
      
        self.world = Box2D.b2World((0, 0), doSleep=True)
        self.ship = Ship(self.world, self.cannonIsShot, False)
  
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
                        asteroid.dispose()
                        # self.asteroids.remove(asteroid)
                        self.asteroids.pop(j)
                    
                    collisionDetected = True
                    break
            if collisionDetected:
                break
                
        
    def spawnAsteroid(self, xPos, yPos):
        if np.random.rand() < .2:
            return
        
        asteroid = Asteroid(self.world, xPos, yPos)
        self.asteroids.append(asteroid)
        
        
    def asteroidsUpdate(self, screen):
        for i in range(len(self.asteroids)-1, -1, -1):
            asteroid = self.asteroids[i]
            
           
            
            if asteroid.isOutOfBounds():
                asteroid.dispose()
                self.asteroids.pop(i)
                continue    
            asteroid.update(screen)
            
    def gameUpdate(self, screen):
        self.world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)

        self.collisionDetection()
        self.ship.update(screen)
        self.asteroidsUpdate(screen)
        self.cannonUpdate(screen)
        
    def handleGameEvents(self, event:pygame.event.Event):
        if event.type == self.obstacle_timer:
                self.spawnAsteroid(0, 0)
        
        # if event.type == pygame.MOUSEBUTTONUP:
        #     pos = toWorldPos(event.pos, WSCALE, HEIGHT)
        #     self.spawnAsteroid(*pos)
        
        self.ship.handleEvents(event)
        
        