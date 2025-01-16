
import pygame
from config.globalConfig import GlobalConfig
from config.miscConfig import MiscConfig
from config.eventConfig import EventConfig
from utils.colors import Colors
from customEnum import ShipActions
from gRouter import G_Router
from globalResolver import GlobalResolver
from pages.pageBase import PageBase
from utils.helper import Helper
from ui.button import Button
from ui.uiFactory import UiFactory



class MapButtonScreen(PageBase):
    def __init__(self, key_map:dict) -> None:
        
        # self.is_transparent = True
        
        self._save_button_map_location = MiscConfig.map_button_save_location
        
        self.key_map = key_map
        
        self.button_to_assign = None

        self._render_key_button_labels()
        self.question_mark = UiFactory.create_text('?')
        
        self.background_screen = pygame.surface.Surface((GlobalConfig.width, GlobalConfig.height))
        self.background_screen.fill(Colors.background_color)
        
        self.button_height = 55
        button_size = (250, self.button_height)
        
        self.boost_button = UiFactory.create_button(ShipActions.Boost.name, lambda: self._assign_button(ShipActions.Boost), dimension = button_size)
        self.cannon_button = UiFactory.create_button(ShipActions.Cannon.name, lambda: self._assign_button(ShipActions.Cannon), dimension = button_size)
        self.rocket_button = UiFactory.create_button(ShipActions.Rocket.name, lambda: self._assign_button(ShipActions.Rocket), dimension = button_size)
        self.steer_button = UiFactory.create_button(ShipActions.Steer.name, lambda: self._assign_button(ShipActions.Steer), dimension = button_size)
       
        self.back_button = UiFactory.create_button('Back', self._on_go_back, dimension = button_size)
        
        
        self._left_margin = .5 * GlobalConfig.width
        self._assigning_mouse_button = False
        
    def _on_go_back(self):
        Helper.save_key_map(self._save_button_map_location, self.key_map)
        pygame.event.post(pygame.event.Event(EventConfig.save_button_map_event))
        G_Router.pop()
      
        
    def _render_key_button_labels(self):
        self.boost_key_text_render = UiFactory.create_text(self.key_map[ShipActions.Boost])
        self.cannon_key_text_render = UiFactory.create_text(self.key_map[ShipActions.Cannon])
        self.rocket_key_text_render = UiFactory.create_text(self.key_map[ShipActions.Rocket])
        self.steer_key_text_render = UiFactory.create_text(self.key_map[ShipActions.Steer])
        
        
    def _assign_button(self, action:ShipActions):
        if self._assigning_mouse_button == True:
            self._assigning_mouse_button = False
            return
        
        self.button_to_assign = action
        
        
    def handle_event(self, event:pygame.event.Event):
        if self.button_to_assign != None:
            if event.type == pygame.KEYDOWN:
                new_button = MiscConfig.button_to_event_map.get(event.key)
                self._assign_button_logic(new_button)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._assigning_mouse_button = True
                
                new_button = MiscConfig.button_to_event_map.get(f'M_{event.button}')
                self._assign_button_logic(new_button)
            
            self._render_key_button_labels()
            
    def _assign_button_logic(self, new_button):
        if new_button != None:
            old_button = self.key_map[self.button_to_assign]
            if new_button in self.key_map.values() and old_button != new_button:
                previous_key = next((k for k, v in self.key_map.items() if v == new_button), None)

                if old_button != None:
                    self.key_map[previous_key] = old_button
                
            self.key_map[self.button_to_assign] = new_button
            self.button_to_assign = None
            
    
    
    
    def draw(self, screen:pygame.surface.Surface, **kwargs):
        GlobalResolver.event_queue.add(self)
        screen.blit(self.background_screen, (0, 0))
        
        self._row_item(screen, self.boost_key_text_render, self.boost_button, .3, is_assigning = self.button_to_assign == ShipActions.Boost)
        self._row_item(screen, self.cannon_key_text_render, self.cannon_button, .4, is_assigning = self.button_to_assign == ShipActions.Cannon)
        self._row_item(screen, self.rocket_key_text_render, self.rocket_button, .5, is_assigning = self.button_to_assign == ShipActions.Rocket)
        self._row_item(screen, self.steer_key_text_render, self.steer_button, .6, is_assigning = self.button_to_assign == ShipActions.Steer)
        
        self.back_button.draw(screen, top_right = (self._left_margin, 0.7 * GlobalConfig.height))
        
        
    def _row_item(self, screen, text_surface:pygame.surface.Surface, button:Button, height_ratio:float, is_assigning:bool = False):
        spacing = 100
        button.draw(screen, top_right = (self._left_margin, height_ratio * GlobalConfig.height,))
        if is_assigning:
            screen.blit(self.question_mark, text_surface.get_rect(topleft = (self._left_margin + spacing,  height_ratio * GlobalConfig.height + self.button_height / 2)))
        else:
            screen.blit(text_surface, text_surface.get_rect(topleft = (self._left_margin + spacing,  height_ratio * GlobalConfig.height + self.button_height / 2)))
    

    
    