

import random
import pygame

from config.GlobalConfig import GlobalConfig


class Background():
    def __init__(self):
        self._surface = pygame.Surface((GlobalConfig.width, GlobalConfig.height), pygame.SRCALPHA)
        self._base_color = (245, 240, 224)
        self._max_radius = 1
        self._alpha = 200
        self._max_stars = 500
        self._draw_stars(self._surface)
        
    def _draw_stars(self, surface:pygame.surface.Surface):
        for _ in range(self._max_stars):
            x = random.random() * GlobalConfig.width
            y = random.random() * GlobalConfig.height
            if random.random() < .5:
                color = (33, 33, 33, self._alpha)
            else :
                 color = (63, 42, 70, self._alpha)
            
            
            radius = 1 + random.random() * self._max_radius
            pygame.draw.circle(surface, color, (x, y), radius)
    
    def draw(self, screen:pygame.surface.Surface):
        screen.blit(self._surface, (0, 0))