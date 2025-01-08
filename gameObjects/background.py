

import random
import pygame

from config.GlobalConfig import GlobalConfig


class Background():
    def __init__(self):
        self._surface = pygame.Surface((GlobalConfig.width, GlobalConfig.height), pygame.SRCALPHA)
        self._base_color = (245, 240, 224)
        self._max_radius = 1
        self._alpha = 30
        self._max_stars = 500
        self._draw_stars(self._surface)
        
    def _draw_stars(self, surface:pygame.surface.Surface):
        for _ in range(self._max_stars):
            x = random.random() * GlobalConfig.width
            y = random.random() * GlobalConfig.height
            # r = self._base_color[0] + (255 - self._base_color[0]) * random.random()
            # g = self._base_color[1] + (255 - self._base_color[1]) * random.random()
            # b = self._base_color[2] + (255 - self._base_color[2]) * random.random()
        
            # color = (r, g, b, self._alpha)
            color = (245, 240, 224, self._alpha)
            
            radius = 1 + random.random() * self._max_radius
            pygame.draw.circle(surface, color, (x, y), radius)
    
    def draw(self, screen:pygame.surface.Surface):
        screen.blit(self._surface, (0, 0))