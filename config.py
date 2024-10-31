

import pygame

from customEnum import ShipActions

class ShipConfig():
    # collision variables
    max_collision_force = 50
    
    
    # weapon settings
    cannon_fire_cool_down = 2
    cannon_burst_rate = 7
    cannon_burst_count = 3
    
    rocket_fire_cool_down = 1
    rocket_burst_rate = 5
    rocket_burst_count = 2
    
    # movement
    ship_max_speed = 20
    turn_rate_degrees = 5
    boost_force = 500
    rocket_kick_back_range = 20
    rocket_kick_back_force = 4000
    
    # dimension
    ship_size_scale = .7
    ship_width = 30
    ship_hieght = 40
    
class AsteroidConfig():
    min_size = 8
    max_size = 30
    min_life = 1
    max_life = 5
    min_sides = 7
    max_sides = 12
    min_speed = 7
    max_speed = 15
    min_initial_angular_velocity = 2
    max_initial_angular_velocity = 7
    
class RocketConfig():
    image_path = 'images/rocket.png'
    flare_path = 'images/flare109.png'
    speed = 4
    turn_rate_degrees = 4
    
    # in seconds
    rocket_life = 10
    
class CannonConfig():
    size = 10
    thickness = 2
    speed = 7
   
    

class GlobalConfig():
    width = 800
    height = 600
    world_scale = 5
    

class Colors():
    green_color = (187, 255, 153)
    blue_color = (97, 123, 255)
    red_color = (255, 187, 153)
    drawing_color = (220, 220, 220)
    fill_color = (0, 0, 0)
    background_color = (10, 10, 10)
    debug_color = (50, 111, 50)
    
class ControllerConfig():

    new_level_point = 2000
    
    # params
    base_level_time = 3
    
    # asteroids
    asteroid_spawn_per_level = 30
    max_asteroid_on_screen = 7
    
    # perk
    upgrade_perk_completion = 10
    
    # weapons
    rocket_base_quantity = 20
    
    
class EventConfig():
    time_timer = pygame.USEREVENT + 2
    start_new_game_event = pygame.USEREVENT + 3
    end_game_event = pygame.USEREVENT + 4
    exit_game_event = pygame.USEREVENT + 5
    save_button_map_event = pygame.USEREVENT + 8
    
class MiscConfig():
    map_button_save_location = 'button_map.json'
    
    default_key_map = {
            ShipActions.Boost: 'DOWN',
            ShipActions.Cannon:'LEFT',
            ShipActions.Rocket: 'RIGHT',
            ShipActions.Steer: 'L CLICK'
        }
    
    button_to_event_map = {
        
            pygame.K_a : 'A' ,
            pygame.K_b : 'B' ,
            pygame.K_c : 'C' ,
            pygame.K_d : 'D' ,
            pygame.K_e : 'E' ,
            pygame.K_f : 'F' ,
            pygame.K_g : 'G' ,
            pygame.K_h : 'H' ,
            pygame.K_i : 'I' ,
            pygame.K_j : 'J' ,
            pygame.K_k : 'K' ,
            pygame.K_l : 'L' ,
            pygame.K_m : 'M' ,
            pygame.K_n : 'N' ,
            pygame.K_o : 'O' ,
            pygame.K_p : 'P' ,
            pygame.K_q : 'Q' ,
            pygame.K_r : 'R' ,
            pygame.K_s : 'S' ,
            pygame.K_t : 'T' ,
            pygame.K_u : 'U' ,
            pygame.K_v : 'V' ,
            pygame.K_w : 'W' ,
            pygame.K_x : 'X' ,
            pygame.K_y : 'Y' ,
            pygame.K_z : 'Z' ,
            'M_1' : 'L CLICK' ,
            'M_3' : 'R CLICK' ,
            pygame.K_UP : 'UP' ,
            pygame.K_DOWN : 'DOWN' ,
            pygame.K_LEFT : 'LEFT' ,
            pygame.K_RIGHT : 'RIGHT' ,
        }
    
    
    