

import pygame
from gameObjects.explosion import Explosion


class ParticleSystem():
    
    def __init__(self):
        self._particles_list = []
        pass
    
    def update(self):
        pass
    
    def explode(self, position:tuple):
        explosion = Explosion(position)
        self._particles_list.append(explosion)
        
    def update(self):
        for p in self._particles_list:
            p.update()
            
    def draw(self, screen:pygame.surface):
        for p in self._particles_list:
            p.draw(screen)