
import math
import numpy as np
import pygame

from config import CannonConfig, Colors, GlobalConfig
from gameObjects.objectBase import ObjectBase, ProjectileBase
from utils.helper import v_to_angle
from utils.camera import Camera


class Cannon(pygame.sprite.Sprite, ObjectBase, ProjectileBase):
    def __init__(self, direction:tuple, startPosition:tuple, camera:Camera):
        
        self.SIZE = CannonConfig.size
        self.SPEED = CannonConfig.speed
        self.THICKNESS = CannonConfig.thickness
        
        self._camera = camera
        _surface = pygame.Surface((self.SIZE, self.THICKNESS), pygame.SRCALPHA)
        pygame.draw.line(_surface, Colors.drawing_color, (0, 0), (self.SIZE, 0), self.THICKNESS)
        self.surface_r = pygame.transform.rotate(_surface, -math.degrees(v_to_angle(direction)))
        self.image = self.surface_r
        self.rect = self.surface_r.get_rect()
    
        self._direction = np.array(direction)
        self._position = np.array(startPosition)
        self._alive = True
    
        
    @property
    def position(self):
        return self._position
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def alive(self):
        return self._alive

    
    def update(self):
        
        self._position += self._direction * self.SPEED
        self._position = self._camera.watch(self._position)
    
        
    def draw(self, screen:pygame.surface.Surface):
        self.rect = self.surface_r.get_rect(center = self._position)
        screen.blit(self.surface_r, self.rect.topleft)
        
    def is_out_of_screen(self):
        if self._position[0] > GlobalConfig.width or self._position[0] < 0 or \
            self._position[1] > GlobalConfig.height or self._position[1] < 0:
                return True
        else:
            return False
                
            
         
    def dispose(self):
        self.surface_r = None
        self._alive = False
    