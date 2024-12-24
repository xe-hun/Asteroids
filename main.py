from enum import Enum
import os
from time import sleep
import pygame
from config import Colors, EventConfig, GlobalConfig
from constant import FPS
from game import Game
from gRouter import G_Router
from globalResolver import GlobalResolver
from pages.endGameScreen import EndGameScreen
from pages.startScreen import StartScreen
from gameStateController import GameStateController
from soundController import SoundController
from ui.button import Button
from ui.timedList import TimedList

class GameState(Enum):
    start_screen = 1
    game = 2
    end_game = 3
   


class Main():
    
    def __init__(self) -> None:
      
        # pygame.init()
        # pygame.mixer.pre_init()
        # pygame.mixer.init()
        # pygame.mixer.pre_init(44100, -16, 4, 64)
        pygame.mixer.init(buffer=64)
        pygame.mixer.stop()
        sleep(.5)
        pygame.mixer.init(buffer=64)
        sleep(.5)
        pygame.init()
        # pygame.mixer.quit()
        # pygame.mixer.init(44100, -16, 2, 64)
        # pygame.mixer.init()
        pygame.display.set_caption('Asteroids')
        
        self.screen = pygame.display.set_mode((GlobalConfig.width, GlobalConfig.height))
        
        SoundController.load_resources(
            laser_fire_sound_filepath = os.path.join('sound', 'game', 'laser_fire.wav'),
            rocket_fire_sound_filepath = os.path.join('sound', 'game', 'rocket_fire.wav'),
            ship_movement_sound_filepath = os.path.join('sound', 'game', 'ship_movement.wav'),
            cursor_hover_sound_filepath = os.path.join('sound', 'ui', 'cursor_hover_sound.mp3'),
            cursor_click_sound_filepath = os.path.join('sound', 'ui', 'cursor_click_sound.mp3'),
            menu_sound_track_filepath = os.path.join('sound', 'ui', 'menu_sound_track.wav'),
            game_sound_track_filepath = os.path.join('sound', 'ui', 'game_sound_track.wav'),
        )
        # self._controller = GameStateController()
        self._timed_list = TimedList((GlobalConfig.width * .9, GlobalConfig.height * .2), 500)
        self.g_router = G_Router()
        self.initialize_start_screen()
      
        
    def initialize_start_screen(self):
        # controller.reset_game()
        # high_score = self._controller.high_score
        self._game_controller = GameStateController()
        self.start_screen = StartScreen(self._game_controller.high_score, self._game_controller.key_map)
        self.g_router.replace(self.start_screen)
        # self.gameState = GameState.start_screen
        # if SoundController.sound_track_channel().get_busy() == False:
        SoundController.sound_track_channel().play(SoundController.menu_sound_track, -1)

        
    def initialize_game(self):
        
        # if SoundController.sound_track_channel().get_busy() == False:
        SoundController.sound_track_channel().play(SoundController.game_sound_track, -1)
            
        
        if self._game_controller.bonus_time_activity != None:
            self._timed_list.register_item(self._game_controller.bonus_time_activity)
            
        game = Game(self._timed_list, self._game_controller)
        self.g_router.replace(game)

        
    def initialize_end_game_screen(self):
        
        endGameScreen = EndGameScreen()
        self.g_router.replace(endGameScreen)
    
    def logic(self):
        
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,2000)
        
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.screen.fill(Colors.background_color)
            
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
            
            pygame.display.flip()
                
        pygame.quit()
        pygame.mixer.quit()
        quit()
            
            
            
    def handle_event(self, event):
        
           
        if event.type == EventConfig.start_new_game_event:
            self.initialize_game()
        if event.type == EventConfig.end_game_event:
            self.initialize_end_game_screen()
        if event.type == EventConfig.exit_game_event:
            self.initialize_start_screen()
            
        button_event = False 
        for item in GlobalResolver.event_queue:
            item.handle_event(event)
            if isinstance(item, Button):
                button_event = True
            
        GlobalResolver.event_queue.clear()
        
        
    
    

if __name__ == "__main__":
    main = Main()
    main.logic()
    # main.game()