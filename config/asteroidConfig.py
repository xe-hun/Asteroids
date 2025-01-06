import random
from utils.helper import Helper


class AsteroidConfig():

    min_size = 8
    min_life = 1
        

    @staticmethod
    def max_size(game_level:int):
        min_val = 20
        max_val = 30
        return Helper.asymptotic_value(min_val, max_val, 0.1, game_level)
     

    


    @staticmethod
    def max_life(game_level:int):
        min_val = 2
        max_val = 6
        return int(Helper.asymptotic_value(min_val, max_val, 0.1, game_level))
   
        
    @staticmethod
    def get_break_parts(game_level:int):
        choice_1 = int(Helper.asymptotic_value(10, 0, .7, game_level))
        return random.choices([0, 2, 3, ],[choice_1, 10, 3])[0]

    # @staticmethod
    # def min_sides(game_level:int):
    #     min_val = .6
    #     max_val = .9
    #     return Helper.asymptotic_value(min_val, max_val, 0.1, game_level)
    #     return 7

    # @staticmethod
    # def max_sides(game_level:int):
    #     min_val = .6
    #     max_val = .9
    #     return Helper.asymptotic_value(min_val, max_val, 0.1, game_level)
    #     return 12

    
    min_speed = .5
    max_speed = 1.2
    min_initial_angular_velocity = 2
    max_initial_angular_velocity = 7
    
        


    