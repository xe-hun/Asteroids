from enum import Enum
import pygame
from constant import END_GAME_EVENT, EXIT_GAME_EVENT, FPS, HEIGHT, SHAKE_EVENT, START_NEW_GAME_EVENT, WIDTH, backgroundColor
from game import Game
from pages.endGameScreen import EndGameScreen
from pages.startScreen import StartScreen
from gameStateController import GameStateController
from test import Test

class GameState(Enum):
    startScreen = 1
    game = 2
    endGame = 3
    test = 4


class Main():
    
    def __init__(self) -> None:
      
        pygame.init()
        pygame.display.set_caption('Asteroids')
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # self.gameState = GameState.test
        # self.test = Test()
        self.controller = GameStateController()
        self.initializeStartScreen(self.controller)
        # self.onStartGame(self.controller)
        
        
    def initializeStartScreen(self, controller:GameStateController):
        controller.resetGame()
        self.startScreen = StartScreen(controller.getHighScore())
        self.gameState = GameState.startScreen
        
    def initializeGame(self):
        self.game = Game(self.controller)
        self.gameState = GameState.game
        
    def initializeEndGameScreen(self):
        self.endGameScreen = EndGameScreen(self.controller.getLivesRemaining())
        self.gameState = GameState.endGame
    
    def logic(self):
        
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,2000)
        
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.screen.fill(backgroundColor)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break;  
                self.handleEvents(event)
            
            self.handleUpdates()
            
            pygame.display.flip()
                
        pygame.quit()
        quit()
            
            
            
    def handleEvents(self, event):
        
        if event.type == pygame.MOUSEBUTTONUP:
            pygame.event.post(pygame.event.Event(SHAKE_EVENT))
           
        if event.type == START_NEW_GAME_EVENT:
            self.initializeGame()
        if event.type == END_GAME_EVENT:
            self.initializeEndGameScreen()
        if event.type == EXIT_GAME_EVENT:
            self.initializeStartScreen(self.controller)
            
            
        if self.gameState == GameState.startScreen:
            self.startScreen.handleEvents(event)

        elif self.gameState == GameState.game:
            self.game.handleGameEvents(event)
            
        elif self.gameState == GameState.endGame:
            self.endGameScreen.handleEvents(event)
            
        elif self.gameState == GameState.test:
            self.test.handleEvent(event)
                
            
    def handleUpdates(self):
        if self.gameState == GameState.startScreen:
            self.startScreen.draw(self.screen)

        elif self.gameState == GameState.game:
            self.game.gameUpdate(self.screen)
            
        elif self.gameState == GameState.endGame:
            self.endGameScreen.draw(self.screen)
            
        elif self.gameState == GameState.test:
            self.test.update(self.screen)
                 
           
    
    
    

if __name__ == "__main__":
    main = Main()
    main.logic()
    # main.game()