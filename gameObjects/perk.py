

from enum import Enum
import random

import numpy as np
from config import Colors
from constant import HEIGHT, WIDTH, outline_color


import pygame

from utils.delay import Delay
from gameObjects.objectBase import ObjectBase, ProjectileBase
from utils.helper import v_mag, v_norm, scale
from utils.lerp import Lerp


class Perk(ObjectBase, ProjectileBase):
    def __init__(self):
        self._game_font_30 = pygame.font.Font('font/pixeltype.ttf', 25)
        self._vertices1 = [
            (5, 5), (5, 15), (10, 20),(15, 15), (15, 5)
        ]
        
        self._vertices2 = [
            (0, 0), (10, 5), (20, 0), (10, 20)
        ]
        
        self._surface = pygame.Surface((21, 21), pygame.SRCALPHA)
        self.image = self._surface
        self.rect = self.image.get_rect()
        
        self._time_to_die = 15000        
        # self._position = np.array(position)
        self._alive = True
        self._time_to_die_lerp = Lerp()
        self._delay = Delay()
        self._scale = 1
        self._target:ObjectBase = None
        self._delay_duration = random.randint(3000, 5000)
        self._attraction_lerp = Lerp()
        
    @classmethod
    def rocket(cls, position, camera): 
        return cls()._create_rocket_perk(position, camera)
        
        
    def _create_rocket_perk(self, position, camera):
        self.label_render = self._game_font_30.render('R', False, Colors.background_color)
        self._draw_polygon(Colors.green_color)
        self._position = np.array(position)
        self._camera = camera
        self._perk_type = PerkType.rocket
        return self
    
    
    @classmethod
    def upgrade(cls, position, camera): 
        return cls()._create_upgrade_perk(position, camera)
        
       
    def _create_upgrade_perk(self, position, camera):
        self.label_render = self._game_font_30.render('S', False, Colors.background_color)
        self._draw_polygon(Colors.blue_color)
        self._position = np.array(position)
        self._camera = camera
        self._perk_type = PerkType.upgrade
        return self
    
    
    def _draw_polygon(self, item_color):
        pygame.draw.polygon(self._surface, Colors.red_color, self._vertices2, 1)
        pygame.draw.polygon(self._surface, item_color, self._vertices1)
        pygame.draw.polygon(self._surface, Colors.red_color, self._vertices1, 2)
    
    
    @property
    def alive(self):
        return self._alive
    
    @property
    def position(self):
        return self._position
    
    @property
    def direction(self):
        return None
    
    @property
    def target(self):
        return self._target
    
    @property
    def perk_type(self):
        return self._perk_type 
    
    
    def _scale_and_displacement(self, lerp:Lerp):
        return lerp.sinusoidal(1, 1.2, 20), lerp.sinusoidal(-.1, .1, 10)
    
    
    def set_target(self, value:ObjectBase):
        self._target = value
        
        
    def check_and_dispose(self):
        if self.target == None:
            self.dispose()
        
        
    def update(self):
        self._scale, _displacement = self._time_to_die_lerp.do(self._time_to_die, self._scale_and_displacement, self.check_and_dispose).value
        if self._target == None:
            self._position = (self.position[0], self.position[1] + _displacement)
        else:
            position_difference = self._target.position - self.position 
            direction_to_target = v_norm(position_difference)
            distance_to_target = v_mag(position_difference)
            
            attraction_factor = self._attraction_lerp.do(1000, lambda lerp: lerp.cubic_ease_in(0, 1)).value
            self._position += direction_to_target * distance_to_target * attraction_factor
             
        self._position = self._camera.watch(self.position)
        
        
    def draw(self, screen:pygame.surface.Surface):
        self.image = scale(self._surface, self._scale)
        self.rect = self.image.get_rect(center = self._position)
        screen.blit(self.image, self.rect.topleft)
        
        label_render = scale(self.label_render, self._scale)
        label_rect = label_render.get_rect(center = (self._position[0] + 1.4, self.position[1] + 2.8))
        screen.blit(label_render, label_rect.topleft)
        
        
    def dispose(self):
        self._alive = False
    
    
    def is_out_of_screen(self):
        if self._position[0] > WIDTH or self._position[0] < 0 or \
            self._position[1] > HEIGHT or self._position[1] < 0:
                return True
        else:
            return False
        
    
    
    
class PerkType(Enum):
    rocket = 1
    upgrade = 2