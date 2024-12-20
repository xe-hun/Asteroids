import pygame
from config import Colors
from ui.button import Button


class UiFactory():
  
    
    _button_size_dimension = (500, 55)
    _click_color = (200, 200, 200)
    _hover_color = (50, 50, 50)
    _text_deactivate_color = (120, 120, 120)
    
    def create_text(text:str, size:int = 35, font:pygame.font.Font = None, color:tuple = Colors.drawing_color):
        m_font = pygame.font.Font('font/pixeltype.ttf', size) if font == None else font
        render = m_font.render(text, False, color)
        text_render_surface = pygame.Surface(render.get_size(), pygame.SRCALPHA)
        text_render_surface.blit(render, (0, 0))
        return text_render_surface
    
    
    def create_button(text:str, on_clicked:callable, size:int = 20, is_active:bool = True, dimension:tuple = _button_size_dimension):
        
        font = pygame.font.Font('font/quantum.ttf', size)
        if is_active:
            return Button(text, dimension = dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=UiFactory._hover_color, font = font)
        else:
            return Button(text, dimension = dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=None, font = font, text_color = UiFactory._text_deactivate_color)
            