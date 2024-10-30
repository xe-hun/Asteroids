
import numpy as np
from constant import SHAKE_EVENT
from utils.lerp import Lerp


class Camera():
    def __init__(self, duration:int, intensity:float, frequency:int) -> None:
        self.duration = duration
        self.intensity = intensity
        self.frequency = frequency
        self.lerp = None
        
    
    def handle_event(self, event):
        if event.type == SHAKE_EVENT:
            self.lerp = Lerp()
            
    def shake(self, x:float):
        if self.lerp == None:
            return x
        
        lerp = self.lerp.do(self.duration, self.shakeFunction, x=x)
        if lerp.is_done == False:
            return lerp.value
        else:
            return x
            
    def watch(self, x):
        return np.array(list(map(self.shake, x)))
       
            
        
    def shakeFunction(self, lerp:Lerp, x):
        displacement = lerp.sinusoidal(-self.intensity, self.intensity, self.frequency) * lerp.ease_out(1, 0)
        return x + displacement
        
        