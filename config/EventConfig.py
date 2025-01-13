

    
import pygame


class EventConfig():
    time_timer = pygame.USEREVENT + 2
    start_new_game_event = pygame.USEREVENT + 3
    end_game_event = pygame.USEREVENT + 4
    exit_game_event = pygame.USEREVENT + 5
    shake_event = pygame.USEREVENT + 6
    save_button_map_event = pygame.USEREVENT + 8
    # tips_timer = pygame.USEREVENT + 9