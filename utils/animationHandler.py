

import pygame

from utils.delay import Delay
from utils.helper import scale


class AnimationHandler():
    def __init__(self, path:str, sprite_width:float, sprite_height:float, frame_count:int, mscale:int = 1):
       
        sprite_sheet = pygame.image.load(path).convert_alpha()
        
        self._frame_count = frame_count
        self._current_frame = 0
        self._sprites = []
        self._delay = Delay()
        
        
        for i in range(frame_count):
            surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            surface.blit(sprite_sheet, (0, 0), rect)
            self._sprites.append(scale(surface, mscale))
            
        self._sprite = self._sprites[self._current_frame]
        self._current_frame += 1
       
        
    def animate(self, position, degree_angle, screen:pygame.surface.Surface):
    
     
        # if self._delay.delay(5, reset=True).done() == True:
        self._current_frame = self._current_frame % self._frame_count
        self._sprite = self._sprites[self._current_frame]
        self._current_frame += 1
        
        
        s = pygame.transform.rotate(self._sprite, degree_angle)
        rect = s.get_rect(center=position)
        screen.blit(s, rect.topleft)
