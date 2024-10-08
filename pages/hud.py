import pygame
from constant import HEIGHT, outlineColor, WIDTH
from gameStateController import GameStateController
from utils.helper import clamp
from utils.lerp import Lerp


class Hud():
    def __init__(self, level:int) -> None:
        gameFont80 = pygame.font.Font('font/Pixeltype.ttf', 80)
        self.gameFont70 = pygame.font.Font('font/Pixeltype.ttf', 70)
        self.gameFont40 = pygame.font.Font('font/Pixeltype.ttf', 40)
      
        self.m_READY_Render = gameFont80.render("READY", False, outlineColor)
        self.initialm_READY_Rect = self.m_READY_Render.get_rect()
        
        self.m_GO_Render = gameFont80.render("GO!!", False, outlineColor)
        self.initialm_GO_Rect = self.m_GO_Render.get_rect()
        
        self.m_LEVEL_Render = gameFont80.render(f"STAGE {level}", False, outlineColor)
        self.initialm_LEVEL_Rect = self.m_LEVEL_Render.get_rect()
        
        self.m_TIME_UP_Render = self.gameFont40.render(f"TIME UP!!", False, outlineColor)
        self.m_TIME_UP_RenderScaled = None
        self.initialm_TIME_UP_Rect = self.m_TIME_UP_Render.get_rect()
        
        
        self.timeTextPos = (0.5 * WIDTH, 0.1 * HEIGHT)
        self.scoreTextPos = (0.85 * WIDTH, 0.1 * HEIGHT)

        self.startSequenceLerp = Lerp()
        self.endSequenceLerp = Lerp()
   
    def scaleRender(self, lerp:Lerp, surface:pygame.Surface, initialWidth:float, initialHeight:float, factor:float):
        width = lerp.easeIn(initialWidth, initialWidth * factor)
        height = lerp.easeIn(initialHeight, initialHeight * factor)
        return pygame.transform.scale(surface, (width, height))
    
    
    def renderText(self, text, position, font:pygame.font.Font):
        surface = font.render(text, False, outlineColor)
        rect = surface.get_rect(center=position)
        return rect, surface
        
   
    def animateSequence(self, lerp:Lerp, screen:pygame.surface.Surface, surface:pygame.surface.Surface, initialRectSize:pygame.rect.Rect):
        scaleFactor = 1.5
        lerp.drive()
        alpha = lerp.Sinusoidal(0, 400)
        alpha = clamp(0, 255, alpha)
        
        surface.set_alpha(alpha)
        renderScaled = self.scaleRender(lerp, surface, *initialRectSize, scaleFactor)
        
        rect = renderScaled.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        screen.blit(renderScaled, rect)
            
    def sequence1(self, lerp:Lerp, screen):
        self.animateSequence(lerp, screen, self.m_LEVEL_Render, self.initialm_LEVEL_Rect.size)
        
    def sequence2(self, lerp:Lerp, screen):
        self.animateSequence(lerp, screen, self.m_READY_Render, self.initialm_READY_Rect.size)
   
        
    def sequence3(self, lerp:Lerp, screen, gameScore, gameTime):
            lerp.drive()
            
            self.animateSequence(lerp, screen, self.m_GO_Render, self.initialm_GO_Rect.size)
          
            
            y = lerp.cubicEaseOut(0, self.scoreTextPos[1])
            gameScoreRect, gameScoreRender = self.renderText(f":{gameScore:02d}", (self.scoreTextPos[0], y), self.gameFont40)
            gameTimeRect, gameTimeRender = self.renderText(f"{gameTime:02d}", (self.timeTextPos[0], y), self.gameFont70)
            
            
            screen.blit(gameScoreRender, gameScoreRect)
            screen.blit(gameTimeRender, gameTimeRect)
      
    
    def update(self, screen, controller:GameStateController):
        # resolver.updateScoreCounter()
        gameScore = controller.getGameScoreCounter()
        gameTime = controller.getGameTime()
    
        isStartSequenceDone = self.startSequenceLerp\
            .wait(300).andThen(1000, self.sequence1, screen=screen)\
            .andThen(1000, self.sequence2, screen=screen)\
            .andThen(1000, self.sequence3, lambda: controller.setLevelInProgress(True), screen = screen, gameScore = gameScore, gameTime = gameTime)\
            .isDone()
        if isStartSequenceDone == True:
            gameScoreRect, gameScoreRender =  self.renderText(f":{gameScore:02d}", self.scoreTextPos, self.gameFont40)
            gameTimeRect, gameTimeRender = self.renderText(f"{gameTime:02d}", self.timeTextPos, self.gameFont70)
            
            screen.blit(gameScoreRender, gameScoreRect)
            screen.blit(gameTimeRender, gameTimeRect)
            
        if controller.isTimeUp():
            isEndSequenceDone = self.endSequenceLerp.wait(300).andThen(1000, self.endSequence1, screen = screen).isDone()
            if isEndSequenceDone:
                screen.blit(self.m_TIME_UP_RenderScaled, self.m_TIME_UP_RenderScaled.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
                
            
    
    def endSequence1(self, lerp:Lerp, screen:pygame.surface.Surface):
        
        lerp.drive()
        alpha = lerp.easeIn(0, 255)
      
        
        self.m_TIME_UP_Render.set_alpha(alpha)
        factor = 1.8
        width = lerp.easeInOut(self.initialm_TIME_UP_Rect.width, self.initialm_TIME_UP_Rect.width * factor)
        height = lerp.easeInOut(self.initialm_TIME_UP_Rect.height, self.initialm_TIME_UP_Rect.height * factor)
        self.m_TIME_UP_RenderScaled = pygame.transform.scale(self.m_TIME_UP_Render, (width, height))
        rect = self.m_TIME_UP_RenderScaled.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        screen.blit(self.m_TIME_UP_RenderScaled, rect)
        
        
        