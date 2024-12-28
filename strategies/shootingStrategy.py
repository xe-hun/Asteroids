from constant import FPS


class ShootingStrategy():
    def __init__(self, fire_cool_down:float, burst_rate:float, burst_count:int, report_projectile_fire:callable, projectile_type:type, fps:int = FPS):
        
        self.bursting = False
        self.shooting = False
        
        self._report_projectile_fire = report_projectile_fire
        self._projectile_type = projectile_type
        
        # frames per second
        self.FPS = fps
        
        # fire per second
        self.FIRE_COOL_DOWN = fire_cool_down
        
        # burst shots per second
        self.BURST_RATE = burst_rate
        
        # how many burst per shot
        self.BURST_COUNT = burst_count
        
        self.BURST_COUNTER_STEP = self.FPS // self.BURST_RATE * self.BURST_COUNT
        self.burst_counter = self.BURST_COUNTER_STEP
        self.fire_rate_counter = 0 
        
    def can_fire(self):
        if self.fire_rate_counter <= 0:
            self.fire_rate_counter = self.FPS / self.FIRE_COOL_DOWN
            return True 
        else:
            return False
        
          
    def update(self, penalty_active:bool, fire_weapon:callable):
        
        if penalty_active == True:
            self.shooting = False
      
        if self.shooting and self.can_fire():
            self.bursting = True
            
        if self.bursting:
            if self.burst_counter % (self.FPS // self.BURST_RATE) == 0:
                fire_weapon()
            self.burst_counter -= 1
            
        # end of burst
        if self.burst_counter <= 0:
            self._report_projectile_fire(self._projectile_type)
            self.bursting = False
            # self.burst_counter = self.FPS // self.BURST_RATE * self.BURST_COUNT
            self.burst_counter = self.BURST_COUNTER_STEP
            # disables hold to fire
            self.shooting = False
            
        if self.fire_rate_counter > 0 and self.bursting == False:
            self.fire_rate_counter -= 1
