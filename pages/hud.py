import pygame
from config import Colors, GlobalConfig
from constant import HEIGHT, outline_color, WIDTH
from pages.pauseScreen import PauseScreen
from ui.timedList import TimedList
from utils.effect import Effect
from gameObjects.reticle import Reticle
from gameStateController import GameStateController
from utils.progressBar import ProgressBar
from utils.helper import clamp, scale
from utils.lerp import Lerp
from utils.watcher import Watcher


class Hud():
    def __init__(self, controller:GameStateController) -> None:
        
        self._controller = controller
        level = controller.level
        
        game_font_50 = pygame.font.Font('font/quantum.ttf', 50)
        self._game_font_10 = pygame.font.Font('font/quantum.ttf', 10)
        self._game_font_40 = pygame.font.Font('font/quantum.ttf', 40)
        self._game_font_30 = pygame.font.Font('font/quantum.ttf', 30)
      
        self._m_READY_Render = game_font_50.render("READY", False, outline_color)
        
        self._m_GO_Render = game_font_50.render("GO!!", False, outline_color)
        
        self._m_STAGE_X_Render = game_font_50.render(f"STAGE {level}", False, outline_color)
        
        self._m_LEVEL_UP_Render = self._game_font_30.render("LEVELED UP!!", False, Colors.green_color)
        
        self._m_TIME_UP_Render = self._game_font_30.render(f"TIME UP!!", False, outline_color)
        self.rocket_thumbnail_surface = scale(pygame.image.load('images/rocket.png'), .5)
        
        self._penalty_bar = ProgressBar(initial_progress = 1)
        self._penalty_bar_rect = self._penalty_bar.surface.get_rect()
        
        self._perk_bar = ProgressBar(initial_progress = 0, bar_width= 100, bar_height = 10, fore_color = Colors.green_color, background_color=(51, 51, 51))
        self.perk_bar_rect = self._perk_bar.surface.get_rect()
        
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
        
        self._rocket_count_watcher = Watcher(self._on_rocket_count_change, self._controller.ship_rocket_count)
        self._perk_count_watcher = Watcher(self._on_perk_count_change, self._controller.perks_completed)
        
        self._mock_event = 0
        self._timed_list = TimedList((GlobalConfig.width * .9, GlobalConfig.height * .2), 500)
       
       
        
    def _on_rocket_count_change(self, _):
        self._rocket_count_render_effect.activate()
        
    def _on_perk_count_change(self, _):
        self._level_up_sequence_lerp = Lerp()
        self._perk_count_render_effect.activate()
        
    
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
        rect = render_scaled.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        screen.blit(render_scaled, rect)
        
    def _level_up_sequence(self, lerp:Lerp, screen):
        self._animate_sequence(lerp, screen, self._m_LEVEL_UP_Render)
            
    def _sequence1(self, lerp:Lerp, screen):
        self._animate_sequence(lerp, screen, self._m_STAGE_X_Render)
        
    def _sequence2(self, lerp:Lerp, screen):
        self._animate_sequence(lerp, screen, self._m_READY_Render)
   
        
    def _sequence3(self, lerp:Lerp, screen):
           
            self._animate_sequence(lerp, screen, self._m_GO_Render)
            
            y_up = lerp.cubic_ease_out(0, self._object_position_up)
            y_down = lerp.cubic_ease_out(HEIGHT, self._object_position_down)
            
            return y_up, y_down
        
    def _pause_game(self):
        if self._controller.game_paused:
            self._controller.game_paused = False 
        else:
            self._controller.game_paused = True
          
        
    def handle_event(self, event):
        self.reticle.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._pause_game()
                
        if event.type == pygame.MOUSEBUTTONUP:
            self._mock_event += 1
            self._timed_list.register_item(f'event {self._mock_event}')
                
      
     
        
        
    def update_penalty_bar_ship_collision(self, penalty_point):
        self._penalty_bar.lerp_progress(1 - penalty_point)
        
    def update_penalty_bar_out_of_bound(self, penalty_point):
        self._penalty_bar.set_progress(1 - penalty_point)
        
    def update_upgrade_perk_bar(self, perks_collected, perks_count):
        self._perk_bar.set_progress(perks_collected)
       
       
             
    
    def update(self):
        self._penalty_bar.update()
       
        
    def draw(self, screen):
        
        self._timed_list.draw(screen)
        
        level_time =  self._controller.level_time
        ship_rocket_count = self._rocket_count_watcher.watch(self._controller.ship_rocket_count).new_value(150)
        perks_count = self._perk_count_watcher.watch(self._controller.perks_completed).new_value(150)
        
        
        if self._start_sequence_lerp.control(self._controller.game_paused)\
            .wait(300).and_then(1000, self._sequence1, screen=screen)\
            .and_then(1000, self._sequence2, screen=screen).is_done:
                
                
            y_up, y_down = self._sequence3_lerp.control(self._controller.game_paused).do(1000, self._sequence3, lambda: self._controller.set_level_in_progress(True), screen = screen).value
                        
            
            _ , game_time_render = self._render_text(f"{level_time:02d}", self._game_font_40)
            
            perk_count_rect, perk_count_render = self._render_text(f" x {perks_count:02d}",
                                                                   self._game_font_10,
                                                                   self._perk_count_render_effect.effect_1)
            if self._perk_count_rect == None:
                self._perk_count_rect = perk_count_rect

            
            rocket_count_rect, rocket_count_render = self._render_text(f" x {ship_rocket_count:02d}",
                                                                       self._game_font_10,
                                                                       self._rocket_count_render_effect.effect_1)
            
            if self._rocket_count_rect == None:
                self._rocket_count_rect = rocket_count_rect
                 
            rocket_thumbnail_rect = self.rocket_thumbnail_surface.get_rect()
            spacing = 2
            
          
            perk_count_x_pos = self._perk_details_position[0]
            perk_count_y_pos =  y_up - self._perk_count_rect.height / 2
            
            perk_bar_x_pos =  self._perk_details_position[0] - self._perk_count_rect.width - spacing
            perk_bar_y_pos = y_up - self.perk_bar_rect.height / 2
            
            rocket_count_x_pos = perk_count_x_pos
            rocket_count_y_pos = perk_count_y_pos - self.perk_bar_rect.height - spacing - rocket_count_rect.height / 2
            
            rocket_thumbnail_x_pos = perk_bar_x_pos
            rocket_thumbnail_y_pos = perk_bar_y_pos - self.perk_bar_rect.height - spacing - rocket_thumbnail_rect.height / 2
            
            penalty_bar_x_pos = self._penalty_bar_position[0]
            penalty_bar_y_pos =  y_down - self._penalty_bar_rect.height / 2
            
            
            
            screen.blit(perk_count_render,  perk_count_render.get_rect(topright = (perk_count_x_pos, perk_count_y_pos)))
            screen.blit(self._perk_bar.surface,  self._perk_bar.surface.get_rect(topright = (perk_bar_x_pos, perk_bar_y_pos)))
            
            screen.blit(rocket_count_render,  rocket_count_render.get_rect(topright = (rocket_count_x_pos, rocket_count_y_pos)))
            screen.blit(self.rocket_thumbnail_surface,  self.rocket_thumbnail_surface.get_rect(topright = (rocket_thumbnail_x_pos, rocket_thumbnail_y_pos))) 
            
            screen.blit(game_time_render, game_time_render.get_rect(center = (self._time_text_position[0], y_up)))
                        
            screen.blit(self._penalty_bar.surface, self._penalty_bar.surface.get_rect(topright = (penalty_bar_x_pos, penalty_bar_y_pos)))   
                
            
        if self._controller.is_time_up:
            end_sequence = self._end_sequence_lerp.control(self._controller.game_paused).wait(300).and_then(1000, self.endSequence1)
            if end_sequence.is_done == False and end_sequence.value != None:
                surface, rect = end_sequence.value
                screen.blit(surface, rect)
                
        if self._level_up_sequence_lerp != None:
            self._level_up_sequence_lerp.control(self._controller.game_paused).do(1000, self._level_up_sequence, self.level_up_sequence_done, screen = screen)
    
    
    def draw_pause_screen(self, screen):
        if self._controller.game_paused:
            if self._pause_screen == None:
                self._pause_screen = PauseScreen(self._controller)
            self._pause_screen.draw(screen)
        else:
            self._pause_screen = None
            
            
    def level_up_sequence_done(self):
        self._level_up_sequence_lerp = None
    
    
    def endSequence1(self, lerp:Lerp):    
        alpha = lerp.ease_in(0, 255)
        factor = lerp.ease_in_out(1, 1.8)
        surface = scale(self._m_TIME_UP_Render, factor)
        surface.set_alpha(alpha)
        rect = surface.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        return surface, rect
    
        
        
        