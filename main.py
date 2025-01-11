import numpy
import Box2D
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



    
pygame.mixer.init(buffer=64)
pygame.init()

pygame.display.set_caption('Asteroids')

back_ground = Background()


screen = pygame.display.set_mode((GlobalConfig.width, GlobalConfig.height))

_game:Game = None

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



def _dispose_old_game():
    global _game
    if _game != None:
        _game.dispose()
        _game = None

def initialize_start_screen():
    
    _dispose_old_game() 
    global _game_controller 
    _game_controller = GameStateController()
    start_screen = StartScreen(_game_controller.high_score, _game_controller.key_map)
    g_router.start(start_screen)

    # SoundController.sound_track_channel().play(SoundController.menu_sound_track, -1)

# _controller = GameStateController()
_game_controller:GameStateController = None
_timed_list = TimedList((GlobalConfig.width * .9, GlobalConfig.height * .2), 500)
g_router = G_Router()
initialize_start_screen()
    
    # keeping a reference in order to call the dispose method method at appropriate situation
    

    

    
def initialize_game():
    
    # SoundController.sound_track_channel().play(SoundController.game_sound_track, -1)
    
    if _game_controller.bonus_time_activity != None:
        _timed_list.register_item(_game_controller.bonus_time_activity)
        
    _dispose_old_game()
    global _game
    _game = Game(_timed_list, _game_controller)
    g_router.replace(_game)

    
def initialize_end_game_screen():
    _dispose_old_game()
    endGameScreen = EndGameScreen()
    g_router.replace(endGameScreen)
    

async def main():
    
    fps_font = Fonts.quantum(15)
    
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer,2000)
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        screen.fill(Colors.background_color)
        back_ground.draw(screen)
        # glow_screen.fill(Colors.background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break;  
            handle_event(event)
            g_router.handle_event(event)
            g_router.handle_event_2(event)
        
        # handle_update()
        g_router.update()
        g_router.draw(screen)
        
        text_fps = UiFactory.create_text(f'{clock.get_fps():.1f}', font = fps_font)
        screen.blit(text_fps, text_fps.get_rect(center=(GlobalConfig.width - 25, GlobalConfig.height - 20)).topleft)
        
        pygame.display.flip()
        await asyncio.sleep(0)  # Let other tasks run
            
    _save_game()  
    pygame.quit()
    pygame.mixer.quit()

        
        
def _save_game():
    global _game_controller
    if _game_controller == None:
        return
    
    Helper.save_data(MiscConfig.saved_data_location, _game_controller.saved_data.to_dict(), GlobalConfig.key)
        
        
def handle_event(event):
    
    if event.type == EventConfig.start_new_game_event:
        initialize_game()
    if event.type == EventConfig.end_game_event:
        _save_game()
        initialize_end_game_screen()
    if event.type == EventConfig.exit_game_event:
        _save_game()
        initialize_start_screen()
        
    button_event = False 
    for item in GlobalResolver.event_queue:
        item.handle_event(event)
        if isinstance(item, Button):
            button_event = True
        
    GlobalResolver.event_queue.clear()
    
    
    

asyncio.run(main())
   
