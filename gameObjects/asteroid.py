import random
from config.asteroidConfig import AsteroidConfig
from config.GlobalConfig import GlobalConfig
from utils.colors import Colors
    
import math
import pygame
import numpy as np
import Box2D

from gameObjects.objectBase import ObjectBase
from utils.camera import Camera
from utils.helper import Helper, debug_draw_box2D_bodies, map_value, v_normalize, to_box2D_coordinate, v_to_component, to_pixel_coordinate, wrap_box2D_object


class Asteroid(pygame.sprite.Sprite, ObjectBase):
    def __init__(self, world:Box2D.b2World, game_level:int, camera:Camera, position:tuple = None, debug_draw:bool = False, halfSize:float = None):
        debug_draw = False
        
        super().__init__()
        self.debug_draw = debug_draw
        self._camera = camera
        self._world = world
        self.box2D_bodies_debug_list = []
        # outOfBoundsExtension prevents the asteroid from being remove right after creation
        # because its created out of bounds, 
        # shifts the out of bound margin by outOfBoundsExtension
        self.out_of_bounds_Extension = 50 / GlobalConfig.world_scale
        creation_extension = 30 / GlobalConfig.world_scale
        
        # asteroid constants
        MIN_SIZE = AsteroidConfig.min_size
        MAX_SIZE = AsteroidConfig.max_size(game_level)
        MIN_LIFE = AsteroidConfig.min_life
        MAX_LIFE = AsteroidConfig.max_life(game_level)
        self._asteroid_max_speed = Helper.convert_pixel_frame_to_meters_second(AsteroidConfig.max_speed)

        # MIN_LIFE = AsteroidConfig.min_life 
        # MAX_LIFE = AsteroidConfig.max_life(game_level)
     
        
       
        stroke_width = 2
        self._breakage_threshold = MIN_SIZE
        
        self._asteroid_half_size =  np.random.randint(MIN_SIZE, MAX_SIZE) if halfSize is None else halfSize
    
        self._asteroid_life = int(map_value(MIN_SIZE, MAX_SIZE, MIN_LIFE, MAX_LIFE, self._asteroid_half_size))
      

        x, y, direction = self._generate_initial_states(creation_extension)
     
        
        if position is None:
            self._position = (x, y)
        else:
            self._position = position
            
        self._direction = direction  
        self._speed = AsteroidConfig.min_speed + random.random() * AsteroidConfig.max_speed
   
        box_2d_velocity = Helper.invert_y_axis(self._direction) * Helper.convert_pixel_frame_to_meters_second(self._speed)
        
        initial_angular_velocity = AsteroidConfig.min_initial_angular_velocity + random.random() * AsteroidConfig.max_initial_angular_velocity
        
        
        self._asteroid_body_box2D = self._create_asteroid_body_box2D_circle(self._asteroid_half_size, self._world, self._position, box_2d_velocity, initial_angular_velocity)


         
        self._surface = self._draw_asteroid_in_pixel_circle(self._asteroid_half_size, stroke_width)
        self.image = self._surface
        self.rect = self._surface.get_rect()
        self._alive = True
        self._rocket_lock = None
        
        
    def _generate_initial_states(self, creation_extension):
        
        pi = math.pi
        world_height, world_width = GlobalConfig.height, GlobalConfig.width
        
        
        return tuple(random.choices([
            (-creation_extension,                           np.random.rand() * world_height,   v_to_component(map_value(0, 1, -0.25 * pi, 0.25 * pi, np.random.rand()))),
            (world_width + creation_extension,               np.random.rand() * world_height,   v_to_component(map_value(0, 1, 0.75 * pi , 1.25 * pi, np.random.rand()))),
            (np.random.rand() * world_width,    world_height + creation_extension,              v_to_component(map_value(0, 1, 1.25 * pi , 1.75 * pi, np.random.rand()))),
            (np.random.rand() * world_width,    -creation_extension,                           v_to_component(map_value(0, 1, 0.25 * pi , 0.75 * pi, np.random.rand()))),
         ],
         weights=[1,1,1,1]).pop())
        
   
    
    def _create_asteroid_body_box2D_circle(self, radius, world:Box2D.b2World, position, linear_velocity, angular_velocity):
        
        position = to_box2D_coordinate(position, GlobalConfig.world_scale, GlobalConfig.height)
        
        
        asteroid_body = world.CreateDynamicBody(position = position,
                                               linearVelocity = linear_velocity,
                                               angularVelocity = angular_velocity,
                                               userData = self,
                                            )
        
        asteroidShape = Box2D.b2CircleShape(radius = radius / GlobalConfig.world_scale)
        asteroid_body.CreateFixture(
            shape = asteroidShape,
            density = 1,
            friction = .3,
            restitution = .4
        )
        
        self.box2D_bodies_debug_list.append(asteroid_body)
        return asteroid_body
        

    def _draw_asteroid_in_pixel_circle(self, radius, stroke_width):
        # shift the polygon so that pos 0, 0 is at top left for pygame coordinate

        asteroid_surface = pygame.Surface((radius * 2 + stroke_width , radius * 2 + stroke_width), pygame.SRCALPHA)
   
        pygame.draw.circle(asteroid_surface, Colors.fill_color, (radius + stroke_width / 2,) * 2, radius)
        pygame.draw.circle(asteroid_surface, Colors.drawing_color,  (radius + stroke_width / 2,) * 2, radius, stroke_width)
        return asteroid_surface
        
        
    def take_damage(self):
        self._asteroid_life -= 1
        if self._asteroid_life <= 0:
            self._alive = False
            
  
    def _update_rocket_lock(self):
        if self._rocket_lock != None and self._rocket_lock.alive == False:
            self._rocket_lock = None
    
    def rocket_lock(self, rocket):
        self._rocket_lock = rocket
        
    @property
    def is_locked_on(self):
        return self._rocket_lock != None
        
    
    @property
    def alive(self):
       return self._alive
            
    
    @property
    def position(self):
        return self._position
    
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def velocity(self):
        return Helper.convert_meters_second_to_pixel_frame(Helper.invert_y_axis(self._asteroid_body_box2D.linearVelocity))
      
    
    @property
    def speed(self):
        return self._speed
    
    
    def can_break_apart(self):
        return self._asteroid_half_size > self._breakage_threshold * 2
        
    
    def break_apart(self, game_level, debug_draw:bool):
      
        break_parts = AsteroidConfig.get_break_parts(game_level)
        asteroids = []
        for _ in range(break_parts):
            asteroidHalfSize = max(((self._asteroid_half_size + np.random.randn() * 10)/ 2), self._breakage_threshold)
            asteroid = Asteroid(self._world, game_level, self._camera, self._position, debug_draw, asteroidHalfSize)
            asteroids.append(asteroid)
        return asteroids
        
       
    def dispose(self):
        self._alive = False
        self._surface = None
        self._world.DestroyBody(self._asteroid_body_box2D)
        pass
    

    def update(self):
                
        self._update_rocket_lock()
        wrap_box2D_object(self._asteroid_body_box2D)  
        self._position = to_pixel_coordinate(self._asteroid_body_box2D.position, GlobalConfig.world_scale, GlobalConfig.height) 
        self._position = self._camera.watch(self._position)
        Helper.cap_box2D_body_speed(self._asteroid_body_box2D, self._asteroid_max_speed)
 
    def draw(self, screen:pygame.surface.Surface):
        
        angleRad = self._asteroid_body_box2D.angle
        self.image = pygame.transform.rotate(self._surface, math.degrees(angleRad - math.pi))
        self.rect = self.image.get_rect(center=self._position)
        
        screen.blit(self.image, self.rect.topleft)  
        
        if self.debug_draw:
            debug_draw_box2D_bodies(screen, self.box2D_bodies_debug_list)
