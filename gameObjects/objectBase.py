
from abc import ABC, abstractmethod
import pygame


class ObjectBase(ABC):
    
    @property
    def position(self):
        pass
    
    @property
    def direction(self):
        pass
    
    @property
    def alive(self):
        pass
    
    @abstractmethod
    def dispose(self):
        pass
    
    @abstractmethod
    def draw(self, screen:pygame.surface.Surface):
        pass
   
    @abstractmethod
    def update(self):
        pass
    
class ProjectileBase(ABC):
    
    @abstractmethod
    def is_out_of_screen():
        pass
    
    
