from config import GlobalConfig
from constant import EXIT_GAME_EVENT, HEIGHT, START_NEW_GAME_EVENT, WIDTH, background_color, outline_color

import pygame

from pages.page_base import PageBase
from ui.uiFactory import UiFactory


class EndGameScreen(PageBase):
    
    def __init__(self, livesRemaining:int) -> None:
        
        self.livesRemaining = livesRemaining
        
       
        font = pygame.font.Font('font/quantum.ttf', 40)
        self.game_over_text = UiFactory.create_text('GAME OVER!!', font = font)
        self.continue_button = UiFactory.create_button('CONTINUE', self.continue_game)
        self.exit_button = UiFactory.create_button('EXIT', self.exit_game, 25)

    
    def draw(self, screen:pygame.surface):
        screen.fill(background_color)
        
        screen.blit(self.game_over_text, self.game_over_text.get_rect(center = (GlobalConfig.width / 2, .5 * GlobalConfig.height,)))
        # self.continue_button.draw(screen, center = (GlobalConfig.width / 2, .5 * GlobalConfig.height,))
        self.exit_button.draw(screen, center = (GlobalConfig.width / 2, .8 * GlobalConfig.height,))
        
          
    def handle_event(self, event:pygame.event.Event):
        pass
    
    def update(self, paused):
        pass
        
    
    def continue_game(self):
        if self.livesRemaining > 0:
            pygame.event.post(pygame.event.Event(START_NEW_GAME_EVENT))
        
    def exit_game(self):
        pygame.event.post(pygame.event.Event(EXIT_GAME_EVENT))
        
   