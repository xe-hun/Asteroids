


from utils.helper import Helper


class ControllerConfig():

    new_level_point = 2000
    
    # params
    # base_level_time = 3
    
    # asteroids
    # asteroid_spawn_per_level = 30
    max_asteroid_on_screen = 12
    
    # perk
    upgrade_perk_completion = 10
    
    # weapons
    start_rocket_quantity = 20
    
    
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
    
    chances_of_perk = .8
    
    chances_of_rocket_over_upgrade = .65
    
    @staticmethod
    def get_level_time(game_level:int):
     
        min_level_time = 80
        max_level_time = 250
        return int(Helper.asymptotic_value(min_level_time, max_level_time, 0.1, game_level))
    
   