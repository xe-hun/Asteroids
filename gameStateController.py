import pygame

from constant import END_GAME_EVENT, START_NEW_GAME_EVENT
from utils.delay import Delay


class GameStateController():
    
  
    
    def __init__(self) -> None:
        self.ASTEROID_DESTROYED_POINT = 100
        self.NEW_LEVEL_POINT = 20
        self.LEVEL_TIME = 30
        self.START_LIVES = 2
        self.ASTEROID_SPAWN_PER_LEVEL = 5
        self.resetGame()
        self.__highScore = 0
        self.__gameScoreCounter = 0
        self.__asteroidSpawnPerLevel = self.ASTEROID_SPAWN_PER_LEVEL
     
        # self.resetGame = False
        self.delay = Delay()
        self.counterDelay = Delay()
        
    def scoreUpdate(self):
        
        def update():
             self.__gameScoreCounter += counterStep
        
        # update the highScore
        if self.__gameScore > self.__highScore:
            self.__highScore = self.__gameScore
            
        counterStep = int((self.__gameScore - self.__gameScoreCounter) / 50)
        
        if self.__gameScoreCounter <= self.__gameScore:
            self.counterDelay.delay(100, onDone=update,  reset=True)
        else:
            self.__gameScoreCounter = self.__gameScore
        
    def setLevelInProgress(self, value):
        self.__levelInProgress = value
        
    def isLevelInProgress(self):
        return self.__levelInProgress
        
    def getGameTime(self):
        return self.__levelTime
    
    def getLivesRemaining(self):
        return self.__livesRemaining
    
    def getGameScoreCounter(self):
        return self.__gameScoreCounter         
    
    def reportAsteroidDestroyed(self):
        self.__numberOfAsteroidsDestroyed += 1
        self.__gameScore += self.ASTEROID_DESTROYED_POINT
    
    def goToNewLevel(self):
        self.__level += 1
        self.__gameScore += self.NEW_LEVEL_POINT
        self.resetLevel()
        pygame.event.post(pygame.event.Event(START_NEW_GAME_EVENT))
        
    def resetLevel(self):
        self.asteroidsRemaining = float('inf')
        self.__asteroidSpawned = 0
        self.__levelTime = self.LEVEL_TIME
        self.__levelInProgress = False
        
    def resetGame(self):
        self.resetLevel()
        self.__numberOfAsteroidsDestroyed = 0
        self.__level = 1
        self.__livesRemaining = self.START_LIVES
        self.__gameScore = 0
        
    def getLevel(self):
        return self.__level
    
    def getHighScore(self):
        return self.__highScore     
    
    def reportAsteroidSpawned(self):
        self.__asteroidSpawned += 1
    
    def shouldSpawnedAsteroid(self):
        return self.__asteroidSpawned <= self.__asteroidSpawnPerLevel
    
    def gameTimePulse(self):
        if self.isLevelInProgress():
            self.__levelTime -= 1
            
    def isTimeUp(self):
        return self.__levelTime <= 0
            
    def reportAsteroidRemaining(self, remaining):
        self.asteroidsRemaining = remaining
            
    def controllerUpdate(self, numAsteroids):
        
        self.reportAsteroidRemaining(numAsteroids)
        
        self.scoreUpdate()
        
        if self.shouldSpawnedAsteroid() == False and self.asteroidsRemaining == 0:
            self.setLevelInProgress(False)
            self.delay.delay(2000, self.goToNewLevel, True)
                
        if self.isTimeUp():
            self.setLevelInProgress(False)
            self.delay.delay(2000, self.gameOver, True)
                
               
                
            
    def gameOver(self):
        self.resetLevel()
        self.__livesRemaining -= 1
        pygame.event.post(pygame.event.Event(END_GAME_EVENT))
        
            # new level