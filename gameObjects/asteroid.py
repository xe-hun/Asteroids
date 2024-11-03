import random
from asteroidParameter import AsteroidParameter
from config import Colors, GlobalConfig
    
import math
import pygame
import numpy as np
import Box2D

from gameObjects.objectBase import ObjectBase
from utils.camera import Camera
from utils.helper import Helper, debug_draw_box2D_bodies, map_value, v_norm, to_box2D_position, v_to_component, to_pixel_position, wrap_box2D_object


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
        MIN_SIZE = AsteroidParameter.min_size
        MAX_SIZE = AsteroidParameter.max_size(game_level)
        MIN_LIFE = AsteroidParameter.min_life
        MAX_LIFE = AsteroidParameter.max_life(game_level)
     
        
       
        stroke_width = 2
        self._breakage_threshold = MIN_SIZE
        
        self._asteroid_half_size =  np.random.randint(MIN_SIZE, MAX_SIZE) if halfSize is None else halfSize
        # num_side = np.random.randint(MIN_SIDES, MAX_SIDES)
          # map the asteroid life according to its size
        self._asteroid_life = int(map_value(MIN_SIZE, MAX_SIZE, MIN_LIFE, MAX_LIFE, self._asteroid_half_size))
      

        x, y, direction = self._generate_initial_states(creation_extension)
     
        
        if position is None:
            self._position = (x, y)
        else:
            self._position = position
            
        self._direction = direction
        
        SPEED = AsteroidParameter.min_speed + random.random() * AsteroidParameter.max_speed
        initial_linear_velocity = self._direction * SPEED
        initial_angular_velocity = AsteroidParameter.min_initial_angular_velocity + random.random() * AsteroidParameter.max_initial_angular_velocity
   
        # lenght_displacement_range = self._asteroid_half_size * .3
        # angle_displacement_range = .05
        
        
      
        # polygon_points = self._create_polygon_points(self._asteroid_half_size, num_side, lenght_displacement_range, angle_displacement_range)
        # self._asteroid_body_box2D = self._create_asteroid_body_box2D(polygon_points, self._world, self._position, initial_linear_velocity, initial_angular_velocity)
        
        self._asteroid_body_box2D = self._create_asteroid_body_box2D_circle(self._asteroid_half_size, self._world, self._position, initial_linear_velocity, initial_angular_velocity)


         
        # self._surface = self._draw_asteroid_in_pixel(polygon_points, self._asteroid_half_size, stroke_width)
        self._surface = self._draw_asteroid_in_pixel_circle(self._asteroid_half_size, stroke_width)
        self.image = self._surface
        self.rect = self._surface.get_rect()
        self._alive = True
        self._rocket_lock = None
        
        
    def _generate_initial_states(self, creation_extension):
        
        pi = math.pi
        world_height, world_width = GlobalConfig.height, GlobalConfig.width
        
        
        return tuple(random.choices([
            (-creation_extension,                           np.random.rand() * world_height,   v_norm(v_to_component(map_value(0, 1, -0.25 * pi, 0.25 * pi, np.random.rand())))),
            (world_width + creation_extension,               np.random.rand() * world_height,   v_norm(v_to_component(map_value(0, 1, 0.75 * pi , 1.25 * pi, np.random.rand())))),
            (np.random.rand() * world_width,    world_height + creation_extension,              v_norm(v_to_component(map_value(0, 1, 1.25 * pi , 1.75 * pi, np.random.rand())))),
            (np.random.rand() * world_width,    -creation_extension,                           v_norm(v_to_component(map_value(0, 1, 0.25 * pi , 0.75 * pi, np.random.rand())))),
         ],
         weights=[1,1,1,1]).pop())
        
   
        
    # def _create_polygon_points(self, asteroid_half_size, num_side, lenght_displacement_range, angle_displacement_range):
    #     # give the polygon uneven sides and angles
       
    #     displacement = [(asteroid_half_size - np.random.randint(0, lenght_displacement_range), asteroid_half_size -np.random.randint(0, lenght_displacement_range)) for _ in range(num_side)]
    #     poly_angles = [np.random.randn() * angle_displacement_range + x for x in np.linspace(0, math.pi * 2 , num_side)]
        
    #     # add displacement values to each sides and angles of the polygon
    #     polygon_points = [(displacement[i][0] * math.cos(j), displacement[i][1] * math.sin(j)) for i, j in enumerate(poly_angles) if i < num_side - 1]
       
    #     return polygon_points
        
        
    # def _create_asteroid_body_box2D(self, polygon_points, world:Box2D.b2World, position, linear_velocity, angular_velocity):
        
    #     position = to_box2D_position(position, GlobalConfig.world_scale, GlobalConfig.height)
        
    #     # scale the polygon points to world dimension
    #     polygon_points = [(p[0] / GlobalConfig.world_scale, p[1] / GlobalConfig.world_scale) for p in polygon_points]
    #     # invert the x axis to account for inverted angle rotation when creating the polygon points
    #     polygon_points = [(-p[0], p[1]) for p in polygon_points]
        
    #     asteroid_body = world.CreateDynamicBody(position = position,
    #                                            linearVelocity = linear_velocity,
    #                                            angularVelocity = angular_velocity,
    #                                            userData = self,
    #                                         )
        
    #     asteroidShape = Box2D.b2PolygonShape(vertices = polygon_points)
    #     asteroid_body.CreateFixture(
    #         shape = asteroidShape,
    #         density = 1,
    #         friction = .3,
    #         restitution = .4
    #     )
        
    #     self.box2D_bodies_debug_list.append(asteroid_body)
    #     return asteroid_body
        

    # def _draw_asteroid_in_pixel(self, polygon_oints, asteroid_half_size, stroke_width):
    #     # shift the polygon so that pos 0, 0 is at top left for pygame coordinate

    #     polygon_points_shifted = [(polygon_oints[i][0] + asteroid_half_size, polygon_oints[i][1] + asteroid_half_size) for i in range(len(polygon_oints))]
    #     asteroid_surface = pygame.Surface((asteroid_half_size * 2 + stroke_width , asteroid_half_size * 2 + stroke_width), pygame.SRCALPHA)
    #     pygame.draw.polygon(asteroid_surface, Colors.fill_color, polygon_points_shifted)
    #     pygame.draw.polygon(asteroid_surface, Colors.drawing_color, polygon_points_shifted, stroke_width)
       
    #     return asteroid_surface
    
    
    def _create_asteroid_body_box2D_circle(self, radius, world:Box2D.b2World, position, linear_velocity, angular_velocity):
        
        position = to_box2D_position(position, GlobalConfig.world_scale, GlobalConfig.height)
        
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
    
    
    def can_break_apart(self):
        return self._asteroid_half_size > self._breakage_threshold * 2
        
    
    def break_apart(self, game_level, debug_draw:bool):
        # position = self.asteroidBodybox2D.position
        # break_parts = random.choices([2, 3, ],[5, 1])[0]
        break_parts = AsteroidParameter.get_break_parts(game_level)
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
        self._position = to_pixel_position(self._asteroid_body_box2D.position, GlobalConfig.world_scale, GlobalConfig.height) 
        self._position = self._camera.watch(self._position)
        Helper.cap_box2D_body_speed(self._asteroid_body_box2D, AsteroidParameter.max_speed)
 
    def draw(self, screen:pygame.surface.Surface):
        
        angleRad = self._asteroid_body_box2D.angle
        self.image = pygame.transform.rotate(self._surface, math.degrees(angleRad - math.pi))
        self.rect = self.image.get_rect(center=self._position)
        screen.blit(self.image, self.rect.topleft)  
        
        if self.debug_draw:
            debug_draw_box2D_bodies(screen, self.box2D_bodies_debug_list)
