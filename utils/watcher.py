from utils.delay import Delay


class Watcher():
    def __init__(self, on_value_change:callable = None, initial_value = None,):
        self._value = initial_value
        self._new_value = initial_value
        self._on_value_change = on_value_change
        self._new_value_queue = []
        pass
    
    def watch(self, value):
        self._update()
        if value != self._value:
            self._on_change(value)
            self._value = value
          
        return self
    
    def on_delay_done(self, i, value):
        self._new_value_queue = self._new_value_queue[:i-1]
        self._new_value = value
    
    def _update(self):
        for delay_params in self._new_value_queue:
            delay, duration, index, value  = delay_params
            delay.delay(duration, self.on_delay_done, i = index, value = value)
            
    def new_value(self, duration:int = 0):
        if duration <= 0:
            self._new_value = self._value
            self._new_value_queue = []
        else:
            delay = Delay()
            index = len(self._new_value_queue)
            self._new_value_queue.append((delay, duration, index, self._value))
            
        return self._new_value
        
    def _on_change(self, value):
        self._on_value_change(value)
        
        