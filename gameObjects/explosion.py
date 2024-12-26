


import pygame
# from constant import outline_color
from utils.colors import Colors
from utils.lerp import Lerp


class Explosion():
    
    def __init__(self, position)->None:
        self._position = position
        self._r1 = None
        self._w1 = None
        self._alpha = None
        self._max_radius = 90
        
        self._surface = pygame.Surface((self._max_radius * 2,) * 2, pygame.SRCALPHA)
        
        
        self._lerp = Lerp()
        self._alive = True
        
        
    @property
    def alive(self):
        return self._alive
        
     
    
    def _kill(self):
        self._alive = False
    
    def _update_parameters(self, lerp:Lerp):
        r1 = lerp.ease_out(40, self._max_radius)
        w1 = lerp.ease_out(10, 5)
        alpha = lerp.ease_out(255, 0)
        return r1, int(w1), alpha
        
        
    def update(self):  
        self._r1, self._w1 ,self._alpha= self._lerp.do(500, self._update_parameters, self._kill).value
    
    def draw(self, screen:pygame.surface.Surface):
        self._surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self._surface, (*(Colors.drawing_color), self._alpha), (self._max_radius,) * 2, self._r1, self._w1)
        rect = self._surface.get_rect(center=self._position)
        screen.blit(self._surface, rect.topleft)

