import pygame

from Activity import Activity
from config.globalConfig import GlobalConfig
from config.miscConfig import MiscConfig
from config.eventConfig import EventConfig
from config.controllerConfig import ControllerConfig
from gameObjects.rocket import Rocket
from config.controllerConfig import ControllerConfig
from gRouter import G_Router
from config.shipConfig import ShipConfig
from model.save_data_model import SaveDataModel
from soundController import SoundController
from utils.helper import Helper
from utils.delay import Delay


class GameStateController():
    def __init__(self) -> None: 
        
        self._bonus_time = 0
        self._level_time = 0
        self._number_of_asteroids_destroyed = 0
        self._game_level = ControllerConfig.start_game_level
        # self._ship_level = 10
        self._ship_level = ControllerConfig.start_ship_level
      
        # self._lives_remaining = self.START_LIVES
        self._game_score = ControllerConfig.new_level_point
        self._game_paused = False
        self._set_new_level_parameters()
        
   
        self._game_score_counter = 0
        SoundController.set_music(True)
        SoundController.set_sound_effect(True)
        SoundController.set_sound_of_space(False)
        
   
        self.delay_before_new_level = Delay()
        self.counter_delay = Delay()
        self._upgrade_perk_collected = 0
       
        self._ship_rocket_count = ControllerConfig.start_rocket_quantity
        
        self._game_paused = False
        self._load_config()
        
        self._new_high_score = None
        
       
    def _load_config(self):        
        key_map = Helper.load_key_map(MiscConfig.map_button_save_location) 
        self.key_map = key_map if key_map != None else MiscConfig.default_key_map
        
        saved_data = Helper.load_data(MiscConfig.saved_data_location, GlobalConfig.key)
        self._saved_data = SaveDataModel.from_dict(saved_data)
        

    def _score_update(self):
        def update():
             self._game_score_counter += counter_step
        
        # update the highScore
        if self._game_score > self.high_score:
            self._new_high_score = self.high_score = self._game_score
            

            
        counter_step = int((self._game_score - self._game_score_counter) / 50)
        
        if self._game_score_counter < self._game_score:
            self.counter_delay.delay(100, on_done=update,  reset=True)
        else:
            self._game_score_counter = self._game_score
        
    def set_level_in_progress(self, value):
        self._level_in_progress = value
     
        
    @property
    def level_is_in_progress(self):
        return self._level_in_progress
        
    @property
    def level_time(self):
        return self._level_time
    
    # @property
    # def lives_remaining(self):
    #     return self._lives_remaining
    
    @property
    def game_score_counter(self):
        return self._game_score_counter   
    
    @property
    def ship_rocket_count(self):
        return self._ship_rocket_count   
    
    @property
    def rocket_empty(self):
        return self.ship_rocket_count <= 0
    
    
    @property
    def ship_upgrade_perk_collected(self):
        return self._upgrade_perk_collected
    
    @property
    def game_level(self):
        return self._game_level
    
    @property
    def ship_level(self):
        return self._ship_level
    
    @property
    def high_score(self):
        return self.saved_data.high_score    
    
    @high_score.setter
    def high_score(self, value):
        self.saved_data.high_score = value
      
    @property
    def saved_data(self):
        return self._saved_data    
          
    @property  
    def is_time_up(self):
        return self._level_time <= 0 
    
    # def set_bonus_time(self, value):
    #     self._bonus_time = value
    
    def _goto_new_level(self):
        pygame.event.post(pygame.event.Event(EventConfig.start_new_game_event))
        self._game_level += 1
        self._game_score += ControllerConfig.new_level_point
        self._set_new_level_parameters()
       
        
    def _set_new_level_parameters(self):
        self._asteroid_spawned = 0
        self._bonus_time = ControllerConfig.get_bonus_time(self._level_time)
        self._game_score += self._bonus_time * 10
        self._level_time = ControllerConfig.get_level_time(self.game_level) + self._bonus_time
        # + self._bonus_time
        self.set_level_in_progress(False)
      
    @property
    def bonus_time_activity(self):
        if self._bonus_time <= 0:
            return None
        else: return Activity.bonus_time_added(self._bonus_time)
        
    @property
    def level_is_in_progress_and_game_not_paused(self):
        return self.level_is_in_progress and not self.game_paused
    
    # @property
    # def level_completed(self):
    #     return self.asteroid_spawn_complete and self.asteroids_alive == 0
    
    @property
    def asteroid_spawn_complete(self):
        # return self._asteroid_spawned >= self._asteroid_spawn_per_level
        return self._asteroid_spawned >= ControllerConfig.asteroid_spawn_per_level(self.game_level)
    
    def _game_time_pulse(self):
        # if self.level_is_in_progress and not self.game_paused:
        if self.level_is_in_progress_and_game_not_paused:
            self._level_time -= 1
    
    def report_asteroid_spawned(self):
        self._asteroid_spawned += 1
            
        
    def report_upgrade_perk_collected(self):
        # self._upgrade_perk_collected += 1/self.PERKS_PER_COMPLETION
        self._upgrade_perk_collected += 1/ShipConfig.ship_upgrade_perks_to_completion(self.ship_level)
        if self._upgrade_perk_collected >= 1:
            self._upgrade_perk_collected = 0
            self._ship_level += 1
            
        return Activity.upgrade_collected()
        
        
    def report_rocket_perk_collected(self):
        self._ship_rocket_count += 1
        return Activity.rocket_collected(1)
    
    
    def report_asteroid_destroyed(self):
        self._number_of_asteroids_destroyed += 1
        self._game_score += ControllerConfig.asteroid_destroyed_point

        
    def report_projectile_fired(self, projectile_type:type):
        if projectile_type == Rocket:
            self._ship_rocket_count -= 1
            
    def report_rocket_perk_spawned(self):
        pass
    
    def report_upgrade_perk_spawned(self):
        pass
            
    def update(self, level_completed):
        
        if self.game_paused:
            return
        
        if self.level_is_in_progress:
            self._score_update()
        
       
        if level_completed:
            self.set_level_in_progress(False)
            self.delay_before_new_level.delay(2000, self._goto_new_level, True)
                
        if self.is_time_up:
            self.set_level_in_progress(False)
            self.delay_before_new_level.delay(2000, self._game_over, True)
         
    @property       
    def game_paused(self):
        return self._game_paused
    
    @game_paused.setter
    def game_paused(self, value:bool):
        self._game_paused = value
        G_Router.game_paused = value
        # self._level_in_progress = not value
        
                
            
    def _game_over(self):
        self._set_new_level_parameters()
        # self._lives_remaining -= 1
        pygame.event.post(pygame.event.Event(EventConfig.end_game_event, new_high_score = self._new_high_score))
        
        
    def handle_event(self, event):
        
        if event.type == EventConfig.time_timer:
            self._game_time_pulse()
        
        if event.type == EventConfig.save_button_map_event:
            self._load_config()