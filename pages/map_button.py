
import pygame

from config import GlobalConfig
from ui.uiFactory import UiFactory


class MapButton():
    def __init__(self) -> None:
        self.background_screen = pygame.surface.Surface((GlobalConfig.width, GlobalConfig.height))
        self.boost_button = UiFactory.create_button_medium('Boost', lambda: print('up'))
        self.cannon_button = UiFactory.create_button_medium('Cannon', lambda: print('up'))
        self.rocket_button = UiFactory.create_button_medium('Rocket', lambda: print('up'))
        self.rocket_button = UiFactory.create_button_medium('Steer', lambda: print('up'))
        
    def draw(self, screen):
        pass
        
    

    
    