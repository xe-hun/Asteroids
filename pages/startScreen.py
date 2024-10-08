from constant import HEIGHT, START_NEW_GAME_EVENT, WIDTH, backgroundColor, outlineColor

import pygame

from gameStateController import GameStateController


class StartScreen():
    
    def __init__(self, highScore:int) -> None:
        
        
        self.gameFont = pygame.font.Font('font/Pixeltype.ttf', 50)
        
        self.msg_startGame = self.gameFont.render('START GAME', False, outlineColor)
        self.msg_startGame_rect = self.msg_startGame.get_rect(center=(WIDTH / 2, 0.4 * HEIGHT))
        
        self.msg_quit = self.gameFont.render('QUIT', False, outlineColor)
        # pygame.draw.polygon(self.msg_quit, outlineColor, [(0,0), (50, 0), (30, 50), (0, 30)], 2)
        self.msg_quit_rect = self.msg_quit.get_rect(center=(WIDTH / 2, 0.5 * HEIGHT))
        
        self.msg_score = self.gameFont.render(f'High Score : {highScore}', False, outlineColor)
        self.msg_score_rect = self.msg_score.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))
    
    def draw(self, screen:pygame.surface):
        screen.fill(backgroundColor)
        screen.blit(self.msg_startGame, self.msg_startGame_rect)
        screen.blit(self.msg_quit, self.msg_quit_rect)
        screen.blit(self.msg_score, self.msg_score_rect)
        
    def handleEvents(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.handleClick(*event.pos, self.msg_startGame_rect, self.startGame)
            self.handleClick(*event.pos, self.msg_quit_rect, self.quitGame)
            # self.handleClick(*event.pos, self.msg_quit_rect, self.onQuitGame())
    
    def startGame(self):
        pygame.event.post(pygame.event.Event(START_NEW_GAME_EVENT))
        
    def quitGame(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
   
            
    def handleClick(self, mouseX:float, mouseY:float, buttonRect:pygame.rect.Rect, onButtonCLick:callable):
        if buttonRect.x <= mouseX <= buttonRect.x + buttonRect.width and \
            buttonRect.y <= mouseY <= buttonRect.y + buttonRect.height:
                # if onButtonCLick is not None:
                    onButtonCLick()
        
    