from enum import Enum
import pygame
from config import GlobalConfig
from constant import END_GAME_EVENT, EXIT_GAME_EVENT, FPS, HEIGHT, SHAKE_EVENT, START_NEW_GAME_EVENT, WIDTH, background_color
from game import Game
from gRouter import G_Router
from globalResolver import GlobalResolver
from pages.endGameScreen import EndGameScreen
from pages.startScreen import StartScreen
from gameStateController import GameStateController
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
        pygame.mixer.pre_init(44100, -16, 2, 64)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 64)
        # pygame.mixer.init()
        pygame.display.set_caption('Asteroids')
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # self._controller = GameStateController()
        self._timed_list = TimedList((GlobalConfig.width * .9, GlobalConfig.height * .2), 500)
        self.g_router = G_Router()
        self.initialize_start_screen()
      
        
    def initialize_start_screen(self):
        # controller.reset_game()
        # high_score = self._controller.high_score
        self._controller = GameStateController()
        self.start_screen = StartScreen(self._controller.high_score, self._controller.key_map)
        self.g_router.replace(self.start_screen)
        # self.gameState = GameState.start_screen
        
    def initialize_game(self):
        if self._controller.bonus_time_activity != None:
            self._timed_list.register_item(self._controller.bonus_time_activity)
            
        self.game = Game(self._timed_list, self._controller)
        self.g_router.replace(self.game)

        # self.gameState = GameState.game
        
    def initialize_end_game_screen(self):
        self.endGameScreen = EndGameScreen(self._controller.lives_remaining)
        self.g_router.replace(self.game)
        # self.gameState = GameState.end_game
    
    def logic(self):
        
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,2000)
        
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.screen.fill(background_color)
            
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
        quit()
            
            
            
    def handle_event(self, event):
        
           
        if event.type == START_NEW_GAME_EVENT:
            self.initialize_game()
        if event.type == END_GAME_EVENT:
            self.initialize_end_game_screen()
        if event.type == EXIT_GAME_EVENT:
            self.initialize_start_screen()
            
        button_event = False 
        for item in GlobalResolver.event_queue:
            item.handle_event(event)
            if isinstance(item, Button):
                button_event = True
            
        GlobalResolver.event_queue.clear()
        
        
            
            
        # if self.gameState == GameState.start_screen:
        #     self.start_screen.handle_event(event)

        # elif self.gameState == GameState.game and not button_event:
        #     self.game.handle_event(event)
            
          
                
            
    # def handle_update(self):
    #     if self.gameState == GameState.start_screen:
    #         self.start_screen.draw(self.screen)

    #     elif self.gameState == GameState.game:
    #         self.game.update(self.screen)
            
    #     elif self.gameState == GameState.end_game:
    #         self.endGameScreen.draw(self.screen)
            
                 
           
    
    
    

if __name__ == "__main__":
    main = Main()
    main.logic()
    # main.game()