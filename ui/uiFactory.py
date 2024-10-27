import pygame
from ui.button import Button


class UiFactory():
    # def __init__(self):
    #     self.game_font_20 = pygame.font.Font('font/quantum.ttf', 20)
    # color = (40, 40, 40, 0)
    
    _large_dimension = (500, 55)
    _medium_dimension = (300, 50)
    _click_color = (200, 200, 200)
    _hover_color = (50, 50, 50)
    _text_deactivate_color = (120, 120, 120)
    
    def create_button_medium(text:str, on_clicked:callable, is_active:bool = True):
        font = pygame.font.Font('font/quantum.ttf', 20)
        if is_active:
            return Button(text, dimension = UiFactory._medium_dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=UiFactory._hover_color, font = font)
        else:
            return Button(text, dimension = UiFactory._medium_dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=None, font = font, text_color = UiFactory._text_deactivate_color)
       
    def create_button_large(text:str, on_clicked:callable, is_active:bool = True):
        font = pygame.font.Font('font/quantum.ttf', 30)
        if is_active:
            return Button(text, dimension = UiFactory._large_dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=UiFactory._hover_color, font = font)
        else:
            return Button(text, dimension = UiFactory._large_dimension, on_click=on_clicked, click_color = UiFactory._click_color, hover_color=None, font = font, text_color = UiFactory._text_deactivate_color)
            