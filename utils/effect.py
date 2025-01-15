
import pygame

from utils.helper import scale
from utils.lerp import Lerp


class Effect():
    def __init__(self):
        self._lerp = None
        
    def effect_1(self, obj:pygame.surface.Surface, duration:int = 1000, on_color:tuple = None, off_color:tuple = None):
        if (self._lerp == None):
           
            return obj
        else:
            lerp_value = self._lerp.do(duration, lambda lerp: lerp.sinusoidal(0, .3), self._on_effect_1_done).value
            factor = 1 + lerp_value
            # ifs o
            # obj.set_colorkey(on_color)
            return scale(obj, factor)
        
        
    def alternate_color(self, duration:int = 1000, color_1:tuple = (255, 255, 255), color_2:tuple = (255, 0, 0)):
        
        if (self._lerp != None):
            lerp_value = self._lerp.do(duration, self._effect_2_function, self._on_effect_2_done, color_1 = color_1, color_2 = color_2).value
            return lerp_value
        else:
            return color_1
         
        
    
    def _on_effect_1_done(self):
        self._lerp = None
   
            
    def _effect_2_function(self, lerp:Lerp, color_1:tuple, color_2:tuple):
        r1, g1, b1 = color_1
        r2, g2, b2 = color_2
        
        return lerp.sinusoidal(r1, r2), lerp.sinusoidal(g1, g2), lerp.sinusoidal(b1, b2),
        
    def _on_effect_2_done(self):
        self._lerp = Lerp()
    
    def activate(self):
        self._lerp = Lerp()
     
        
        
        
        