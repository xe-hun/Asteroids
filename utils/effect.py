

import pygame

from utils.helper import scale
from utils.lerp import Lerp


class Effect():
    def __init__(self):
        self._lerp = None
        
        
    
    def _on_effect_done(self):
        self._lerp = None
        
    
    def effect_1(self, obj:pygame.surface.Surface, duration:int = 1000, on_color:tuple = None, off_color:tuple = None):
        if (self._lerp == None):
            # if on_color != None:      
            #     obj.set_colorkey(off_color)      
            return obj
        else:
            lerp_value = self._lerp.do(duration, lambda lerp: lerp.sinusoidal(0, .3), self._on_effect_done).value
            factor = 1 + lerp_value
            # ifs o
            # obj.set_colorkey(on_color)
            return scale(obj, factor)
    
    def activate(self):
        self._lerp = Lerp()
     
        
        