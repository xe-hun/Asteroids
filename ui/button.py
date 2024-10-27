import pygame

from utils.delay import Delay
from globalResolver import GlobalResolver
from utils.lerp import Lerp


class Button():
    def __init__(self, text:str, dimension:tuple, on_click:callable, color:tuple = (0, 0, 0, 0), click_color:tuple = None, hover_color:tuple = None, text_color:tuple = (255, 255, 255), font_size:int = 30, font:pygame.font.Font = None):
        
        self._font = font if font != None else pygame.font.Font(None, font_size)
        self._on_click = on_click
        self._dimension = dimension
        self._color = color
        self._click_color = click_color
        self._hover_color = hover_color
        self._text_color = text_color
        
        self._surface = pygame.Surface(dimension, pygame.SRCALPHA)
        self._surface.fill(color)
        self._text_render = self._font.render(text, False, self._text_color)
        self._rect = self._surface.get_rect()
        self._is_clicked = False
        self._hover = False
        self._click_lerp = Lerp(activate=False)
        self._on_click_delay = Delay(activate=False)
        
    def _click_effect(self, lerp:Lerp):
        if self._click_color == self._color:
            return self._surface
        
        r = int(lerp.sinusoidal(self._color[0], self._click_color[0]))
        g = int(lerp.sinusoidal(self._color[1], self._click_color[1]))
        b = int(lerp.sinusoidal(self._color[2], self._click_color[2]))
        
        return (r, g, b), self._text_render
    
    def _on_click_done(self):
        self._fill_hover_color()
            
    
    def draw(self, screen:pygame.surface.Surface, position:tuple, pause:bool = False):
        
        GlobalResolver.event_queue.add(self)
    
        click_lerp = self._click_lerp.control(pause).do(200, self._click_effect, self._on_click_done)
        color, text_render = click_lerp.value
        
        if click_lerp.is_done == False:
            self._surface.fill(color)
            
        self._rect = self._surface.get_rect(center = position)
        self._text_rect = text_render.get_rect(center=position)
            
        screen.blit(self._surface, self._rect)
        screen.blit(text_render, self._text_rect)
        
        self._on_click_delay.delay(200, self._on_click)
            
        
    def _fill_hover_color(self):
        if self._hover_color == None:
            return
        if self._hover == True:
            self._surface.fill(self._hover_color)
        else:
            self._surface.fill(self._color)
        
    
    def handle_event(self, event):
        
        if event.type == pygame.MOUSEMOTION:
            if self._rect.collidepoint(event.pos):
                self._hover = True
                self._fill_hover_color()
            elif self._hover == True:
                self._hover = False
                self._fill_hover_color()
                    
            
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self._is_clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._rect.collidepoint(event.pos) and self._is_clicked:
                self._is_clicked = False
                self._click_lerp = Lerp()
                self._on_click_delay = Delay()