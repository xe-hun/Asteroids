import math
import os
import random
import numpy as np
import pygame
from asteroid import Asteroid
from cannon import Cannon
from constant import WIDTH, HEIGHT, outlineColor, backgroundColor, FPS
from helper import mapValue
from ship import Ship



class Main():
    
    
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
        cannonIsDestroyed = False
        for cannon in self.cannonFireList.copy():
            cannon.update(screen)
            
            for asteroid in self.asteroids:
                if asteroid.asteroidRect.colliderect(
                    cannon.cannonRect):
                    cannon.dispose()
                    self.cannonFireList.remove(cannon)
                    cannonIsDestroyed = True
                    break
            if cannonIsDestroyed:
                break
                    
            if cannon.isOutOfScreen():
                cannon.dispose()
                self.cannonFireList.remove(cannon)
                

    def gameUpdate(self, screen):
                    
        self.ship.update(screen)
        self.cannonUpdate(screen)
        # pygame.display.update()
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
        
        
    def asteroidsUpdate(self):
        for asteroid in self.asteroids.copy():
            if asteroid.isOutOfScreen():
                asteroid.dispose()
                self.asteroids.remove(asteroid)
            asteroid.update(self.screen)
            
            
                
        


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
                
            
            self.asteroidsUpdate()
            self.gameUpdate(self.screen)
                
        pygame.quit()
        quit()
    
                



if __name__ == "__main__":
    main = Main()
    main.game()