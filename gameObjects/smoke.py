 
        
import random
import numpy as np
import pygame
from config.rocket_config import RocketConfig
from constant import FPS
from utils.lerp import Lerp
from utils.helper import scale


class Smoke:
    def __init__(self, rate:int = 30, tail:float = .3):
        self.pf = FPS // rate
        self.tail = tail
        self.particles = []
        self.frames = 0
        self.img = pygame.image.load(RocketConfig.smoke_path).convert_alpha()
        
    def update(self, direction:tuple, velocity:tuple, position:tuple):
        self.particles = [i for i in self.particles if i.alive]
        self.frames += 1
        if self.frames % self.pf == 0:
            self.frames = 0
            rotated_image = pygame.transform.rotate(self.img, random.random() * 360)
            self.particles.append(SmokeParticle(rotated_image,direction, velocity, position, self.tail))
        for i in self.particles:
            i.update()
            
    def draw(self, screen:pygame.surface.Surface):
        for i in self.particles:
            i.draw(screen)
            
            


class SmokeParticle:
    
    def __init__(self, img:pygame.surface.Surface,direction:tuple, velocity:tuple, position:tuple, tail:float):
        
        self.SCALE_RATE = .0009
        
        self.tail = tail * 1000
        # tail = clamp(0, 1, tail)
        self.direction = np.array(direction)
        self.velocity = np.array(velocity)
        self.position = np.array(position)
        
        self.img_scale = .02
        self.unscaled_image = img
        self.scaled_image = scale(self.unscaled_image, self.img_scale)
        self.alpha = 255
        self.alpha_rate = 30
        self.alive = True
        self.particle_speed = 3
        
        self.lerp = Lerp()
        

    def dispose(self):
        self.alive = False
        
    def update(self):
        
        particle_force = -self.direction * self.particle_speed
        particle_force += self.velocity
        self.position += particle_force
        
        self.img_scale += self.SCALE_RATE
        
      
        self.alpha = self.lerp.do(self.tail, lambda lerp:lerp.ease_in(255, 0), self.dispose).value
       
            
        self.scaled_image = scale(self.unscaled_image, self.img_scale)
        self.scaled_image.set_alpha(self.alpha)
        
    def draw(self, screen:pygame.surface.Surface):
        screen.blit(self.scaled_image, self.scaled_image.get_rect(center = self.position))
        
    