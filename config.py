

import pygame


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
    min_size = 12
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
    
class ControllerConfig():

    new_level_point = 2000
    
    # params
    base_level_time = 200
    
    # asteroids
    asteroid_spawn_per_level = 20
    max_asteroid_on_screen = 7
    
    # perk
    upgrade_perk_completion = 10
    
    # weapons
    rocket_base_quantity = 20
    
    
class EventConfig():
    start_new_game_event = pygame.USEREVENT + 3
    end_game_event = pygame.USEREVENT + 4
    exit_game_event = pygame.USEREVENT + 5
    