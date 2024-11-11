 
from abc import ABC, abstractmethod


class PageBase(ABC):
    
    @abstractmethod
    def update(self, paused):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass