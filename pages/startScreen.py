from config.GlobalConfig import GlobalConfig
from config.EventConfig import EventConfig
from utils.fonts import Fonts
from utils.colors import Colors
import pygame
from gRouter import G_Router
from pages.mapButtonScreen import MapButtonScreen
from pages.pageBase import PageBase
from ui.uiFactory import UiFactory


class StartScreen(PageBase):
    
    def __init__(self, best_level:int, key_map:dict) -> None:
        
        self._asteroid_star = UiFactory.create_text('ASTEROID X', font = Fonts.quantum(50))
        self._asteroid_star_rect = self._asteroid_star.get_rect(center=(GlobalConfig.width / 2, 0.2 * GlobalConfig.height))
        
        self._start_game_button = UiFactory.create_button('START GAME', self._start_game, 25)
     
        self._map_button = UiFactory.create_button('MAP BUTTON', self._on_map_button, 25)
    
        self._quit_button = UiFactory.create_button('EXIT', self._quit_game, 25)        
        # font = Fonts.quantum(30)
        self.msg_score = UiFactory.create_text(f'Best Level : {best_level}', font = Fonts.quantum(30))
        # self.msg_score = font.render(f'High Score : {highScore}', False, Colors.drawing_color)
        self.msg_score_rect = self.msg_score.get_rect(center=(GlobalConfig.width / 2, 0.8 * GlobalConfig.height))
        
        self._key_map = key_map
        
 
        
    
    def draw(self, screen:pygame.surface, **kwargs):
        
      
        screen.fill(Colors.background_color)
        screen.blit(self._asteroid_star, self._asteroid_star_rect)
        # self._start_game_button.draw(screen, self._start_game_button_position)
        # self._map_button.draw(screen, self._map_button_position)
        # self._quit_button.draw(screen, self._quit_button_position)
        
        UiFactory.make_button_list(screen, [
            self._start_game_button,
            self._map_button,
            self._quit_button
        ], 
        GlobalConfig.height * .5,
        GlobalConfig.height * .8,
        GlobalConfig.width / 2
                                   )
        
        screen.blit(self.msg_score, self.msg_score_rect.topleft)
        
    
    def _start_game(self):
        pygame.event.post(pygame.event.Event(EventConfig.start_new_game_event))
        
    def _quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
    def _on_map_button(self):
        G_Router.push(MapButtonScreen(self._key_map))
        
        