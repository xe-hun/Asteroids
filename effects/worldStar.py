import math
import random

import pygame

from config.globalConfig import GlobalConfig


class WorldStar():
    
    NUM_STARS = 30
    STAR_COLOR = (200, 200, 200)
    
    def __init__(self) -> None:
      
        self.starList = [(random.random() * GlobalConfig.width, random.random() * GlobalConfig.height,\
            1 + random.random() * 2) for i in range(WorldStar.NUM_STARS)]
    
    
    def draw(self, screen:pygame.surface.Surface):
        for s in self.starList:
           pygame.draw.circle(screen, WorldStar.STAR_COLOR, (s[0], s[1]), s[2])
            