

import numpy as np
import pygame

from constant import HEIGHT, WIDTH
from utils.delay import Delay
from utils.lerp import Lerp
from utils.helper import v_angle_diff, v_dot, v_mag, v_norm, v_rotate


import math
import random
import pygame
import numpy as np

from constant import FPS, HEIGHT, WIDTH
from utils.helper import clamp, scale




class Test():
    def __init__(self):
        self.smoke = SmokeT(50, tail=.9)
        # self.objPos = np.array((WIDTH / 2, HEIGHT / 2))
        # self.prevPos = self.objPos.copy()
        self.objDir = np.array((1, 0))
        self.mouseDown = False
        self.rocket = Rocket()
        self.delay = Delay()
        self.prevDir = self.objDir.copy()
        self.flareImage = pygame.image.load('images/flare.png').convert_alpha()
        
    def handleEvent(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouseDown = False
        
    def turnCall(self, lerp:Lerp, dir1, dir2):
        res = lerp.linear(dir1[0], dir2[0]) , lerp.linear(dir1[1], dir2[1])
        return res
    
    def updateDirection(self):
        if self.mouseDown:
            self.prevDir = self.objDir.copy()
            # self.objPos = np.array(event.pos)
            self.objDir = v_norm(np.array(pygame.mouse.get_pos()) - self.rocket.position)

    def update(self, screen:pygame.surface.Surface):
        
        self.delay.delay(400, self.updateDirection, True)
        
      
        screen.blit(self.flareImage, self.flareImage.get_rect(center = self.rocket.toWorldPos((-5, .5))).topleft)
        
        self.rocket.update(self.objDir)
        self.rocket.draw(screen)
        
        self.smoke.update(self.rocket.direction, self.rocket.velocity, self.rocket.toWorldPos((-5, .5)))
        self.smoke.draw(screen)
        
        # pygame.draw.line(screen, (10, 200, 10), self.rocket.position, self.rocket.toWorldPos((-50, -3)), 3)
        # if self.mouseDown:
        #      self.objPos = np.array(pygame.mouse.get_pos())
        
        # self.objVel = self.objPos - self.prevPos
        # self.prevPos = self.objPos.copy()
        
        
        
        
        # if mag(self.objVel) != 0:
        #     self.objDir = norm(self.objVel)
            
        # self.smoke.update(direction=self.objDir, velocity=self.objVel, position=self.objPos)
        # self.smoke.update(direction=self.objDir, velocity=(0,0), position=self.objPos)
        # self.smoke.draw(screen)
        
        

        


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
        
        
class SmokeT:
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
    
    
    
      
            
class Rocket():
    def __init__(self):
        self.img = scale(pygame.image.load('images/rocket.png').convert_alpha(), .2)
        self.speed = 5
        self.angle = 0
        self.position = np.array((WIDTH / 2, HEIGHT / 2))
        self.direction = None
        self.turnRate = math.radians(4)
        self.rect = self.img.get_rect()
        self.posOffset = np.array((0, 5))
        
        # self.velocity = None
        
    def toWorldPos(self, vec:tuple):
        return self.position + v_rotate(vec, self.angle)
    # + rotateVec(vec, self.angle)
    
    def update(self, newDirection:tuple):
                
        if self.direction is None:
            self.direction = newDirection
            
        if v_angle_diff(self.direction, newDirection) < self.turnRate:
            self.direction = newDirection
        else:
            dotProd = v_dot(self.direction, v_rotate(newDirection, math.pi / 2))
                
            if dotProd > 0:
                self.direction = v_rotate(self.direction, -self.turnRate)
            elif dotProd < 0:
                self.direction = v_rotate(self.direction, self.turnRate)
            
        self.velocity = self.direction * self.speed
        self.angle = math.atan2(self.direction[1], self.direction[0])
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        self.warp()
    
    def draw(self, screen:pygame.surface.Surface):
       
        rotImg = pygame.transform.rotate(self.img, -math.degrees(self.angle))
        self.rect = rotImg.get_rect(center = (self.position[0], self.position[1]))
        screen.blit(rotImg, self.rect.topleft)
        
    def warp(self):
        if self.position[0] > WIDTH:
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = WIDTH
            
        if self.position[1] > HEIGHT:
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = HEIGHT
  
    
    
    
    
    
    
            
         
            
# class Rocket():
#     def __init__(self):
#         self.img = pygame.image.load('images/rocket.png').convert_alpha()
#         self.speed = 3
#         self.angle = 0
#         self.position = np.array((WIDTH / 2, HEIGHT / 2))
#         self.direction = None
#         self.turnRate = math.radians(3)
        
#         # self.velocity = None
        
#     def update(self, newDirection:tuple):
#         if self.direction is None:
#             self.direction = newDirection
            
#         if angleDiff(self.direction, newDirection) < self.turnRate:
#             self.direction = newDirection
#         else:
#             dotProd = dot(self.direction, rotateVec(newDirection, math.pi / 2))
                
#             if dotProd > 0:
#                 self.direction = rotateVec(self.direction, -self.turnRate)
#             elif dotProd < 0:
#                 self.direction = rotateVec(self.direction, self.turnRate)
            
#         self.velocity = self.direction * self.speed
#         self.angle = math.atan2(self.direction[1], self.direction[0])
#         self.position[0] += self.velocity[0]
#         self.position[1] += self.velocity[1]
        
#         self.warp()
    
#     def draw(self, screen:pygame.surface.Surface):
       
#         rotImg = pygame.transform.rotate(self.img, -math.degrees(self.angle))
#         rect = rotImg.get_rect(center = (self.position[0], self.position[1]))
#         screen.blit(rotImg, rect.topleft)
        
#     def warp(self):
#         if self.position[0] > WIDTH:
#             self.position[0] = 0
#         if self.position[0] < 0:
#             self.position[0] = WIDTH
            
#         if self.position[1] > HEIGHT:
#             self.position[1] = 0
#         if self.position[1] < 0:
#             self.position[1] = HEIGHT
        
    
       
        
        