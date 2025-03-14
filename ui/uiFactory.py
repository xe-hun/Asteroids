import pygame
from utils.colors import Colors
from ui.button import Button
from utils.fonts import Fonts


class UiFactory():
  
    
    _button_size_dimension = (500, 55)
    _click_color = (200, 200, 200)
    _hover_color = (50, 50, 50)
    _text_deactivate_color = (120, 120, 120)
    
    def create_text(text:str, size:int = 35, font:pygame.font.Font = None, color:tuple = Colors.drawing_color):
        m_font = Fonts.pixel_type(size) if font == None else font
        render = m_font.render(text, False, color)
        text_render_surface = pygame.Surface(render.get_size(), pygame.SRCALPHA)
        text_render_surface.blit(render, (0, 0))
        return text_render_surface
    
    
    def create_button(text:str, on_clicked:callable, size:int = 20, is_active:bool = True, dimension:tuple = _button_size_dimension, font:pygame.font.Font = None, hover:bool = True):
        
        if font == None:
            m_font = Fonts.quantum(size)
        else:
            m_font = font
            
        if is_active:
            return Button(text, dimension = dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color= False if not hover else UiFactory._hover_color, font = m_font)
        else:
            return Button(text, dimension = dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=None, font = m_font, text_color = UiFactory._text_deactivate_color, with_sound = False)
        
        
    def make_button_list(screen:pygame.surface.Surface, items:list[Button], top:float, bottom:float, x:float):
        assert len(items) != 0 
        'Item list may not be empty!'
        for i in range(len(items)):
            position = (x, top + i * (bottom - top) / len(items) - 1)
            items[i].draw(screen, position)
        
            