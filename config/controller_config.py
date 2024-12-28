


from utils.helper import Helper


class ControllerConfig():

    new_level_point = 2000
    
    max_asteroid_on_screen = 12
  
    start_rocket_quantity = 20
    start_game_level = 1
    start_ship_level = 1
    
    
    chances_of_perk = .8
    chances_of_rocket_over_upgrade = .65
    
    
    @staticmethod
    def get_bonus_time(level_time):
        return level_time // 3
    
    @staticmethod
    def chances_of_asteroid(game_level:int):
        min_chance = .6
        max_chance = .9
        return Helper.asymptotic_value(min_chance, max_chance, 0.1, game_level)
    
    @staticmethod
    def asteroid_spawn_per_level(game_level:int):
        min_qty = 15
        # min_qty = 3
        max_qty = 40
        # max_qty = 4
        return int(Helper.asymptotic_value(min_qty, max_qty, 0.2, game_level))
    
    @staticmethod
    def get_level_time(game_level:int):
     
        min_level_time = 100
        max_level_time = 250
        return int(Helper.asymptotic_value(min_level_time, max_level_time, 0.1, game_level))
    
   