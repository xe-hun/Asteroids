


from constant import FPS
from utils.delay import Delay
from pages.hud import Hud


class PenaltyStrategy():
    def __init__(self, hud:Hud):
        self.TIME_TO_RESET_PENALTY = 4000
        self._penalty_bar_reset_delay = None
        self._out_of_bound_delay = Delay()
        self._penalty = 0
        self._hud = hud
        
    @property
    def _ship_penalty_point(self):
        return self._penalty
    
    @_ship_penalty_point.setter
    def _ship_penalty_point(self, value):
        self._penalty = min(value, 1)

    
    def penalise_collision(self, penalty):
        self._penalty_bar_reset_delay = Delay()
        self._ship_penalty_point += penalty
        self._hud.update_penalty_bar_ship_collision(self._ship_penalty_point)
        
    def _penalise_out_of_bound(self, out_of_bound):
        if out_of_bound == True:
            if self._out_of_bound_delay == None:
                self._out_of_bound_delay = Delay()
                
            if self._out_of_bound_delay.delay(2000).is_done:
                self._ship_penalty_point += .1 / FPS
                self._hud.update_penalty_bar_out_of_bound(self._ship_penalty_point)
        else:
            if self._out_of_bound_delay != None:
                self._penalty_bar_reset_delay = Delay()
                self._out_of_bound_delay = None
            
            
    def _on_penalty_lerp_reset(self, out_of_bound):
        if out_of_bound:
            return
        
        self._ship_penalty_point = 0
        self._hud.update_penalty_bar_ship_collision(0)
        
    def update(self, ship_out_of_bound):
        
        self._penalise_out_of_bound(ship_out_of_bound)
        
        if self._penalty_bar_reset_delay != None:
            self._penalty_bar_reset_delay.delay(self.TIME_TO_RESET_PENALTY, on_done = self._on_penalty_lerp_reset, out_of_bound = ship_out_of_bound)
        
        