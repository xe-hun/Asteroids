from config import Colors, EventConfig, GlobalConfig
import pygame
from ui.uiFactory import UiFactory


class StartScreen():
    
    def __init__(self, highScore:int) -> None:
        
        
        self._text_start_game = UiFactory.create_button_large('START GAME', self._start_game)
        self._text_start_game_position = (GlobalConfig.width / 2, .4 * GlobalConfig.height)
     
        
        self._text_quit = UiFactory.create_button_large('QUIT', self._quit_game)
        self._text_quit_position = (GlobalConfig.width / 2, 0.5 * GlobalConfig.height)
        
        font = pygame.font.Font('font/quantum.ttf', 30)
        self.msg_score = font.render(f'High Score : {highScore}', False, Colors.drawing_color)
        self.msg_score_rect = self.msg_score.get_rect(center=(GlobalConfig.width / 2, 0.8 * GlobalConfig.height))
    
    def draw(self, screen:pygame.surface):
        screen.fill(Colors.background_color)
        self._text_start_game.draw(screen, self._text_start_game_position)
        self._text_quit.draw(screen, self._text_quit_position)
        screen.blit(self.msg_score, self.msg_score_rect)
        
    def handleEvents(self, event:pygame.event.Event):
        pass
     
    
    def _start_game(self):
        pygame.event.post(pygame.event.Event(EventConfig.start_new_game_event))
        
    def _quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        