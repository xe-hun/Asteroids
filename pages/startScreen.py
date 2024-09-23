from constant import HEIGHT, WIDTH, backgroundColor, outlineColor

import pygame


class StartScreen():
    
    def __init__(self, onStartGame:callable, onQuitGame:callable) -> None:
        
        self.onStartGame = onStartGame
        self.onQuitGame = onQuitGame
        
        self.gameFont = pygame.font.Font('font/Pixeltype.ttf', 50)
        
        self.msg_startGame = self.gameFont.render('Start Game', False, outlineColor)
        self.msg_startGame_rect = self.msg_startGame.get_rect(center=(WIDTH / 2, 0.4 * HEIGHT))
        
        self.msg_quit = self.gameFont.render('Quit', False, outlineColor)
        # pygame.draw.polygon(self.msg_quit, outlineColor, [(0,0), (50, 0), (30, 50), (0, 30)], 2)
        self.msg_quit_rect = self.msg_quit.get_rect(center=(WIDTH / 2, 0.5 * HEIGHT))
        
        self.msg_score = self.gameFont.render('Score : 200', False, outlineColor)
        self.msg_score_rect = self.msg_score.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))
    
    def draw(self, screen:pygame.surface):
        screen.fill(backgroundColor)
        screen.blit(self.msg_startGame, self.msg_startGame_rect)
        screen.blit(self.msg_quit, self.msg_quit_rect)
        screen.blit(self.msg_score, self.msg_score_rect)
        
    def handleEvent(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.handleClick(*event.pos, self.msg_startGame_rect, self.onStartGame)
            self.handleClick(*event.pos, self.msg_quit_rect, self.onQuitGame)
            # self.handleClick(*event.pos, self.msg_quit_rect, self.onQuitGame())
        
   
            
    def handleClick(self, mouseX:float, mouseY:float, buttonRect:pygame.rect.Rect, onButtonCLick:callable):
        if buttonRect.x <= mouseX <= buttonRect.x + buttonRect.width and \
            buttonRect.y <= mouseY <= buttonRect.y + buttonRect.height:
                # if onButtonCLick is not None:
                    onButtonCLick()
        
    