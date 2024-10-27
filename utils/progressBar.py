

import pygame

from constant import FPS
from utils.lerp import Lerp


class ProgressBar():
    def __init__(self, initial_progress:float = 1, bar_width:int = 400, bar_height:int = 2, fore_color:tuple = (200, 200, 200), background_color = (255, 25, 25)):
        self._bar_width = bar_width
        self._bar_height = bar_height
        self._fore_color = fore_color
        self._background_color = background_color
        self._checkpoint = self._value = initial_progress
        self._progress_bar_value = 1
        self._time_to_update = .1
        self._lerp = None
        
        
        self.surface = pygame.Surface((self._bar_width, self._bar_height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self._bar_width, self._bar_height)
        pygame.draw.rect(self.surface, self._fore_color, rect)
        
        self._draw(initial_progress)
        
        
    def lerp_progress(self, value):
        assert value >= 0 and value <= 1 
        'new value must be between 0 and 1'
        
        
        self._checkpoint = self._progress_bar_value
   
        if value == self._checkpoint:
            return
        
        self._lerp = Lerp()
        self._value = value
        progress_diff = max(abs(value - self._checkpoint), 0.1)
        self._time_to_update = progress_diff * 3000
        
    @property
    def value(self):
        return self._value
        
    def set_progress(self, value):
        self._value = self._progress_bar_value = value
        self._draw(value)
        
    def _draw(self, progress_bar_value):
        rect = pygame.Rect(0, 0, self._bar_width, self._bar_height)
        pygame.draw.rect(self.surface, self._fore_color, rect)
        rect = pygame.Rect(0, 0, (1 - progress_bar_value) * self._bar_width + .1, self._bar_height)
        pygame.draw.rect(self.surface, self._background_color, rect)
        
       
        
    def update(self):
        if self._lerp == None:
            return
        lerp = self._lerp.do(self._time_to_update,
            lambda l: l.cubic_ease_out(self._checkpoint, self._value))
        
                
        if lerp.is_done == False:
            self._progress_bar_value = lerp.value
            self._draw(self._progress_bar_value)
            
            
        