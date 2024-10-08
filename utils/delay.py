import math
import time
from utils.helper import clamp


class Delay():
    
    def __init__(self) -> None:
        # self.progress = 0
        # self.isDone = True
        # self.startTime = None
        self.reset()
        pass
        
    def delay(self, duration:int, onDone:callable = None, reset:bool = False, **kwargs):
        
        if self.progress >= 1 :
            if onDone:
                onDone(**kwargs)
            if reset:
                self.reset()
            self.isDone = True
            return self
        
        if self.startTime == None:
            self.startTime = time.time() * 1000
            self.isDone = False
        
        else:
            currentTime = time.time() * 1000
            self.progress = (currentTime - self.startTime) / duration
            self.porgress = clamp(0, 1, self.progress)
        return self
    
    def reset(self):
        self.progress = 0
        self.startTime = None
        self.isDone = True
        
    def done(self):
        return self.isDone
    
  
            