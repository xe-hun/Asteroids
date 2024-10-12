 
        
import random
import pygame
from constant import FPS
from helper import clamp, scale


class Smoke:
    def __init__(self, rate:int = 30, tail:float = .5):
        self.pf = FPS // rate
        self.tail = tail
        self.particles = []
        self.frames = 0
        self.img = pygame.image.load('images/smoke.png').convert_alpha()
        
    def update(self, direction:tuple, velocity:tuple, position:tuple):
        self.particles = [i for i in self.particles if i.alive]
        self.frames += 1
        if self.frames % self.pf == 0:
            self.frames = 0
            rotatedImage = pygame.transform.rotate(self.img, random.random() * 360)

            self.particles.append(SmokeParticle(rotatedImage,direction, velocity, position, self.tail))
        for i in self.particles:
            i.update()
            
    def draw(self, screen:pygame.surface.Surface):
        for i in self.particles:
            i.draw(screen)
            
            


class SmokeParticle:
    
    def __init__(self, img:pygame.surface.Surface,direction:tuple, velocity:tuple, position:tuple, tail:float):
        tail = clamp(0, 1, tail)
        self.direction = direction
        self.velocity = velocity
        # variation =  .09 * random.random() * random.choice([-1, 1])
        self.x = position[0] 
        self.y = position[1] 
        self.scaleK = .03
        self.origImage = img
        self.scaledImage = scale(self.origImage, self.scaleK)
        self.alpha = 255
        # self.alphaRate = 255 / 2 * tail
        self.alphaRate = 10
        self.alive = True
        # self.vx = velocity[0] + random.random() * .01
        # self.vy = velocity[1] + random.random() * .01
        self.s =  .009 * random.random() * random.choice([-1, 1])
        
    def update(self):
        s = 10 
       
        smokeVelX, smokeVelY = 0, 0 
        smokeVelX = - self.direction[0] * s
        smokeVelY = - self.direction[1] * s
        
        smokeVelX += self.velocity[0]
        smokeVelY += self.velocity[1]
        
        self.x += smokeVelX 
        self.y += smokeVelY 
        self.scaleK += .0009
        self.alpha -= self.alphaRate
        if self.alpha < 0:
            self.alpha = 0
            self.alive = False
            
        self.alphaRate -= .1
        if self.alphaRate < 1.5:
            self.alphaRate = 1.5
            
        self.scaledImage = scale(self.origImage, self.scaleK)
        self.scaledImage.set_alpha(self.alpha)
        
    def draw(self, screen:pygame.surface.Surface):
        screen.blit(self.scaledImage, self.scaledImage.get_rect(center = (self.x, self.y)))
        
    