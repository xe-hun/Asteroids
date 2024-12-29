 
from abc import ABC, abstractmethod

import pygame


class PageBase(ABC):
    
  
    is_transparent = False
    
    def update(self, paused):
        pass
    
    @abstractmethod
    def draw(self, screen:pygame.surface.Surface, **kwargs):
        pass
    
    def handle_event(self, event):
        pass
    
    def handle_event_2(self, event):
        pass