

import pygame
from config import Colors
from utils.delay import Delay
from utils.lerp import Lerp


class TimedList():
    def __init__(self, position:tuple, ingress_time:int = 1000, item_display_duration:int = 3000):
        
        self._game_font_10 = pygame.font.Font('font/quantum.ttf', 10)
        self._ingress_time = ingress_time
        self._item_display_duration = item_display_duration
        self._position = position
        self._target_item = None
        self._y_displacement = 0
        self._item_register_queue = []
        self._item_update_queue = []
        self._lerp1 = Lerp(activate=False)
        
    def _get_params(self, lerp:Lerp):
        alpha = lerp.ease_in(0, 255)
        displacement = lerp.ease_in(0, 20)
        return alpha, displacement
        
    def register_item(self, item_description:str):
        
        render = self._game_font_10.render(item_description, False, Colors.drawing_color)
        surface = pygame.Surface(render.get_size(), pygame.SRCALPHA)
        surface.blit(render, (0, 0))
      
        
        _target_e = (self._position, surface, Delay())
        self._item_register_queue.append(_target_e)
        
        if self._lerp1.is_done:
            if (self._target_item != None):
                self._save_position_checkpoint()
                self._item_update_queue.append(self._target_item)

            self._lerp1 = Lerp()
            self._target_item = self._item_register_queue[0]
            
        
    def draw(self, screen:pygame.surface.Surface):
        
        lerp_1 = self._lerp1.do(self._ingress_time, self._get_params, self._on_done)

        if lerp_1.is_done == False:
            alpha, self._y_displacement = lerp_1.value
        else:
            alpha = 255

        if self._target_item != None:
            position, surface, delay = self._target_item
        
            if delay.delay(self._item_display_duration).is_done == False:
                # print(alpha)
                surface.set_alpha(alpha)
                screen.blit(surface, surface.get_rect(center = position).topleft)
        
            for j in range(len(self._item_update_queue)-1, -1, -1):
                pos, sur, delay =  self._item_update_queue[j]
                
                if delay.delay(self._item_display_duration).is_done:
                    self._item_update_queue.pop(j)
                    continue
                
                # sur = self._game_font_10.render(ite, False, Colors.drawing_color)
                screen.blit(sur, sur.get_rect(center = (pos[0], pos[1] + self._y_displacement)).topleft)
            
   
                
                    
            
    def _save_position_checkpoint(self):
        for i in range(len(self._item_update_queue)):
            position, surface, _ = self._item_update_queue[i]
            new_position = (position[0], position[1] + self._y_displacement)
            self._item_update_queue[i] = (new_position, surface, _)
        self._y_displacement = 0
        
        
        
        
        
    def _on_done(self):
        self._item_register_queue = self._item_register_queue[1:]
        
        if len(self._item_register_queue) > 0:
                
            self._save_position_checkpoint()
            self._item_update_queue.append(self._target_item)
                
            self._lerp1 = Lerp()
            self._target_item = self._item_register_queue[0]
       
            
    