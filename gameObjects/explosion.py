


import pygame
# from constant import outline_color
from config.GlobalConfig import GlobalConfig
from utils.helper import Helper, clamp
from utils.colors import Colors
from utils.lerp import Lerp


class Explosion():
    
    def __init__(self, position)->None:
        self._position = position
        self._r1 = None
        self._w1 = None
        self._flare_blur_radius = None
        self._flare_scale = None
        self._alpha = None
        self._max_radius = 90
        self._flare_max_radius = 300
        self._flare_radius = 30
        
        self._surface = pygame.Surface((self._max_radius * 2,) * 2, pygame.SRCALPHA)
        self._flare_surface = pygame.Surface((self._flare_max_radius * 2 ,) * 2, pygame.SRCALPHA)
        
        self._flash_surface = pygame.Surface((GlobalConfig.width, GlobalConfig.height), pygame.SRCALPHA)
        pygame.draw.rect(self._flash_surface, (255, 255, 255, 30), pygame.Rect(0, 0, GlobalConfig.width, GlobalConfig.height))
        
       
        self._explosion_lerp = Lerp()
        self._flare_lerp = Lerp()
        self._alive = True
        self._flash = False
        
        
    @property
    def alive(self):
        return self._alive
        
     
    
    def _dispose(self):
        self._alive = False
    
    def _explosion_parameters(self, lerp:Lerp):
        r1 = lerp.ease_out(40, self._max_radius)
        w1 = lerp.ease_out(10, 5)
        alpha = lerp.ease_out(255, 0)
        return r1, int(w1), alpha
    
    def _flare_parameters(self, lerp:Lerp):
        # flare_alpha = lerp.sinusoidal(10, 30)
        flare_alpha = lerp.ease_out(60, 0)
        flare_scale = lerp.linear(1, self._flare_max_radius / self._flare_radius)
        return int(flare_alpha), flare_scale
        
        
    def update(self):  
        self._r1, self._w1 ,self._alpha= self._explosion_lerp.do(500, self._explosion_parameters, self._dispose).value
      
        self.flare_alpha, self._flare_scale = self._flare_lerp.do(int(7/GlobalConfig.fps * 1000), self._flare_parameters).value
        
        
    
    def draw(self, screen:pygame.surface.Surface):
        self._surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self._surface, (*(Colors.drawing_color), self._alpha), (self._max_radius,) * 2, self._r1, self._w1)
        rect = self._surface.get_rect(center=self._position)
        screen.blit(self._surface, rect.topleft)
        
        if self._flare_lerp.is_done == False:
            # flare_surface = self._flare_surface.copy()
            self._flare_surface.fill((0, 0, 0, 0))
            pygame.draw.circle(self._flare_surface, (255, 255, 255, self.flare_alpha), (self._flare_max_radius,) * 2, self._flare_radius * self._flare_scale)
            # self._flare_surface.set_alpha(self.flare_alpha)
            
            # self._flare_surface = Helper.add_glow5(self._flare_surface, intensity=5, radius=self.flare_blur_radius)
            flare_rect = self._flare_surface.get_rect(center=self._position)
            screen.blit(self._flare_surface, flare_rect.topleft)
            
            
        if self._flash == False:
            screen.blit(self._flash_surface, (0, 0))
            self._flash = True
            

