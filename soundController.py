


import pygame


class SoundController():
    
    _is_music_on = False
    _is_sound_effect_on = False
    _is_sound_of_space_on = False
    
    def set_music(value:bool):
        SoundController._is_music_on = value
        SoundController.sound_track_channel().set_volume(float(value))
        
    def set_sound_effect(value:bool):
        SoundController._is_sound_effect_on = value
        
        for i in SoundController._effect_channels:
            i.set_volume(float(value))
        
      
        SoundController.achievement_channel().set_volume(float(value))
        
    def set_sound_of_space(value:bool):
        SoundController._is_sound_of_space_on = value
        SoundController.ship_boost_channel().set_volume(float(not value))
        SoundController.ship_weapon_channel().set_volume(float(not value))
        
        
    
   
    def is_music_on ():
        return SoundController._is_music_on
   
 
    def is_sound_effect_on ():
        return SoundController._is_sound_effect_on
    
    def is_sound_of_space_on():
        return SoundController._is_sound_of_space_on
   
    
    @staticmethod
    def load_resources(laser_fire_sound_filepath,
                       rocket_fire_sound_filepath,
                       ship_movement_sound_filepath,
                       cursor_hover_sound_filepath,
                       cursor_click_sound_filepath,
                       menu_sound_track_filepath,
                       game_sound_track_filepath,
                       perk_collected_sound_filepath,
                       level_up_sound_filepath,
                       ready_sound_filepath,
                       ):
        
        SoundController.rocket_fire_sound = SoundController.load_sound(rocket_fire_sound_filepath)
        SoundController.ship_movement_sound = SoundController.load_sound(ship_movement_sound_filepath)
        SoundController.laser_fire_sound = SoundController.load_sound(laser_fire_sound_filepath)
        SoundController.cursor_hover_sound = SoundController.load_sound(cursor_hover_sound_filepath)
        SoundController.cursor_click_sound = SoundController.load_sound(cursor_click_sound_filepath)
        SoundController.menu_sound_track = SoundController.load_sound(menu_sound_track_filepath)
        SoundController.game_sound_track = SoundController.load_sound(game_sound_track_filepath)
        SoundController.perk_collected_sound = SoundController.load_sound(perk_collected_sound_filepath)
        SoundController.level_up_sound = SoundController.load_sound(level_up_sound_filepath)
        SoundController.ready_sound = SoundController.load_sound(ready_sound_filepath)
        
        pygame.mixer.set_num_channels(8)
        SoundController._effect_channels = [pygame.mixer.Channel(i) for i in range(1, SoundController._num_effect_channel)]
    
    _num_effect_channel = 4
    _effect_channels = []
    _current_effect_channel = 0
        
    @staticmethod
    def load_sound(path):
        return pygame.mixer.Sound(path)
        
        
    
    @staticmethod
    def game_effect_channel():
        channel = SoundController._effect_channels[SoundController._current_effect_channel]
        SoundController._current_effect_channel = (SoundController._current_effect_channel) % (SoundController._num_effect_channel - 1)
        return channel
    
    @staticmethod
    def ship_weapon_channel():
        return pygame.mixer.Channel(SoundController._num_effect_channel + 0)
    
    @staticmethod
    def ship_boost_channel():
        return pygame.mixer.Channel(SoundController._num_effect_channel + 1)
    
    
    @staticmethod
    def sound_track_channel():
        return pygame.mixer.Channel(SoundController._num_effect_channel + 2)
    
    @staticmethod
    def achievement_channel():
        return pygame.mixer.Channel(SoundController._num_effect_channel + 3)
    