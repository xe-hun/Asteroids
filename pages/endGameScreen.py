from constant import EXIT_GAME_EVENT, HEIGHT, START_NEW_GAME_EVENT, WIDTH, background_color, outline_color

import pygame


class EndGameScreen():
    
    def __init__(self, livesRemaining:int) -> None:
        
        self.livesRemaining = livesRemaining
        
        self.gameFont50 = pygame.font.Font('font/quantum.ttf', 30)
        self.gameFont30 = pygame.font.Font('font/quantum.ttf', 10)
        
        self.m_LIVES_Render = self.gameFont30.render(f'LIVES x {livesRemaining}', False, outline_color)
        self.m_LIVES_Rect = self.m_LIVES_Render.get_rect(center=(WIDTH / 2, 0.4 * HEIGHT))
        
        self.m_CONTINUE_Render = self.gameFont50.render('CONTINUE', False, outline_color)
        self.m_CONTINUE_Rect = self.m_CONTINUE_Render.get_rect(center=(WIDTH / 2, 0.5 * HEIGHT))
        
        self.m_GAME_OVER_Render = self.gameFont50.render('GAME OVER!!', False, outline_color)
        self.m_GAME_OVER_Rect = self.m_CONTINUE_Render.get_rect(center=(WIDTH / 2, 0.5 * HEIGHT))
        
        self.m_EXIT_Render = self.gameFont50.render('EXIT', False, outline_color)
        self.m_EXIT_Rect = self.m_EXIT_Render.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))
    
    def draw(self, screen:pygame.surface):
        screen.fill(background_color)
        screen.blit(self.m_LIVES_Render, self.m_LIVES_Rect)
        if self.livesRemaining > 0:
            screen.blit(self.m_CONTINUE_Render, self.m_CONTINUE_Rect) 
        else:
            screen.blit(self.m_GAME_OVER_Render, self.m_GAME_OVER_Rect) 
        
        screen.blit(self.m_EXIT_Render, self.m_EXIT_Rect)
        
    def handleEvents(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            
            self.handleClick(*event.pos, self.m_CONTINUE_Rect, self.continueGame)
            # self.handleClick(*event.pos, self.m_GAME_OVER_Rect, self.continueGame)
            
            self.handleClick(*event.pos, self.m_EXIT_Rect, self.exitGame)
    
    def continueGame(self):
        if self.livesRemaining > 0:
            pygame.event.post(pygame.event.Event(START_NEW_GAME_EVENT))
        
    def exitGame(self):
        pygame.event.post(pygame.event.Event(EXIT_GAME_EVENT))
        
   
            
    def handleClick(self, mouseX:float, mouseY:float, buttonRect:pygame.rect.Rect, onButtonCLick:callable):
        if buttonRect.x <= mouseX <= buttonRect.x + buttonRect.width and \
            buttonRect.y <= mouseY <= buttonRect.y + buttonRect.height:
                # if onButtonCLick is not None:
                    onButtonCLick()
        
    