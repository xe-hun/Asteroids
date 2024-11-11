

from pages.page_base import PageBase


class GRouter():
    def __init__(self):
        pass
    
    _page_list = []
    game_paused = False
    
    @staticmethod
    def push(page:PageBase):
        GRouter._page_list.append(page)
        return len(GRouter._page_list) - 1
    
    @staticmethod
    def pop(index:int = -1):
        GRouter._page_list = GRouter._page_list[:index]
    
    @staticmethod
    def replace(page:PageBase):
        if len(GRouter._page_list) == 0:
            GRouter._page_list.append(page)
        else:
            GRouter._page_list[-1] = page
    
    
    def update(self):
       
        try:
            GRouter._page_list[-1].update(GRouter.game_paused)
        except AttributeError:
            pass
    
    def draw(self, screen):
       
        try:
           GRouter._page_list[-1].draw(screen)
        except AttributeError:
            pass
        
    def handle_event(self, event):
        
        try:
           GRouter._page_list[-1].handle_event(event)
        except AttributeError:
            pass