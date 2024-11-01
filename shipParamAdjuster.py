

import math

from utils.helper import Helper


class ShipParamAdjuster():
    
    
    # _ship_level = 1
    
    def __init__(self) -> None:
        pass
    
    # def reset(self):
    #     ShipParamAdjuster._ship_level = 1
    
    
    # def increment_ship_level():
    #     ShipParamAdjuster._ship_level += 1
        
    def upgrade_perks_per_complition(ship_level:int):
        min_p = 10
        max_p = 18
        return Helper.asymptotic_value(min_p, max_p, 0.1, ship_level)
        