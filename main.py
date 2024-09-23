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



class MainGame():
    
    
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption('Asteroids')
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ship = Ship(self.cannonIsShot)
        self.cannonFireList = set()
        self.asteroids = set()
        
    def cannonIsShot(self, cannon:Cannon):
        self.cannonFireList.add(cannon)
        
    def cannonUpdate(self, screen):
        for cannon in self.cannonFireList.copy():
            cannon.update(screen)    
            
            if cannon.isOutOfScreen():
                cannon.dispose()
                self.cannonFireList.remove(cannon)
                
    def collisionDetection(self):
        collisionDetected = False
        for cannon in self.cannonFireList.copy():
            for asteroid in self.asteroids.copy():
                if asteroid.rect.colliderect(cannon.rect) and \
                    pygame.sprite.collide_mask(cannon, asteroid):
                    # handle cannon
                    cannon.dispose()
                    self.cannonFireList.remove(cannon)
                    
                    # handle asteroid
                    asteroid.takeDamage()
                    if asteroid.isAsteroidDead():
                        self.asteroids.remove(asteroid)
                        asteroid.dispose()
                    
                    collisionDetected = True
                    break
            if collisionDetected:
                break
                

    def gameUpdate(self, screen):
                    
        self.collisionDetection()
        self.ship.update(screen)
        self.asteroidsUpdate(screen)
        self.cannonUpdate(screen)
        pygame.display.flip()
        
    def spawnAsteroid(self):
        
        pi = math.pi
        spawnPosAndAngle = random.choices([
         (-10,                         np.random.rand() * HEIGHT,   mapValue(0, 1, -0.25 * pi, 0.25 * pi, np.random.rand()) ),
         (np.random.rand() * WIDTH,    HEIGHT + 10,                 mapValue(0, 1, 1.25 * pi , 1.75 * pi, np.random.rand()) ),
         (WIDTH + 10,                  np.random.rand() * HEIGHT,   mapValue(0, 1, 0.75 * pi , 1.25 * pi, np.random.rand()) ),
         (np.random.rand() * WIDTH,    -10,                         mapValue(0, 1, 0.25 * pi , 0.75 * pi, np.random.rand()) ),
         None,],
         weights=[1,2,2,1,7])
        
        if(spawnPosAndAngle[0] == None):
            return
        
        
        asteroid = Asteroid(*spawnPosAndAngle)
        self.asteroids.add(asteroid)
        
        
    def asteroidsUpdate(self, screen):
        for asteroid in self.asteroids.copy():
            if asteroid.isOutOfScreen():
                asteroid.dispose()
                self.asteroids.remove(asteroid)
            asteroid.update(screen)
            
    def game(self):
        
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,2000)
        
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.screen.fill(backgroundColor)
    
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    run = False
                    break;
                if event.type == pygame.KEYDOWN:
                    pass
                
                if event.type == obstacle_timer:
                    self.spawnAsteroid()
                
                self.ship.handleEvents(event) 
                
            
           
            self.gameUpdate(self.screen)
                
        pygame.quit()
        quit()
    

if __name__ == "__main__":
    main = MainGame()
    main.game()