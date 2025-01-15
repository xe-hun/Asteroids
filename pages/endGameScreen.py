
   
from config.GlobalConfig import GlobalConfig
from config.EventConfig import EventConfig
from utils.effect import Effect
from utils.fonts import Fonts
from utils.colors import Colors


import pygame

from pages.pageBase import PageBase
from ui.uiFactory import UiFactory


class EndGameScreen(PageBase):
    
    def __init__(self, new_high_score:int = None) -> None:
        
        
       
        font = Fonts.quantum(40)
        self.game_over_text = UiFactory.create_text('GAME OVER!!', font = Fonts.quantum(40))
        self._new_high_score = new_high_score
        if self._new_high_score != None:
            self._new_high_score_label = UiFactory.create_text(f'NEW HIGH-SCORE!!', font = Fonts.quantum(25))
            
              
        self._exit_button = UiFactory.create_button('EXIT', self.exit_game, 25)
        
        self._effect = Effect()
        self._effect.activate()

    
    def draw(self, screen:pygame.surface, **kwargs):
        screen.fill(Colors.background_color)
        
        screen.blit(self.game_over_text, self.game_over_text.get_rect(center = (GlobalConfig.width / 2, .5 * GlobalConfig.height,)))
        
        if self._new_high_score != None:
            screen.blit(self._new_high_score_label, self._new_high_score_label.get_rect(center = (GlobalConfig.width / 2, .3 * GlobalConfig.height,)))
            self._new_high_score_value = UiFactory.create_text(f'{self._new_high_score}', font = Fonts.quantum(25), color = self._effect.alternate_color(1500))
            
            screen.blit(self._new_high_score_value, self._new_high_score_value.get_rect(center = (GlobalConfig.width / 2, .4 * GlobalConfig.height,)))
            
     
        self._exit_button.draw(screen, center = (GlobalConfig.width / 2, .6 * GlobalConfig.height,))
        
       
        
    def exit_game(self):
        pygame.event.post(pygame.event.Event(EventConfig.exit_game_event))
        
   