class ShootingStrategy():
    def __init__(self, fireCoolDown, burstRate, burstCount, fps:int = 60):
        self.bursting = False
        self.shooting = False
        
        # frames per second
        self.FPS = fps
        
        # fire per second
        self.FIRE_COOL_DOWN = fireCoolDown
        
        # burst shots per second
        self.BURST_RATE = burstRate
        
        # how many burst per shot
        self.BURST_COUNT = burstCount
        
        
        self.burstCounter = self.FPS // self.BURST_RATE * self.BURST_COUNT
        self.fireRateCounter = 0 
        
    def canFire(self):
        if self.fireRateCounter == 0:
            self.fireRateCounter = self.FPS / self.FIRE_COOL_DOWN
            return True 
        else:
            return False
        
          
    def update(self, fireWeaponMethod:callable):
      
        if self.shooting and self.canFire():
            self.bursting = True
            
        if self.bursting:
            if self.burstCounter % (self.FPS // self.BURST_RATE) == 0:
                fireWeaponMethod()
            self.burstCounter -= 1
            
        if self.burstCounter <= 0:
            self.burstCounter = self.FPS // self.BURST_RATE * self.BURST_COUNT
            self.bursting = False
            
        if self.fireRateCounter > 0 and self.bursting == False:
            self.fireRateCounter -= 1
