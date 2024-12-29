

from pages.pageBase import PageBase


class G_Router():
    def __init__(self):
        pass
    
    _page_list:list[PageBase] = []
    game_paused:bool = False
    
    @staticmethod
    def push(page:PageBase):
        G_Router._page_list.append(page)
        return len(G_Router._page_list) - 1
    
    @staticmethod
    def pop(index:int = -1):
        G_Router._page_list = G_Router._page_list[:index]
    
    @staticmethod
    def replace(page:PageBase):
        if len(G_Router._page_list) == 0:
            G_Router._page_list.append(page)
        else:
            G_Router._page_list[-1] = page
            
    @staticmethod
    def start(page:PageBase):
       G_Router._page_list = [page]
       
    
    def update(self):
        G_Router._page_list[-1].update(G_Router.game_paused)
     
    def draw(self, screen, **kwargs):
        page = G_Router._page_list[-1]
        page_index = len(G_Router._page_list) - 1
        self._recursive_draw(page_index - 1, page.is_transparent, screen, **kwargs)
        page.draw(screen, **kwargs)
        
    def _recursive_draw(self, page_index:int, previous_page_is_transparent, screen, **kwargs):
        if previous_page_is_transparent == False or page_index < 0:
            return
        
        page = G_Router._page_list[page_index]
        self._recursive_draw(page_index - 1, page.is_transparent, screen, **kwargs)
        page.draw(screen, **kwargs)
            
        
    def handle_event(self, event):    
        G_Router._page_list[-1].handle_event(event)
        
    def handle_event_2(self, event):
        for e in G_Router._page_list:
            e.handle_event_2(event)