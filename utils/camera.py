
from constant import SHAKE_EVENT
from utils.lerp import Lerp


class Camera():
    def __init__(self, duration:int, intensity:float, frequency:int) -> None:
        self.duration = duration
        self.intensity = intensity
        self.frequency = frequency
        self.lerp = None
        
    
    def eventUpdate(self, event):
        if event.type == SHAKE_EVENT:
            self.lerp = Lerp()
            
    def watch(self, x:float):
        if self.lerp == None:
            return x
        
        lerp = self.lerp.do(self.duration, self.shakeFunction, x=x)
        if lerp.isDone() == False:
            return lerp.getValue()
        else:
            return x
            
        
    def shakeFunction(self, lerp:Lerp, x):
        displacement = lerp.Sinusoidal(-self.intensity, self.intensity, self.frequency) * lerp.easeOut(1, 0)
        return x + displacement
        
        