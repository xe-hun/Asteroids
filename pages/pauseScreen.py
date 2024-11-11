import pygame
from config import Colors, EventConfig, GlobalConfig

from gameStateController import GameStateController
from pages.mapButtonScreen import MapButtonScreen
from pages.page_base import PageBase
from ui.button import Button
from ui.uiFactory import UiFactory
from utils.lerp import Lerp


class PauseScreen(PageBase):
    def __init__(self, controller:GameStateController) -> None:
        
        self._controller = controller
        self._map_button_screen = None
        
        self.transparent_screen = pygame.surface.Surface((GlobalConfig.width, GlobalConfig.height), pygame.SRCALPHA)
        
        
        self._m_CONTINUE_position = (GlobalConfig.width / 2, .3 * GlobalConfig.height)
        self._m_MUSIC_position = (GlobalConfig.width / 2, .4 * GlobalConfig.height)
        self._m_SOUND_position = (GlobalConfig.width / 2, .5 * GlobalConfig.height)
        self._m_MAP_BUTTON_position = (GlobalConfig.width / 2, .6 * GlobalConfig.height)
        self._m_QUIT_position = (GlobalConfig.width / 2, .7 * GlobalConfig.height)
        
        self._start_sequence_lerp = Lerp()
        
        self._continue_button = UiFactory.create_button('CONTINUE', self._on_continue)
        self._music_button = UiFactory.create_button('MUSIC', self._on_music_control, is_active = self._controller.music_on)
        self._sound_button = UiFactory.create_button('SOUND', self._on_sound_control, is_active = self._controller.sound_on)
        self._map_button = UiFactory.create_button('MAP BUTTON', self._on_map_button)
        self._back_button = UiFactory.create_button('BACK', self._on_back)
       
    def _on_continue(self): 
        self._controller.game_paused = False
        
    def _on_music_control(self):
        self._controller.music_on = not self._controller.music_on
        if self._controller.music_on:
            self._music_button = UiFactory.create_button('MUSIC', on_clicked=self._on_music_control)
        else:
            self._music_button = UiFactory.create_button('MUSIC', on_clicked=self._on_music_control, is_active = False)
            
    def _on_map_button(self):
        def on_back_pressed():
            self._map_button_screen = None
        self._map_button_screen = MapButtonScreen(on_back_pressed, self._controller.key_map)
            
    def _on_sound_control(self):
        self._controller.sound_on = not self._controller.sound_on
        if self._controller.sound_on:
            self._sound_button = UiFactory.create_button('SOUND', on_clicked=self._on_sound_control)
        else:
            self._sound_button = UiFactory.create_button('SOUND', on_clicked=self._on_sound_control, is_active = False)
            
        
    def _on_back(self):
         pygame.event.post(pygame.event.Event(EventConfig.exit_game_event))
        
        
    def _start_sequence(self, lerp:Lerp):
        y_continue = lerp.cubic_ease_out(0, self._m_CONTINUE_position[1])
        y_music = lerp.cubic_ease_out(0, self._m_MUSIC_position[1])
        y_sound = lerp.cubic_ease_out(0, self._m_SOUND_position[1])
        y_map_button = lerp.cubic_ease_out(0, self._m_MAP_BUTTON_position[1])
        y_quit = lerp.cubic_ease_out(0, self._m_QUIT_position[1])
        screen_alpha = lerp.cubic_ease_out(0, 230)
        
        return y_continue, y_music, y_sound, y_map_button, y_quit, screen_alpha
        
        
    def draw(self, screen):
        
        if self._map_button_screen != None:
            self._map_button_screen.draw(screen)
        else:
            y_continue, y_music, y_sound, y_map_button, y_quit, screen_alpha = self._start_sequence_lerp.do(500, self._start_sequence).value
            
            self.transparent_screen.fill(Colors.background_color)
            self.transparent_screen.set_alpha(screen_alpha)
            screen.blit(self.transparent_screen, self.transparent_screen.get_rect(topleft = (0, 0)))
            
            self._continue_button.draw(screen, (self._m_CONTINUE_position[0], y_continue))
            self._music_button.draw(screen, (self._m_MUSIC_position[0], y_music))
            self._sound_button.draw(screen, (self._m_SOUND_position[0], y_sound))
            self._map_button.draw(screen, (self._m_MAP_BUTTON_position[0], y_map_button))
            self._back_button.draw(screen, (self._m_QUIT_position[0], y_quit))
            
    def update(self, _):
        pass
    
    def handle_event(self, _):
        pass
        
       
      
     
        