import pygame
from config.global_config import GlobalConfig
from config.rocket_config import RocketConfig
from soundController import SoundController
from utils.fonts import Fonts
from utils.colors import Colors
from ui.uiFactory import UiFactory
from utils.effect import Effect
from gameObjects.reticle import Reticle
from utils.progressBar import ProgressBar
from utils.helper import clamp, scale
from utils.lerp import Lerp
from utils.watcher import Watcher


class Hud():
    def __init__(self, game_level:int, ship_rocket_count:int, ship_level:int, ship_upgrade_perk_collected:int) -> None:
       
        game_font_50 = Fonts.quantum(50)
        self._game_font_10 = Fonts.quantum(10)
        self._game_font_40 = Fonts.quantum(40)
        game_font_30 = Fonts.quantum(30)
      
        self._m_READY_Render = UiFactory.create_text('READY', font = game_font_50)
        
        self._m_Go_Render = UiFactory.create_text('GO!!', font = game_font_50)
        
        self._m_STAGE_X_Render = UiFactory.create_text(f"STAGE {game_level}", font = game_font_50)
      
        self._m_LEVEL_UP_Render = UiFactory.create_text(f"LEVELED UP !!", font = game_font_30, color = Colors.green_color)
        
        self._m_TIME_UP_Render = UiFactory.create_text(f"TIME UP !!", font = game_font_30)
        
        self.rocket_thumbnail_surface = scale(pygame.image.load(RocketConfig.image_path), .5)
        
        self._penalty_bar = ProgressBar(initial_progress = 1)
        self._penalty_bar_rect = self._penalty_bar.surface.get_rect()
        
        self._ship_level_bar = ProgressBar(initial_progress = ship_upgrade_perk_collected, bar_width= 100, bar_height = 10, fore_color = Colors.green_color, background_color=(51, 51, 51))
        self._ship_level_bar_rect = self._ship_level_bar.surface.get_rect()
        
        self._object_position_up = 0.1 * GlobalConfig.height
        self._object_position_down = 0.9 * GlobalConfig.height
        right_margin = 0.97 * GlobalConfig.width
        
        self._time_text_position = (0.5 * GlobalConfig.width, self._object_position_up)
        
        self._perk_details_position = (right_margin, self._object_position_up)
        self._rocket_details_position = (right_margin, self._object_position_up)
      
        self._rocket_thumbnail_position = (right_margin, self._object_position_up)
        
        self._penalty_bar_position = (right_margin, self._object_position_down)
        
        self._rocket_count_rect = None
        self._perk_count_rect = None

        self._start_sequence_lerp = Lerp()
        self._end_sequence_lerp = Lerp()
        self._sequence3_lerp = Lerp()
        self._level_up_sequence_lerp = None
        
        self.reticle = Reticle()
        self._rocket_count_render_effect = Effect()
        self._perk_count_render_effect = Effect()
        
        self._pause_screen = None
        
        self._rocket_count_watcher = Watcher(self._on_rocket_count_change, ship_rocket_count)
        self._ship_level_watcher = Watcher(self._on_ship_level_change, ship_level)
        self._upgrade_perk_collected_watcher = Watcher(self._on_upgrade_perk_collected_change, ship_upgrade_perk_collected)
        
     
        # self._timed_list = TimedList((GlobalConfig.width * .9, GlobalConfig.height * .2), 500)
       
       
    def _on_rocket_count_change(self, _):
        self._rocket_count_render_effect.activate()
        
    def _on_ship_level_change(self, _):
        self._level_up_sequence_lerp = Lerp()
        self._perk_count_render_effect.activate()
        SoundController.achievement_channel().play(SoundController.level_up_sound)
        
    def _on_upgrade_perk_collected_change(self, value):
        self._ship_level_bar.set_progress(value)
        
    
    def _render_text(self, text, font:pygame.font.Font, effect:callable = None):
        surface = font.render(text, False, Colors.drawing_color)
        if effect == None:
            s = surface
        else:
            s = effect(surface, 500, off_color=Colors.drawing_color, on_color=Colors.green_color)
            
        rect = s.get_rect()
        return rect, s
        
   
    def _animate_sequence(self, lerp:Lerp, screen:pygame.surface.Surface, surface:pygame.surface.Surface):
        scale_factor = lerp.ease_in(1, 1.5)
        
        alpha = lerp.sinusoidal(0, 400)
        alpha = clamp(0, 255, alpha)
        
        surface.set_alpha(alpha)
        render_scaled = scale(surface, scale_factor)        
        rect = render_scaled.get_rect(center = (GlobalConfig.width / 2, GlobalConfig.height / 2))
        screen.blit(render_scaled, rect)
        
        
    def _level_up_sequence(self, lerp:Lerp, screen):
        self._animate_sequence(lerp, screen, self._m_LEVEL_UP_Render)
        
            
    def _sequence1(self, lerp:Lerp, screen):
        self._animate_sequence(lerp, screen, self._m_STAGE_X_Render)
        
        
    def _sequence2(self, lerp:Lerp, screen):
        self._animate_sequence(lerp, screen, self._m_READY_Render)
   
        
    def _sequence3(self, lerp:Lerp, screen):   
            self._animate_sequence(lerp, screen, self._m_Go_Render)
            
            y_up = lerp.cubic_ease_out(0, self._object_position_up)
            y_down = lerp.cubic_ease_out(GlobalConfig.height, self._object_position_down)
            
            return y_up, y_down
        
        
    # def _pause_game(self, on_game_paused:callable):
    #     on_game_paused()
          
          
  
        
    def handle_event(self, event):
        self.reticle.handle_event(event)
        
      
                # self._pause_game()
        
      
     
        
        
    def update_penalty_bar_ship_collision(self, penalty_point):
        self._penalty_bar.lerp_progress(1 - penalty_point)
        
    def update_penalty_bar_out_of_bound(self, penalty_point):
        self._penalty_bar.set_progress(1 - penalty_point)
        
    # def update_upgrade_perk_bar(self, perks_collected, perks_count):
    #     self._perk_bar.set_progress(perks_collected)
    
    def update(self):
        self._penalty_bar.update()
        
    def draw(self, screen, level_time:int, ship_rocket_count:int, ship_level:int, ship_upgrade_perk_collected:int, game_paused:bool, is_time_up:bool, set_level_in_progress:callable):
        
       
        
        # level_time =  level_time
        rocket_count = self._rocket_count_watcher.watch(ship_rocket_count).new_value(150)
        level_count = self._ship_level_watcher.watch(ship_level).new_value(150)
        self._upgrade_perk_collected_watcher.watch(ship_upgrade_perk_collected)
        
        
        if self._start_sequence_lerp.control(game_paused)\
            .wait(300).and_then(1000, self._sequence1, screen=screen)\
            .and_then(1000, self._sequence2, screen=screen).is_done:
                
                
            y_up, y_down = self._sequence3_lerp.control(game_paused).do(1000, self._sequence3, set_level_in_progress, screen = screen).value
                            
            _ , game_time_render = self._render_text(f"{level_time:02d}", self._game_font_40)
            
            perk_count_rect, perk_count_render = self._render_text(f" x {level_count:02d}",
                                                                   self._game_font_10,
                                                                   self._perk_count_render_effect.effect_1)
            if self._perk_count_rect == None:
                self._perk_count_rect = perk_count_rect

            
            rocket_count_rect, rocket_count_render = self._render_text(f" x {rocket_count:02d}",
                                                                       self._game_font_10,
                                                                       self._rocket_count_render_effect.effect_1)
            
            if self._rocket_count_rect == None:
                self._rocket_count_rect = rocket_count_rect
                 
            rocket_thumbnail_rect = self.rocket_thumbnail_surface.get_rect()
            spacing = 2
            
          
            perk_count_x_pos = self._perk_details_position[0]
            perk_count_y_pos =  y_up - self._perk_count_rect.height / 2
            
            perk_bar_x_pos =  self._perk_details_position[0] - self._perk_count_rect.width - spacing
            perk_bar_y_pos = y_up - self._ship_level_bar_rect.height / 2
            
            rocket_count_x_pos = perk_count_x_pos
            rocket_count_y_pos = perk_count_y_pos - self._ship_level_bar_rect.height - spacing - rocket_count_rect.height / 2
            
            rocket_thumbnail_x_pos = perk_bar_x_pos
            rocket_thumbnail_y_pos = perk_bar_y_pos - self._ship_level_bar_rect.height - spacing - rocket_thumbnail_rect.height / 2
            
            penalty_bar_x_pos = self._penalty_bar_position[0]
            penalty_bar_y_pos =  y_down - self._penalty_bar_rect.height / 2
            
            
            
            screen.blit(perk_count_render,  perk_count_render.get_rect(topright = (perk_count_x_pos, perk_count_y_pos)))
            screen.blit(self._ship_level_bar.surface,  self._ship_level_bar.surface.get_rect(topright = (perk_bar_x_pos, perk_bar_y_pos)))
            
            screen.blit(rocket_count_render,  rocket_count_render.get_rect(topright = (rocket_count_x_pos, rocket_count_y_pos)))
            screen.blit(self.rocket_thumbnail_surface,  self.rocket_thumbnail_surface.get_rect(topright = (rocket_thumbnail_x_pos, rocket_thumbnail_y_pos))) 
            
            screen.blit(game_time_render, game_time_render.get_rect(center = (self._time_text_position[0], y_up)))
                        
            screen.blit(self._penalty_bar.surface, self._penalty_bar.surface.get_rect(topright = (penalty_bar_x_pos, penalty_bar_y_pos)))   
                
            
        if is_time_up:
            end_sequence = self._end_sequence_lerp.control(game_paused).wait(300).and_then(1000, self.endSequence1)
            if end_sequence.is_done == False and end_sequence.value != None:
                surface, rect = end_sequence.value
                screen.blit(surface, rect)
                
        if self._level_up_sequence_lerp != None:
            self._level_up_sequence_lerp.control(game_paused).do(1000, self._level_up_sequence, self.level_up_sequence_done, screen = screen)
    
    
  
            
            
    def level_up_sequence_done(self):
        self._level_up_sequence_lerp = None
    
    
    def endSequence1(self, lerp:Lerp):    
        alpha = lerp.ease_in(0, 255)
        factor = lerp.ease_in_out(1, 1.8)
        surface = scale(self._m_TIME_UP_Render, factor)
        surface.set_alpha(alpha)
        rect = surface.get_rect(center = (GlobalConfig.width / 2, GlobalConfig.height / 2))
        return surface, rect
    
        
        
        