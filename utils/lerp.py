import math
import time
from utils.helper import clamp


class Lerp():
    
    def __init__(self, onDone:callable = None) -> None:
        self.startTime = None
        self.duration = None
        self.__done = False
        self.progress = 0
        self.child = None
        self.onDone = onDone
        self.value = None
        
    
    
    def drive(self):
        if self.progress >= 1:
            if self.onDone != None and self.__done == False:
                self.onDone()
                
            self.__done = True
            return False
        
        if self.startTime == None:
            self.startTime = time.time() * 1000
        
        else:
            currentTime = time.time() * 1000
            self.progress = (currentTime - self.startTime) / self.duration
            self.progress = clamp(0, 1, self.progress)
            
        return True
            
    def isDone(self):
        return self.__done
    
    def getValue(self):
        return self.value
        
            
    
    def do(self, duration:int, call:callable, onDone:callable=None, **kwargs):
        if self.duration == None:
            self.duration = duration
            
        if onDone != None:
            self.onDone = onDone
            
        if self.drive() == True:
            # self.drive()
            self.value = call(self, **kwargs)
            # self.drive()
            return Dummy(self.value)
        return self
    
    def wait(self, duration:int):
        if self.duration == None:
            self.duration = duration
            
        if self.drive() == True:
            # self.drive()
            return Dummy(None)
        return self
    
    def andThen(self, duration:int, call:callable, onDone:callable = None, **kwargs):
   
        
        if self.child == None:
            self.child = Lerp(onDone)
            self.child.duration = duration
        
        if self.child.drive() == True:
            # self.child.drive()
            self.value = call(self.child, **kwargs)
            self.child.value = self.value
            # self.child.drive()
            return Dummy(self.value)
        else:
            # self.child.value = self.value
            return self.child
    
    def andWait(self, duration:int):
        if self.child == None:
            self.child = Lerp()
            self.child.duration = duration
        
        if self.child.drive() == True:
            # self.child.value = None

            # self.child.drive()
            return Dummy(None)
        else:
            return self.child
        
          
        
    def linear(self, a, b):
        t = self.progress
        return a + (b - a) * t
    
    def easeIn(self, a, b):
        t = self.progress
        return a + (b - a) * t * t
    
    def easeOut(self, a, b):
        t = self.progress
        return a + (b - a) * (1 -  (1 - t) * (1 - t))
    
    def easeInOut(self, a, b):
        t = self.progress
        return a + (b - a) * (2 * t * t if t < .5 else 1 - 2 * (1 - t) * (1 - t))
    
    def cubicEaseIn(self, a, b):
        t = self.progress
        return a + (b - a) * t * t * t  
    
    def cubicEaseOut(self, a, b):
        t = self.progress
        return a + (b - a) *( 1 - (1 - t) *(1 - t) * (1 - t))
    
    def cubicEaseInOut(self, a, b):
        t = self.progress
        return a + (b - a) * (4 * t * t * t if t < .5 else 1 - 4 * (1 - t) * (1 - t) * (1 - t))
    
    def exponentialEaseIn(self, a, b):
        t = self.progress
        return a + (b - a) * math.pow(2, 10 * (t - 1))
    
    def exponentialEaseOut(self, a, b):
        t = self.progress
        return a + (b - a) * (1 - math.pow(2, -10 * (t - 1)))
    
    def Sinusoidal(self, a, b, f:int=1):
        t = self.progress
        return a + (b - a) * (1 - (0.5 * math.cos(2 * math.pi * f * t) + .5))
    
    # def exponentialEaseInOut(self, a, b):
    #     t = self.progress
    #     return a + (b - a) * (2 * math.pow(2, 10 * (t - 1)) if t < .5 else 1 - 2 * math.pow(2, -10 * (t - 1)))
    
    # def SinusoidalEaseIn(self, a, b):
    #     t = self.progress
    #     return a + (b - a) * (1 - math.cos(t * math.pi / 2))
    
    # def SinusoidalEaseOut(self, a, b):
    #     t = self.progress
    #     return a + (b - a) * (1 - math.sin(t * math.pi / 2))
    
    # def SinusoidalEaseInOut(self, a, b):
    #     t = self.progress
    #     return a + (b - a) * (-.5 - math.cos(math.pi * t) + .5)
    
    
    # def BackTween(self, a, b, overshoot):
    #     t = self.progress
    #     return a + (b - a) * ((t - 1) * (t - 1) * ((1.5 - overshoot) * (t - 1) - overshoot) + 1)
    
    # def BackEaseIn(self, a, b, overshoot):
    #     t = self.progress
    #     return a + (b - a) * (t  * t * ((1.5 - overshoot) * t - overshoot))
      



class Dummy():
    
    def __init__(self, value) -> None:
        self.value = value
    
    def andThen(self, *args, **kwargs):
        
        return Dummy(self.value)   
    
    def andWait(self, *args, **kwargs):
        return Dummy(self.value)   
       
    def isDone(self):
        return False
    
    def onDone(self, *args, **kwargs):
        return Dummy(self.value)   
    
    def getValue(self):
        return self.value   
