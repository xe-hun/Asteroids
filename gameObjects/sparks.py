


import math
import random
import numpy as np
import pygame
from utils.helper import Helper, v_rotate, v_to_component
from utils.lerp import Lerp


class Sparks():
    
    def __init__(self)->None:
        pass
        
    @classmethod
    def directional(cls, direction, position, quantity:int = 5, start_perimeter:int = 6, max_perimeter:int = 60, particle_size:float = 1):
        return cls()._create_directional(direction, position, quantity, start_perimeter, max_perimeter, particle_size)
    
    def _create_directional(self, direction:tuple, position:tuple, quantity:int,  start_perimeter:int = 6, max_perimeter:int = 60, particle_size:float = 1):
        self._position = position
        self._direction = -direction
        self._particle_list = []
        
        # rondimise angle from -30 to 30
        for _ in range(quantity):
            random_direction = -30  +  60 * random.random()
            random_direction = math.radians(random_direction)
            
            direction_vector = v_rotate(self._dirsection, random_direction)
            
            max_range = start_perimeter + random.random() * max_perimeter
            particle = SparkParticle(self._position, direction_vector, particle_size, start_perimeter, max_range)    
            self._particle_list.append(particle)            
        
        return self
    
    @classmethod
    def create_random(cls, position, quantity:int = 5, start_perimeter:int = 6, max_perimeter:int = 60, particle_size:float = 1):
        return cls()._create_random(position, quantity, start_perimeter, max_perimeter, particle_size)
    
    def _create_random(self, position:tuple, quantity:int,  start_perimeter:int = 6, max_perimeter:int = 60, particle_size:float = 1):
        self._position = position
        self._particle_list = []
        
        for _ in range(quantity):
            random_direction = 2 * math.pi * random.random()
            direction_vector = v_to_component(random_direction)
            
            max_range = start_perimeter + random.random() * max_perimeter
            particle = SparkParticle(self._position, direction_vector, particle_size, start_perimeter, max_range)
            self._particle_list.append(particle)
            
        return self
            
        
    @property
    def alive(self):
        return len(self._particle_list) >= 0
     
            
    def update(self):  
        self._particle_list = [p for p in self._particle_list if p.alive]
        
        for particle in self._particle_list:
            particle.update()
            
    
    
    def draw(self, screen:pygame.surface.Surface):
        for particle in self._particle_list:
            particle.draw(screen)
            
            
        
class SparkParticle():
    
    def __init__(self, position, direction, particle_radius, min_sphere, max_sphere):
        self._radius = particle_radius
        self._position = np.array(position)
        self._direction = np.array(direction)
        self._min_sphere = min_sphere
        self._max_sphere = max_sphere
        self._color = (255, 255, 255)
        self._surface = pygame.Surface((self._radius * 2,) * 2, pygame.SRCALPHA)
        pygame.draw.circle(self._surface, self._color, (self._radius,) * 2, self._radius)
        self._surface = Helper.add_glow5(self._surface, intensity=3)
        self._lerp = Lerp()
        self._alive = True
        self._path = self._position
        self._alpha = 255
        
        
    @property
    def alive(self):
        return self._alive
        
    def _kill(self):
        self._alive = False
        
    def update(self):  
        self._path, self._alpha = self._lerp.do(400, self._update_parameters, self._kill).value
        
    def draw(self, screen:pygame.surface.Surface):
      
        
        
        # self._surface.set_alpha(self._alpha)
        rect = self._surface.get_rect(center = self._path)
        screen.blit(self._surface, rect.topleft)
        
    def _update_parameters(self, lerp:Lerp):
        
        displacement = lerp.linear(self._min_sphere, self._max_sphere)
        alpha = lerp.ease_out(255, 0)
        path = self._position + self._direction * displacement
        return path, alpha
     
        
        
        

