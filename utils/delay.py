import math
import time
from constant import FPS
from utils.helper import clamp


class Delay():
    
    def __init__(self, fps:int = FPS, use_timer:bool = False, activate:bool = True) -> None:
        self.UNIT_OF_SECOND = 1000
        self._fps = fps
        self._use_timer = use_timer
        self._activate = activate
        self._reset()
        pass
        
    def delay(self, duration:int, on_done:callable = None, reset:bool = False, **kwargs):
        
        assert duration > 0
        "duration cannot be <= 0"
        
        if self._activate == False:
            self._is_done == True
            return self
        
        if self._progress >= 1 :
            if on_done != None and self.is_done == False:
                on_done(**kwargs)
            if reset:
                self._reset()
            self._is_done = True
            return self
        
        
        self._is_done = False
        if self._use_timer == True and self._start_time == None:
            self._start_time = time.time() * 1000
            
        elif self._use_timer == True:
            current_time = time.time() * 1000
            self._progress = (current_time - self._start_time) / duration
        
        else:
            self._frame_counter += (self.UNIT_OF_SECOND / self._fps)
            self._progress = self._frame_counter / duration
            
        self._progress = clamp(0, 1, self._progress)
        return self
    
    def _reset(self):
        self._progress = 0
        self._frame_counter = 0
        self._start_time = None
        self._is_done = True
    
    @property
    def is_done(self):
        return self._is_done
    
  
            