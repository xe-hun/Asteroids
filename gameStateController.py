import pygame

from Activity import Activity
from config import ControllerConfig, EventConfig
from constant import END_GAME_EVENT, START_NEW_GAME_EVENT
from gameObjects.rocket import Rocket
from utils.helper import Helper
from utils.delay import Delay


class GameStateController():
    def __init__(self) -> None:
        self.ASTEROID_DESTROYED_POINT = 100
        self.NEW_LEVEL_POINT = ControllerConfig.new_level_point
        # self.LEVEL_TIME = ControllerConfig.level_time
        self.START_LIVES = 2
        self.PERKS_PER_COMPLETION = ControllerConfig.upgrade_perk_completion
        self.reset_game()
        
        self._high_score = 0
        self._game_score_counter = 0
        self._asteroid_spawn_per_level = ControllerConfig.asteroid_spawn_per_level
        self.music_on = False
        self.sound_on = False
        
        
     
        # self.resetGame = False
        self.delay_before_new_level = Delay()
        self.counter_delay = Delay()
        self._upgrade_perk_collected = 0
        self._upgrade_perk_completed = 0
        self._ship_rocket_count = ControllerConfig.rocket_base_quantity
        
        self._game_paused = False
        
    def _score_update(self):
        
        def update():
             self._game_score_counter += counter_step
        
        # update the highScore
        if self._game_score > self._high_score:
            self._high_score = self._game_score
            
        counter_step = int((self._game_score - self._game_score_counter) / 50)
        
        if self._game_score_counter <= self._game_score:
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
    
    @property
    def lives_remaining(self):
        return self._lives_remaining
    
    @property
    def game_score_counter(self):
        return self._game_score_counter   
    
    @property
    def ship_rocket_count(self):
        return self._ship_rocket_count   
    
    @property
    def upgrade_perk_completed(self):
        return self._upgrade_perk_completed   
    
    @property
    def upgrade_perk_collected(self):
        return self._upgrade_perk_collected
    
    @property
    def level(self):
        return self._level
    
    @property
    def high_score(self):
        return self._high_score    
          
    @property  
    def is_time_up(self):
        return self._level_time <= 0 
    
    def goto_new_level(self):
        self._level += 1
        self._game_score += self.NEW_LEVEL_POINT
        self.reset_level(self._level)
        pygame.event.post(pygame.event.Event(EventConfig.start_new_game_event))
        
    def reset_level(self, level):
        # self.asteroids_remaining = float('inf')
        self._asteroid_spawned = 0
        self._level_time = Helper.calculate_level_time(level)
        self._level_in_progress = False
        
    def reset_game(self):
        self._number_of_asteroids_destroyed = 0
        self._level = 1
        self._lives_remaining = self.START_LIVES
        self._game_score = 0
        self._game_paused = False
        self.reset_level(self._level)
      

        
    @property
    def level_is_in_progress_and_game_not_paused(self):
        return self.level_is_in_progress and not self.game_paused
    
    def asteroid_spawn_complete(self):
        return self._asteroid_spawned >= self._asteroid_spawn_per_level
    
    def game_time_pulse(self):
        # if self.level_is_in_progress and not self.game_paused:
        if self.level_is_in_progress_and_game_not_paused:
            self._level_time -= 1
    
    def report_asteroid_spawned(self):
        self._asteroid_spawned += 1
            
    # def _get_asteroid_remaining(self, remaining):
    #     self.asteroids_remaining = remaining
        
    def report_upgrade_perk_collected(self):
        self._upgrade_perk_collected += 1/self.PERKS_PER_COMPLETION
        if self._upgrade_perk_collected >= 1:
            self._upgrade_perk_collected = 0
            self._upgrade_perk_completed += 1
            
        return Activity.upgrade_collected()
        
        # return self._perks_collected, self._perks_completed
    
    def report_rocket_perk_collected(self):
        self._ship_rocket_count += 1
        return Activity.rocket_collected(1)
    
        
    
    def report_asteroid_destroyed(self):
        self._number_of_asteroids_destroyed += 1
        # self._game_score += self.ASTEROID_DESTROYED_POINT
        
    def report_projectile_fired(self, projectile_type:type):
        if projectile_type == Rocket:
            self._ship_rocket_count -= 1
            
    def report_rocket_perk_spawned(self):
        pass
    
    def report_upgrade_perk_spawned(self):
        pass
            
    def update(self, asteroids_alive):
        
        
        if self.game_paused:
            return
        
        # self._get_asteroid_remaining(numAsteroids)
        
        self._score_update()
        
        if self.asteroid_spawn_complete() and asteroids_alive == 0:
            self.set_level_in_progress(False)
            self.delay_before_new_level.delay(2000, self.goto_new_level, True)
                
        if self.is_time_up:
            self.set_level_in_progress(False)
            self.delay_before_new_level.delay(2000, self.game_over, True)
         
    @property       
    def game_paused(self):
        return self._game_paused
    
    @game_paused.setter
    def game_paused(self, value:bool):
        self._game_paused = value
        # self._level_in_progress = not value
        
                
            
    def game_over(self):
        self.reset_level(self.level)
        self._lives_remaining -= 1
        pygame.event.post(pygame.event.Event(EventConfig.end_game_event))
        