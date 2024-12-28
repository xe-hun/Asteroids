


from config.global_config import GlobalConfig
from config.shipConfig import ShipConfig
from constant import FPS
from utils.delay import Delay
from pages.hud import Hud


class PenaltyStrategy():
    def __init__(self, report_ship_collision:callable, report_ship_out_of_bound:callable, reset_penalty:callable):
        
        self._penalty_bar_reset_delay = None
        self._out_of_bound_delay = Delay()
        self._penalty = 0
        self._report_ship_collision = report_ship_collision
        self._report_ship_out_of_bound = report_ship_out_of_bound
        self._reset_penalty = reset_penalty
        
        
    @property
    def _penalty_point(self):
        return self._penalty
    
    @_penalty_point.setter
    def _penalty_point(self, value):
        self._penalty = min(value, 1)
        
    def penalty_active(self):
        return self._penalty_point >= 1

    
    def penalise_collision(self, penalty):
        self._penalty_bar_reset_delay = Delay()
        self._penalty_point += penalty
        self._report_ship_collision(self._penalty_point)
        
    def _penalise_out_of_bound(self, out_of_bound):
        if out_of_bound == True:
            if self._out_of_bound_delay == None:
                self._out_of_bound_delay = Delay()
                
            if self._out_of_bound_delay.delay(ShipConfig.ship_out_of_bound_delay_before_penalty).is_done:
                self._penalty_point += .1 / GlobalConfig.fps
                self._report_ship_out_of_bound(self._penalty_point)
        else:
            if self._out_of_bound_delay != None:
                self._penalty_bar_reset_delay = Delay()
                self._out_of_bound_delay = None
            
            
    def _on_penalty_lerp_reset(self, out_of_bound):
        if out_of_bound:
            return
        
        self._penalty_point = 0
        self._reset_penalty()
        
    def update(self, is_ship_out_of_bound):
        
        self._penalise_out_of_bound(is_ship_out_of_bound)
        
        if self._penalty_bar_reset_delay != None:
            # self._penalty_bar_reset_delay.delay(self.TIME_TO_RESET_PENALTY, on_done = self._on_penalty_lerp_reset, out_of_bound = ship_out_of_bound)
            self._penalty_bar_reset_delay.delay(ShipConfig.penalty_expires, on_done = self._on_penalty_lerp_reset, out_of_bound = is_ship_out_of_bound)
        
        