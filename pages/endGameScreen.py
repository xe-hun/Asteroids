from config.GlobalConfig import GlobalConfig
from config.EventConfig import EventConfig
from utils.fonts import Fonts
from utils.colors import Colors


import pygame

from pages.pageBase import PageBase
from ui.uiFactory import UiFactory


class EndGameScreen(PageBase):
    
    # def __init__(self, livesRemaining:int) -> None:
    def __init__(self) -> None:
        
        # self.livesRemaining = livesRemaining
        
       
        font = Fonts.quantum(40)
        self.game_over_text = UiFactory.create_text('GAME OVER!!', font = font)
        # self.continue_button = UiFactory.create_button('CONTINUE', self.continue_game)
        self.exit_button = UiFactory.create_button('EXIT', self.exit_game, 25)

    
    def draw(self, screen:pygame.surface, **kwargs):
        screen.fill(Colors.background_color)
        
        screen.blit(self.game_over_text, self.game_over_text.get_rect(center = (GlobalConfig.width / 2, .5 * GlobalConfig.height,)))
        # self.continue_button.draw(screen, center = (GlobalConfig.width / 2, .5 * GlobalConfig.height,))
        self.exit_button.draw(screen, center = (GlobalConfig.width / 2, .6 * GlobalConfig.height,))
        
          
  
    
    # def continue_game(self):
    #     if self.livesRemaining > 0:
    #         pygame.event.post(pygame.event.Event(START_NEW_GAME_EVENT))
        
    def exit_game(self):
        pygame.event.post(pygame.event.Event(EventConfig.exit_game_event))
        
   