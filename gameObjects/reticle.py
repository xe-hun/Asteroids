

import pygame


class Reticle():
    def __init__(self):
        
        self._position = (0, 0)
        self._angle_degree = -90
        
        self._green_color = (90, 220, 90)
        self._red_color = (255, 90, 90)
        self._surface = pygame.Surface((9, 25), pygame.SRCALPHA)
        pygame.draw.line(self._surface, self._green_color, (5, 25), (5, 0))
        pygame.draw.line(self._surface, self._green_color, (1, 5), (5, 5))
        
        # self._mouse_down = True
    
        
    def update(self, position, angle_degree):
        self._position = position
        self._angle_degree = angle_degree
        
    def draw(self, screen):
        
        surface_R = pygame.transform.rotate(self._surface, self._angle_degree)
        rect = surface_R.get_rect(center=self._position)
        screen.blit(surface_R, rect.topleft)
        
    def handle_event(self, event):
        # if self._game_in_progress == False:
        #     return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.line(self._surface, self._red_color, (5, 25), (5, 0))
            pygame.draw.line(self._surface, self._red_color, (1, 5), (5, 5))
            # self._mouse_down = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            pygame.draw.line(self._surface, self._green_color, (5, 25), (5, 0))
            pygame.draw.line(self._surface, self._green_color, (1, 5), (5, 5))
            
        
    
        
        
    
    