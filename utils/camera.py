
import numpy as np
from config.EventConfig import EventConfig
from utils.lerp import Lerp


class Camera():
    def __init__(self, duration:int, intensity:float, frequency:int) -> None:
        self.duration = duration
        self.intensity = intensity
        self.frequency = frequency
        self.lerp = None
        self._displacement = 0
        
    
    def handle_event(self, event):
        if event.type == EventConfig.shake_event:
            self.lerp = Lerp()
            
    def update(self):
        
        if self.lerp == None:
            self._displacement = 0
        else: 
            self._displacement = self.lerp.do(self.duration, self.shake_function).value
        
            
    def watch(self, pos):
        return self._displacement + np.array(list(pos))
       
            
        
    def shake_function(self, lerp:Lerp):
        displacement = lerp.sinusoidal(-self.intensity, self.intensity, self.frequency) * lerp.ease_out(1, 0)
        return displacement
        
        