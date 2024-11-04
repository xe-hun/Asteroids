import random
from config import ControllerConfig
from controllerParameter import ControllerParameter
from utils.delay import Delay
from utils.helper import Helper


class SpawnStrategy():
    def __init__(self, spawn_asteroid:callable, spawn_rocket_perk:callable, spawn_update_perk:callable):
        self._delay = Delay()
        self._spawn_interval = 3000
        # self.CHANCES_OF_ASTEROID = LevelAdjuster.chances_of_asteroid
        # self.CHANCES_OF_ASTEROID = 
        # self.CHANCES_OF_PERK = LevelAdjuster.chances_of_perk
        # self.CHANCES_OF_ROCKET_PERK_OVER_UPGRADE_PERK = LevelAdjuster.chances_of_rocket_perk_over_upgrade_perk
        # self.BASE_GAME_TIME = LevelAdjuster.game_time()
        # self.CHANCES_OF_ASTEROID = .8
        # self.CHANCES_OF_ASTEROID = .8
        # self.CHANCES_OF_PERK = .8
        # self.CHANCES_OF_ROCKET_PERK_OVER_UPGRADE_PERK = .6
        # self.BASE_GAME_TIME = 100
        self._spawn_asteroid = spawn_asteroid
        self._spawn_rocket_perk = spawn_rocket_perk
        self._spawn_update_perk = spawn_update_perk
        

    
    def update(self, game_time, can_spawn_asteroid, game_level):
        if self._delay.delay(self._spawn_interval, reset=True).is_done:
            # can_spawn_asteroid = asteroids_alive < ControllerConfig.max_asteroid_on_screen
            
            if self._with_chance_of(ControllerParameter.chances_of_asteroid(game_level)) and can_spawn_asteroid:
                self._spawn_asteroid()
                # print(LevelParamAdjuster.chances_of_asteroid(game_level))
                
            # this value decreases as time approaches level_time
            # minimises the advantage gained when for prolonging a level
            decreasing_probability = (game_time / ControllerParameter.get_level_time(game_level))
            if self._with_chance_of(ControllerParameter.chances_of_perk * decreasing_probability):
                if self._with_chance_of(ControllerParameter.chances_of_rocket_over_upgrade):
                    self._spawn_rocket_perk()
                else:
                    self._spawn_update_perk()
  
    
    def _with_chance_of(self, percentage):
        return random.random() <= percentage