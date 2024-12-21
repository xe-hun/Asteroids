


import pygame


class SoundController():
    
    # rocket_fire_sound_filepath:str
    # ship_movement_sound_filepath:str
    # laser_fire_sound_filepath:str
    # cursor_hover_sound_filepath:str
    
    
    @staticmethod
    def load_resources(laser_fire_sound_filepath,
                       rocket_fire_sound_filepath,
                       ship_movement_sound_filepath,
                       cursor_hover_sound_filepath,
                       cursor_click_sound_filepath,
                       menu_sound_track_filepath,
                       ):
        
        SoundController.rocket_fire_sound_filepath = rocket_fire_sound_filepath
        SoundController.ship_movement_sound_filepath = ship_movement_sound_filepath
        SoundController.laser_fire_sound_filepath = laser_fire_sound_filepath
        SoundController.cursor_hover_sound_filepath = cursor_hover_sound_filepath
        SoundController.cursor_click_sound_filepath = cursor_click_sound_filepath
        SoundController.menu_sound_track_filepath = menu_sound_track_filepath
        
        pygame.mixer.set_num_channels(4)
        
    @staticmethod
    def shoot_laser_sound():
        return pygame.mixer.Sound(SoundController.laser_fire_sound_filepath)
    
    @staticmethod
    def shoot_rocket_sound():
        return pygame.mixer.Sound(SoundController.rocket_fire_sound_filepath)
    
    @staticmethod
    def ship_movement_sound():
        return pygame.mixer.Sound(SoundController.ship_movement_sound_filepath)
    
    @staticmethod
    def cursor_hover_sound():
        return pygame.mixer.Sound(SoundController.cursor_hover_sound_filepath)
        
    @staticmethod
    def cursor_click_sound():
        return pygame.mixer.Sound(SoundController.cursor_click_sound_filepath)
    
    @staticmethod
    def menu_sound_track():
        return pygame.mixer.Sound(SoundController.menu_sound_track_filepath)
    
    @staticmethod
    def ship_weapon_channel():
        return pygame.mixer.Channel(0)
    
    @staticmethod
    def ship_boost_channel():
        return pygame.mixer.Channel(1)
    
    @staticmethod
    def game_effect_channel():
        return pygame.mixer.Channel(2)
    
    @staticmethod
    def sound_track_channel():
        return pygame.mixer.Channel(3)