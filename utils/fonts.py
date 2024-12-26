
    
import os
import pygame

from utils.helper import Helper


class Fonts():
    def pixel_type(size:int):
        return pygame.font.Font(os.path.join(Helper.resource_path(), 'font', 'pixeltype.ttf'), size)
    
    def quantum(size:int):
        return pygame.font.Font(os.path.join(Helper.resource_path(), 'font', 'quantum.ttf'), size)
    