

import os
from utils.helper import Helper


class ShipConfig():
   
    max_collision_force = 50
    
    rocket_burst_rate = 5
      
    ship_size_scale = .7
    
    ship_width = 30
    
    ship_hieght = 40
    
    rocket_kick_back_range = 20
    
    rocket_kick_back_force = 4000
    
    flare_path = os.path.join(Helper.resource_path(), 'images', 'flare109.png')
    
    flame_path = os.path.join(Helper.resource_path(), 'images', 'flame101x186.png')
    

    @staticmethod
    def ship_upgrade_perks_to_completion(ship_level:int):
        min_value = 5
        max_value = 21
        return int(Helper.asymptotic_value(min_value, max_value, 0.09, ship_level))
    

    @staticmethod
    def cannon_fire_cool_down(ship_level:int):
        min_value = 1
        max_value = 2
        return Helper.asymptotic_value(min_value, max_value, 0.1, ship_level)
    


    @staticmethod
    def cannon_burst_rate(ship_level:int):
        min_value = 5
        max_value = 8
        return int(Helper.asymptotic_value(min_value, max_value, 0.09, ship_level))


    @staticmethod
    def cannon_burst_count(ship_level:int):
        min_count = 1
        max_count = 4
        return int(Helper.asymptotic_value(min_count, max_count, 0.2, ship_level))

    

    @staticmethod
    def rocket_fire_cool_down(ship_level:int):
        min_value = 0.5
        max_value = 1
        return Helper.asymptotic_value(min_value, max_value, 0.1, ship_level)

    
    # rocket_burst_rate = 5


    @staticmethod
    def rocket_burst_count(ship_level:int):
        min_p = 1
        max_p = 4
        return int(Helper.asymptotic_value(min_p, max_p, 0.13, ship_level))
        # return 2

    
    
    
    @staticmethod# movement
    def ship_max_speed(ship_level:int):
        min_p = 20
        max_p = 30
        return Helper.asymptotic_value(min_p, max_p, 0.1, ship_level)
        # return 20


    @staticmethod
    def turn_rate_degrees(ship_level:int):
        min_p = 4
        max_p = 7
        return Helper.asymptotic_value(min_p, max_p, 0.1, ship_level)
        # return 5


    @staticmethod
    def boost_force(ship_level:int):
        min_p = 500
        max_p = 700
        return Helper.asymptotic_value(min_p, max_p, 0.1, ship_level)
        # return 500

        