from enum import Enum
import pygame
from constant import FPS, HEIGHT, WIDTH, backgroundColor
from game import Game
from pages.startScreen import StartScreen
from test import Test

class GameState(Enum):
    startScreen = 1
    game = 2
    test = 3


class Main():
    
    def __init__(self) -> None:
      
        pygame.init()
        pygame.display.set_caption('Asteroids')
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # self.gameState = GameState.startScreen
        self.gameState = GameState.test
        self.startScreen = StartScreen(self.onStartGame, self.onQuitGame)
        self.test = Test()
        self.run = True
        # self.gameIsRunni
               
    def onStartGame(self):
        self.game = Game()
        self.gameState = GameState.game
    
    def onQuitGame(self):
        self.run = False
    
    def logic(self):
        
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,2000)
        
        clock = pygame.time.Clock()
        
        while self.run:
            clock.tick(FPS)
            self.screen.fill(backgroundColor)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break;
                
                if self.gameState == GameState.startScreen:
                    self.startScreen.handleEvent(event)

                elif self.gameState == GameState.game:
                    self.game.handleGameEvents(event)
                    
                elif self.gameState == GameState.test:
                    self.test.handleEvent(event)
                
              
                
            if self.gameState == GameState.startScreen:
                self.startScreen.draw(self.screen)

            elif self.gameState == GameState.game:
                self.game.gameUpdate(self.screen)
                # self.startScreen.handleEvent()
            elif self.gameState == GameState.test:
                self.test.update(self.screen)
                
                
            pygame.display.flip()
                
        pygame.quit()
        quit()
    
    
    

if __name__ == "__main__":
    main = Main()
    main.logic()
    # main.game()