from config import Colors, EventConfig, GlobalConfig
import pygame
from gRouter import G_Router
from pages.mapButtonScreen import MapButtonScreen
from pages.page_base import PageBase
from ui.uiFactory import UiFactory


class StartScreen(PageBase):
    
    def __init__(self, highScore:int, key_map:dict) -> None:
        
        
        self._text_start_game = UiFactory.create_button('START GAME', self._start_game, 30)
        self._text_start_game_position = (GlobalConfig.width / 2, .4 * GlobalConfig.height)
     
        self._text_map_button = UiFactory.create_button('MAP BUTTON', self._on_map_button, 30)
        self._text_map_button_position = (GlobalConfig.width / 2, 0.5 * GlobalConfig.height)
        
        self._text_quit = UiFactory.create_button('QUIT', self._quit_game, 30)
        self._text_quit_position = (GlobalConfig.width / 2, 0.6 * GlobalConfig.height)
        
        font = pygame.font.Font('font/quantum.ttf', 30)
        self.msg_score = font.render(f'High Score : {highScore}', False, Colors.drawing_color)
        self.msg_score_rect = self.msg_score.get_rect(center=(GlobalConfig.width / 2, 0.8 * GlobalConfig.height))
        
        self._key_map = key_map
        
 
        
    
    def draw(self, screen:pygame.surface):
        
      
        screen.fill(Colors.background_color)
        self._text_start_game.draw(screen, self._text_start_game_position)
        self._text_map_button.draw(screen, self._text_map_button_position)
        self._text_quit.draw(screen, self._text_quit_position)
        screen.blit(self.msg_score, self.msg_score_rect)
        
    
    def _start_game(self):
        pygame.event.post(pygame.event.Event(EventConfig.start_new_game_event))
        
    def _quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
    def _on_map_button(self):
        G_Router.push(MapButtonScreen(self._key_map))
        
        