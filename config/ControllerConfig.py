


from utils.helper import Helper


class ControllerConfig():

    new_level_point = 2000
    
    asteroid_destroyed_point = 100
    
    max_asteroid_on_screen = 12
  
    start_rocket_quantity = 20
    start_game_level = 1
    start_ship_level = 1
    
    
    chances_of_perk = .8
    chances_of_rocket_over_upgrade = .65
    
    
    @staticmethod
    def get_bonus_time(level_time):
        return min(level_time // 2, 30)
    
    @staticmethod
    def chances_of_asteroid(game_level:int):
        min_chance = .75
        max_chance = .9
        return Helper.asymptotic_value(min_chance, max_chance, 0.2, game_level)
    
    @staticmethod
    def asteroid_spawn_per_level(game_level:int):
        min_qty = 20
        max_qty = 55
        return int(Helper.asymptotic_value(min_qty, max_qty, 0.1, game_level))
    
    @staticmethod
    def get_level_time(game_level:int):
     
       
        min_level_time = 110
        max_level_time = 200
        return int(Helper.asymptotic_value(min_level_time, max_level_time, 0.1, game_level))
    
   