


import pygame


class SoundStrategy():
    def __init__(self, shoot_file_path):
        self.shoot_file_path = shoot_file_path
    
    def shoot(self):
        return pygame.mixer.Sound(self.shoot_file_path)