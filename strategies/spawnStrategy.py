import random
from config import ControllerConfig
from utils.delay import Delay
from utils.helper import Helper


class SpawnStrategy():
    def __init__(self, spawn_asteroid:callable, spawn_rocket_perk:callable, spawn_update_perk:callable):
        self._delay = Delay()
        self._spawn_interval = 3000
        self.CHANCES_OF_ASTEROID = .8
        self.CHANCES_OF_PERK = .8
        self.CHANCES_OF_ROCKET_PERK_OVER_UPGRADE_PERK = .6
        self.BASE_GAME_TIME = 100
        self._spawn_asteroid = spawn_asteroid
        self._spawn_rocket_perk = spawn_rocket_perk
        self._spawn_update_perk = spawn_update_perk
        

    
    def update(self, game_time, game_level, asteroids_alive):
        if self._delay.delay(self._spawn_interval, reset=True).is_done:
            can_spawn_asteroid = asteroids_alive < ControllerConfig.max_asteroid_on_screen
            
            if self._with_chance_of(self.CHANCES_OF_ASTEROID) and can_spawn_asteroid:
                self._spawn_asteroid()
                
            # this value decreases as time approaches level_time
            # minimises the advantage gained when for prolonging a level
            decreasing_probability = 1 - (game_time / Helper.calculate_level_time(game_level))
        
            if self._with_chance_of(self.CHANCES_OF_PERK * decreasing_probability):
                if self._with_chance_of(self.CHANCES_OF_ROCKET_PERK_OVER_UPGRADE_PERK):
                    self._spawn_rocket_perk()
                else:
                    self._spawn_update_perk()
  
    
    def _with_chance_of(self, percentage):
        return random.random() <= percentage