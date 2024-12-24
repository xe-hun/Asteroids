


import pygame


class SoundController():
    
    _music_on = False
    _sound_on = False
    
    def set_music_on(value:bool):
        SoundController._music_on = value
        SoundController.sound_track_channel().set_volume(float(value))
        
    def set_sound_on(value:bool):
        SoundController._sound_on = value
        SoundController.ship_boost_channel().set_volume(float(value))
        SoundController.game_effect_channel().set_volume(float(value))
        SoundController.ship_weapon_channel().set_volume(float(value))
        
        
    
   
    def music_on ():
        return SoundController._music_on
   
   
    # @music_on.setter
    # def music_on (value:bool):
    #     pass
        # print('kemba')
        # SoundController._music_on = value
        # SoundController.sound_track_channel().set_volume(float(value))
        
 
    def sound_on ():
        return SoundController._sound_on
   
    # @sound_on.setter
    # def sound_on (value:bool):
    #     pass
        # SoundController._sound_on = value
        # SoundController.ship_boost_channel().set_volume(float(value))
        # SoundController.game_effect_channel().set_volume(float(value))
        # SoundController.ship_weapon_channel().set_volume(float(value))

   
    
    
    @staticmethod
    def load_resources(laser_fire_sound_filepath,
                       rocket_fire_sound_filepath,
                       ship_movement_sound_filepath,
                       cursor_hover_sound_filepath,
                       cursor_click_sound_filepath,
                       menu_sound_track_filepath,
                       game_sound_track_filepath,
                       ):
        
        SoundController.rocket_fire_sound = SoundController.load_sound(rocket_fire_sound_filepath)
        SoundController.ship_movement_sound = SoundController.load_sound(ship_movement_sound_filepath)
        SoundController.laser_fire_sound = SoundController.load_sound(laser_fire_sound_filepath)
        SoundController.cursor_hover_sound = SoundController.load_sound(cursor_hover_sound_filepath)
        SoundController.cursor_click_sound = SoundController.load_sound(cursor_click_sound_filepath)
        SoundController.menu_sound_track = SoundController.load_sound(menu_sound_track_filepath)
        SoundController.game_sound_track = SoundController.load_sound(game_sound_track_filepath)
        
        pygame.mixer.set_num_channels(4)
        
        # _effect_channels = [pygame.mixer.Channel(i) for i in range(1, 4)]
        # _current_effect_channel = 0
        
    @staticmethod
    def load_sound(path):
        return pygame.mixer.Sound(path)
        
        
    # @staticmethod
    # def shoot_laser_sound():
    #     return pygame.mixer.Sound(SoundController.laser_fire_sound_filepath)
    
    # @staticmethod
    # def shoot_rocket_sound():
    #     return pygame.mixer.Sound(SoundController.rocket_fire_sound_filepath)
    
    # @staticmethod
    # def ship_movement_sound():
    #     return pygame.mixer.Sound(SoundController.ship_movement_sound_filepath)
    
    # @staticmethod
    # def cursor_hover_sound():
    #     return pygame.mixer.Sound(SoundController.cursor_hover_sound_filepath)
        
    # @staticmethod
    # def cursor_click_sound():
    #     return pygame.mixer.Sound(SoundController.cursor_click_sound_filepath)
    
    # @staticmethod
    # def menu_sound_track():
    #     return pygame.mixer.Sound(SoundController.menu_sound_track_filepath)
    
    # @staticmethod
    # def game_sound_track():
    #     return pygame.mixer.Sound(SoundController.game_sound_track_filepath)
    
    @staticmethod
    def ship_weapon_channel():
        return pygame.mixer.Channel(0)
    
    @staticmethod
    def ship_boost_channel():
        return pygame.mixer.Channel(1)
    
   
    
    # @staticmethod
    # def game_effect_channel():
    #     channel = SoundController._effect_channels[SoundController._current_effect_channel]
    #     SoundController._current_effect_channel = (SoundController._current_channel + 1) % len(SoundController._effect_channels)
    #     return channel
    
    # def play_effect(self, sound):
    #     # Round-robin through effect channels
    #     channel = self.effect_channels[self.current_channel]
    #     self.current_channel = (self.current_channel + 1) % len(self.effect_channels)
    #     channel.play(sound)
    
    @staticmethod
    def game_effect_channel():
        return pygame.mixer.Channel(2)
    
    @staticmethod
    def sound_track_channel():
        return pygame.mixer.Channel(3)