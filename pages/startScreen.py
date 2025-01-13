import random
from config.GlobalConfig import GlobalConfig
from config.EventConfig import EventConfig
from config.MiscConfig import MiscConfig
from customEnum import ShipActions
from utils.delay import Delay
from pages.creditPage import CreditPage
from ui.timedList import TimedList
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

        self.msg_score = UiFactory.create_text(f'high score : {best_level}', font = Fonts.quantum(30))
        
        self._msg_credit = UiFactory.create_button('credit', self._on_select_credit, 18, dimension = (200, 40))

        self.msg_score_rect = self.msg_score.get_rect(center=(GlobalConfig.width / 2, 0.8 * GlobalConfig.height))
        
        self._key_map = key_map
        
        self._button_list = [
            self._start_game_button,
            self._map_button,
            self._quit_button
        ]
        
        self._credit_page = CreditPage()
        
        self._tips_timed_list = TimedList((GlobalConfig.width * .5, GlobalConfig.height * .4), item_display_duration = 5000, size = 14)
        #  font = Fonts.pixel_type(30)
        
        # pygame.time.set_timer(EventConfig.tips_timer, 5500)
        self.tips_delay = Delay()
        
        self._tips_index = 1
        
        self._tips = MiscConfig.get_game_tips(key_map)
        
        self._tips_timed_list.register_item(self._tips[0])

        
    def update(self, paused):
        
        if self.tips_delay.delay(5500, reset=True).is_done:
            self._increment_tips()
        
        self._tips_timed_list.update()
        
    def _increment_tips(self):
        self._tips_index += 1
        if self._tips_index >= len(self._tips):
            self._tips_index = 0
        self._tips_timed_list.register_item(self._tips[self._tips_index])

    def draw(self, screen:pygame.surface, **kwargs):
        
      
        screen.blit(self._asteroid_star, self._asteroid_star_rect)
     
        self._tips_timed_list.draw(screen)
       
        UiFactory.make_button_list(screen, self._button_list, 
        GlobalConfig.height * .5,
        GlobalConfig.height * .8,
        GlobalConfig.width / 2)
        
        screen.blit(self.msg_score, self.msg_score_rect.topleft)
        self._msg_credit.draw(screen, (GlobalConfig.width * .2, GlobalConfig.height * .9))
        
    
    def _start_game(self):
        pygame.event.post(pygame.event.Event(EventConfig.start_new_game_event))
        
    def _quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
    def _on_select_credit(self):
        G_Router.push(self._credit_page)
        
    def _on_map_button(self):
        G_Router.push(MapButtonScreen(self._key_map))
        
        