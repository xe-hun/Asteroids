import math
import time
from constant import FPS
from utils.helper import clamp


class Lerp():
    
    def __init__(self, fps:int = FPS, use_timer:bool = False, activate:bool = True) -> None:
        self.UNIT_OF_SECOND = 1000
        self._activate = activate
        self._fps = fps
        self._duration = None
        self._on_done = None
        self._on_begin = None
        self._use_timer = use_timer
        self._start_time = None
        self._is_done = False
        self._progress = 0
        self._child = None
        self._value = None
        self._frame_counter = 0
        self._pause = False
       
        
        
    def _drive(self):
        
        # the drive method is not supposed to be executed because
        # the Lerp class has not yet been activated
        if self._activate == False:
            self._is_done = True
            return True
        
       
        # this returns the _drive() method early, thereby simulating
        # the pause conditions.
        if self._pause:
            return not self._is_done
        
        # when progress is zero, the Lerp class is activated and not paused
        # then we must be at the beginning of the process and thereby calling
        # the _on_begin function
        if self._progress <= 0 and self._on_begin != None:
            self._on_begin()
        
        # progress theoretically ends at one, therefore if its above one, the
        # the condition to end the sequence is safe to be executed
        if self._progress >= 1:
            if self._on_done != None and self._is_done == False:
                self._on_done()
                
            self._is_done = True
            return False
        
        # determins wether to use timer or update
        if self._use_timer == True and self._start_time == None:
            self._start_time = time.time() * 1000
            
        elif self._use_timer == True:
            current_time = time.time() * 1000
            self._progress = (current_time - self._start_time) / self._duration
        else:
            self._frame_counter += (self.UNIT_OF_SECOND / self._fps)
            self._progress = self._frame_counter / self._duration
              
        self._progress = clamp(0, 1, self._progress)    
        return True
            
    @property
    def is_done(self):
        return self._is_done
    
    @property
    def value(self):
        return self._value
        
    def copy_params(self, on_done, on_begin, duration):
       
        self._on_done = on_done
        self._on_begin = on_begin
        self._duration = duration
        
    def copy_control(self, pause):
        self._pause = pause
        
    def control(self, pause:bool = False):
        assert self._use_timer == False
        'control() not allowed when _use_timer == True'
        
        # assert (self._first_call == False and self.duration == None)\
        #     or (self._first_call == True and self.duration != None)
        # 'control() may only be called in the beginning of the chain'
        
        self._pause = pause
        return self
            
    def do(self, duration:int, call:callable, on_done:callable = None, on_begin:callable = None, **kwargs):
        assert duration > 0 
        "duration cannot be <= 0"
        
        
        if self._duration == None:
            self._duration = duration
            
        self._on_done = on_done
        self._on_begin = on_begin
            
        if self._drive() == True:
            self._value = call(self, **kwargs)
         
            return Dummy(self._value, self._activate)
        return self
    
    def wait(self, duration:int, on_done:callable = None, on_begin:callable = None):
        
        if self._duration == None:
            self._duration = duration
            
        self._on_done = on_done
        self._on_begin = on_begin
            
        if self._drive() == True:
         
            return Dummy(None, self._activate)
        return self
    
    def and_then(self, duration:int, call:callable, on_done:callable = None, on_begin:callable = None, **kwargs):
        
             
        if self._child == None:
            self._child = Lerp()
            self._child.copy_params(on_done, on_begin, duration)
     
        self._child.copy_control(self._pause)
        
        if self._child._drive() == True:
           
            self._value = call(self._child, **kwargs)
            self._child._value = self._value
           
            return Dummy(self._value, self._activate)
        else:
          
            return self._child
    
    def and_wait(self, duration:int, on_done:callable = None, on_begin:callable = None):
        if self._child == None:
            self._child = Lerp()
            self._child.copy_params(on_done, on_begin, duration)

        self._child.copy_control(self._pause)
        
        if self._child._drive() == True:
           
            return Dummy(None, self._activate)
        else:
            return self._child
        
          
        
    def linear(self, a, b):
        t = self._progress
        return a + (b - a) * t
    
    def ease_in(self, a, b):
        t = self._progress
        return a + (b - a) * t * t
    
    def ease_out(self, a, b):
        t = self._progress
        return a + (b - a) * (1 -  (1 - t) * (1 - t))
    
    def ease_in_out(self, a, b):
        t = self._progress
        return a + (b - a) * (2 * t * t if t < .5 else 1 - 2 * (1 - t) * (1 - t))
    
    def cubic_ease_in(self, a, b):
        t = self._progress
        return a + (b - a) * t * t * t  
    
    def cubic_ease_out(self, a, b):
        t = self._progress
        return a + (b - a) *( 1 - (1 - t) *(1 - t) * (1 - t))
    
    def cubic_ease_in_out(self, a, b):
        t = self._progress
        return a + (b - a) * (4 * t * t * t if t < .5 else 1 - 4 * (1 - t) * (1 - t) * (1 - t))
    
    def exponential_ease_in(self, a, b):
        t = self._progress
        return a + (b - a) * math.pow(2, 10 * (t - 1))
    
    def exponential_ease_out(self, a, b):
        t = self._progress
        return a + (b - a) * (1 - math.pow(2, -10 * (t - 1)))
    
    def sinusoidal(self, a, b, f:int=1):
        t = self._progress
        return a + (b - a) * (1 - (0.5 * math.cos(2 * math.pi * f * t) + .5))
    
    
    



class Dummy():
    
    def __init__(self, value, activate:bool) -> None:
        self._value = value
        self._activate = activate
    
    def and_then(self, *args, **kwargs):
        
        return Dummy(self._value, self._activate)   
    
    def and_wait(self, *args, **kwargs):
        return Dummy(self._value, self._activate)   
       
    @property
    def is_done(self):
        return False if self._activate else True
    
    @property
    def value(self):
        return self._value   
