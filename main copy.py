import contextlib




# This suppresses the `Hello from pygame` message.
with contextlib.redirect_stdout(None):
    import pygame

import asyncio    

from gameObjects.background import Background
from utils.fonts import Fonts
from ui.uiFactory import UiFactory

import os
# import pygame
from config.GlobalConfig import GlobalConfig
from config.MiscConfig import MiscConfig
from config.EventConfig import EventConfig
from utils.colors import Colors
from constant import FPS
from game import Game
from gRouter import G_Router
from globalResolver import GlobalResolver
from utils.helper import Helper
from pages.endGameScreen import EndGameScreen
from pages.startScreen import StartScreen
from gameStateController import GameStateController
from soundController import SoundController
from ui.button import Button
from ui.timedList import TimedList



class Main():
    
    def __init__(self) -> None:
      
     
        pygame.mixer.init(buffer=64)
        pygame.init()
      
        pygame.display.set_caption('Asteroids')
        
        self.back_ground = Background()
        
        
        self.screen = pygame.display.set_mode((GlobalConfig.width, GlobalConfig.height))
        # self.glow_screen = pygame.Surface((GlobalConfig.width, GlobalConfig.height)).convert()
        self._game:Game = None

        # SoundController.load_resources(
        #     laser_fire_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'game', 'laser_fire.wav'),
        #     rocket_fire_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'game', 'rocket_fire.wav'),
        #     ship_movement_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'game', 'ship_movement.wav'),
        #     cursor_hover_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'ui', 'cursor_hover_sound.mp3'),
        #     cursor_click_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'ui', 'cursor_click_sound.mp3'),
        #     menu_sound_track_filepath = os.path.join(Helper.resource_path(), 'sound', 'ui', 'menu_sound_track.wav'),
        #     game_sound_track_filepath = os.path.join(Helper.resource_path(), 'sound', 'ui', 'game_sound_track.wav'),
        #     perk_collected_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'game', 'collect_perk.mp3'),
        #     level_up_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'game', 'level_up.mp3'),
        #     ready_sound_filepath = os.path.join(Helper.resource_path(), 'sound', 'game', 'ready.mp3'),
        # )
        # self._controller = GameStateController()
        self._timed_list = TimedList((GlobalConfig.width * .9, GlobalConfig.height * .2), 500)
        self.g_router = G_Router()
        self.initialize_start_screen()
        
        # keeping a reference in order to call the dispose method method at appropriate situation
      
    def _dispose_old_game(self):
        if self._game != None:
            self._game.dispose()
            self._game = None
        
    def initialize_start_screen(self):
        
        self._dispose_old_game()  
        self._game_controller = GameStateController()
        self.start_screen = StartScreen(self._game_controller.high_score, self._game_controller.key_map)
        self.g_router.start(self.start_screen)
   
        # SoundController.sound_track_channel().play(SoundController.menu_sound_track, -1)

        
    def initialize_game(self):
        
        # SoundController.sound_track_channel().play(SoundController.game_sound_track, -1)
        
        if self._game_controller.bonus_time_activity != None:
            self._timed_list.register_item(self._game_controller.bonus_time_activity)
            
        self._dispose_old_game()
        self._game = Game(self._timed_list, self._game_controller)
        self.g_router.replace(self._game)

        
    def initialize_end_game_screen(self):
        self._dispose_old_game()
        endGameScreen = EndGameScreen()
        self.g_router.replace(endGameScreen)
       
    
    async def logic(self):
        
        fps_font = Fonts.quantum(15)
        
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,2000)
        
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.screen.fill(Colors.background_color)
            self.back_ground.draw(self.screen)
            # self.glow_screen.fill(Colors.background_color)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break;  
                self.handle_event(event)
                self.g_router.handle_event(event)
                self.g_router.handle_event_2(event)
            
            # self.handle_update()
            self.g_router.update()
            self.g_router.draw(self.screen)
            
            text_fps = UiFactory.create_text(f'{clock.get_fps():.1f}', font = fps_font)
            self.screen.blit(text_fps, text_fps.get_rect(center=(GlobalConfig.width - 25, GlobalConfig.height - 20)).topleft)
            
            pygame.display.flip()
            await asyncio.sleep(0)  # Let other tasks run
              
        # self._save_game()  
        # pygame.quit()
        # pygame.mixer.quit()
    
            
            
    def _save_game(self):
        if self._game_controller == None:
            return
        
        Helper.save_data(MiscConfig.saved_data_location, self._game_controller.saved_data.to_dict(), GlobalConfig.key)
            
            
    def handle_event(self, event):
        
        if event.type == EventConfig.start_new_game_event:
            self.initialize_game()
        if event.type == EventConfig.end_game_event:
            self._save_game()
            self.initialize_end_game_screen()
        if event.type == EventConfig.exit_game_event:
            self._save_game()
            self.initialize_start_screen()
            
        button_event = False 
        for item in GlobalResolver.event_queue:
            item.handle_event(event)
            if isinstance(item, Button):
                button_event = True
            
        GlobalResolver.event_queue.clear()
        
        
    

# async def main():
    # m = Main()
    # await m.logic()
    

# if __name__ == "__main__":
#     main = Main()
#     main.logic()
#     # main.game()
# if __name__ == "__main__":
async def main():
    m = Main()
    await m.logic()
    
asyncio.run(main())
   
