


import pygame


class SoundStrategy():
    def __init__(self, laser_fire_sound_filepath, rocket_fire_sound_filepath, ship_movement_sound_filepath):
        self.laser_sound = pygame.mixer.Sound(laser_fire_sound_filepath)
        self.rocket_fire_sound_filepath = rocket_fire_sound_filepath
        self.ship_movement_sound_filepath = ship_movement_sound_filepath
        
        pygame.mixer.set_num_channels(2)
    
    def shoot_laser_sound(self):
        return self.laser_sound
    
    def shoot_rocket_sound(self):
        return pygame.mixer.Sound(self.rocket_fire_sound_filepath)
    
    def ship_movement_sound(self):
        return pygame.mixer.Sound(self.ship_movement_sound_filepath)
    
    def channel2(self):
        return pygame.mixer.Channel(1)
    
    def channel1(self):
        return pygame.mixer.Channel(0)