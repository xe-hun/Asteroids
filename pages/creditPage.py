

from config.globalConfig import GlobalConfig
from utils.fonts import Fonts
from gRouter import G_Router
from pages.pageBase import PageBase
from ui.uiFactory import UiFactory
import webbrowser


class CreditPage(PageBase):
    def __init__(self):
        address = '@nutak20'
        self._msg_follow = UiFactory.create_button(f'follow on X : {address}',self._follow_on_x, font = Fonts.pixel_type(30), hover = False)
        self._btn_back = UiFactory.create_button('Back', lambda : G_Router.pop(), 20, dimension = (200, 40))
    
    def draw(self, screen, **kwargs):
        
        self._msg_follow.draw(screen, (GlobalConfig.width * .5, GlobalConfig.height * .5))
        self._btn_back.draw(screen, (GlobalConfig.width * .5, GlobalConfig.height * .6))
        
    def _follow_on_x(self):
        webbrowser.open('https://x.com/Nutak20')
    
    