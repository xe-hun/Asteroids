import math
import random
import numpy as np
import pygame
import Box2D
from config import Colors, GlobalConfig, MiscConfig
from customEnum import ShipActions, Steering


from soundController import SoundController
from utils.animationHandler import AnimationHandler
from gameObjects.objectBase import ObjectBase
from gameObjects.rocket import Rocket
from shipParameter import ShipParameter
from strategies.shootingStrategy import ShootingStrategy
from utils.camera import Camera
from utils.box2DHelperClasses import RaycastCallback
from utils.helper import Helper, v_angle_diff, check_box2D_object_in_bounds, clamp, v_dot, v_norm, v_rotate, scale, v_to_angle, v_to_component, to_box2D_position,\
                        to_pixel_position, debug_draw_box2D_bodies
from gameObjects.cannon import Cannon
from utils.watcher import Watcher



class Ship(pygame.sprite.Sprite, ObjectBase):
    
    def __init__(self, world:Box2D.b2Body,  camera:Camera, register_projectile:callable, register_damage:callable, report_projectile_fire:callable, ship_level:int = 1, debugDraw:bool = False):
        
        self._debugDraw = debugDraw
        self._report_projectile_fire = report_projectile_fire
        self._alive = True
        self._steer_on = False
        self.in_boundary = True
        self._is_colliding = False
        
        self._collision_force = 0
        
      
        self.MAX_COLLISION_FORCE = ShipParameter.max_collision_force
      
        self._set_ship_parameters(ship_level)
        
        # ship dimensions
        self.SHIP_SIZE_SCALE = ShipParameter.ship_size_scale
        self.SHIP_WIDTH = ShipParameter.ship_width * self.SHIP_SIZE_SCALE
        self.SHIP_HEIGHT = ShipParameter.ship_hieght * self.SHIP_SIZE_SCALE
        self.SHIP_BASE_POINT = - self.SHIP_WIDTH / (2 * GlobalConfig.world_scale)
        
        # ship flags
        self._register_projectile = register_projectile
        self._register_damage = register_damage
        
        self._boosting = False
        self._steering = Steering.noSteering
        self._steering1 = Steering.noSteering
   
        
        # ship parameters
        self._turn_force = 0
        self._position = (GlobalConfig.width // 2, GlobalConfig.height // 2)
   

        # rocket kick back parameters
        self.ROCKET_KICK_BACK_RANGE = ShipParameter.rocket_kick_back_range
        self.ROCKET_KICK_BACK_FORCE = ShipParameter.rocket_kick_back_force
        
        # building the shop
        # polygon points for ship frame centered on zero
        # ships width is 30 and ships height is 40
        b2_vec2 = Box2D.b2Vec2
        polygon_points =  [ b2_vec2(-15,-20) * self.SHIP_SIZE_SCALE, b2_vec2(-8, -15) * self.SHIP_SIZE_SCALE, b2_vec2(0, -20) * self.SHIP_SIZE_SCALE,
                          b2_vec2(8, -15) * self.SHIP_SIZE_SCALE, b2_vec2(15, -20) * self.SHIP_SIZE_SCALE, b2_vec2(0, 20) * self.SHIP_SIZE_SCALE]
        # seperate the polygon shapes to mitigate against
        # convex shape for box2D
        polygon_points_seperated =  [[b2_vec2(-15,-20) * self.SHIP_SIZE_SCALE, b2_vec2(-8, -15) * self.SHIP_SIZE_SCALE, b2_vec2(0, 20) * self.SHIP_SIZE_SCALE],
                                    [b2_vec2(-8, -15) * self.SHIP_SIZE_SCALE, b2_vec2(0, -20) * self.SHIP_SIZE_SCALE, b2_vec2(8, -15) * self.SHIP_SIZE_SCALE, b2_vec2(0, 20) * self.SHIP_SIZE_SCALE],    
                                    [b2_vec2(8, -15) * self.SHIP_SIZE_SCALE, b2_vec2(15, -20) * self.SHIP_SIZE_SCALE, b2_vec2(0, 20) * self.SHIP_SIZE_SCALE]]
                                  
        
        self._ship_surface, self.rect = self._build_ship_in_pixel(self._position,
                                            self.SHIP_WIDTH, self.SHIP_HEIGHT, list(polygon_points))
        
        self.image = self._ship_surface
        
        self._world = world
        self._box2D_bodies_debug_list = []
        
        _ship_position_in_box2D = to_box2D_position(self._position, GlobalConfig.world_scale, GlobalConfig.height)
        self._ship_body_box2D = self._build_ship_body_box2D(self._world, _ship_position_in_box2D, list(polygon_points_seperated))
        
        self._camera = camera
        
        # alternates between left and right rocket
        self.rocket_alternate = False
        self.flare_image = scale(pygame.image.load('images/flare109.png').convert_alpha(), .5)
        # self.flare_image.set_alpha(.9)
        self.animation_handler = AnimationHandler('images/flame101x186.png', 101, 186, 5, .13)


    def _set_ship_parameters(self, ship_level):
        CANNON_FIRE_COOL_DOWN = ShipParameter.cannon_fire_cool_down(ship_level)
        CANNON_BURST_RATE = ShipParameter.cannon_burst_rate(ship_level)
        CANNON_BURST_COUNT = ShipParameter.cannon_burst_count(ship_level)

        
        ROCKET_FIRE_COOL_DOWN = ShipParameter.rocket_fire_cool_down(ship_level)
        ROCKET_BURST_RATE = ShipParameter.rocket_burst_rate
        ROCKET_BURST_COUNT = ShipParameter.rocket_burst_count(ship_level)
     
        
        self._cannon_fire_strategy = ShootingStrategy(CANNON_FIRE_COOL_DOWN, CANNON_BURST_RATE, CANNON_BURST_COUNT, self._report_projectile_fire, Cannon)
        self._rocket_fire_strategy = ShootingStrategy(ROCKET_FIRE_COOL_DOWN, ROCKET_BURST_RATE, ROCKET_BURST_COUNT, self._report_projectile_fire, Rocket)
        
        self.MAXSPEED = ShipParameter.ship_max_speed(ship_level)
        # turn rate in degrees
        self.TURN_RATE = math.radians(ShipParameter.turn_rate_degrees(ship_level))
        self.BOOST_FORCE = ShipParameter.boost_force(ship_level)
        
        self._ship_level_watcher = Watcher(self._on_ship_level_change, ship_level)
    
    def _on_ship_level_change(self, value):
        self._set_ship_parameters(value)
        
       

        
    def _build_ship_body_box2D(self, world:Box2D.b2World, position, _polygon_points_list):
        
        ship_body = world.CreateDynamicBody(position = position, userData = self,)
        
        for polygon_points in _polygon_points_list:
            # scale down polygon points from pixel space to world space
            polygonPointsInWorldScale = [p / GlobalConfig.world_scale for p in polygon_points]
            
            ship_body.CreateFixture(
                density = 1,
                friction = .3,
                shape = Box2D.b2PolygonShape(vertices = polygonPointsInWorldScale)
            )
        
        self._box2D_bodies_debug_list.append(ship_body)
        ship_body.fixedRotation = True
        ship_body.inertia = 50
        # Box2D.b2Body.angularDamping = 500
        return ship_body
    
        
    def _build_ship_in_pixel(self, position, ship_width, ship_height, polygon_points):
        # shift the polygon points by half width and half ship height to make top left 0,0 for pygame coordinate
        stroke_size = 2
        polygon_points_shifted = [(i[0] + ship_width / 2 , i[1] + ship_height / 2 ) for i in polygon_points]
        
        ship_surface = pygame.Surface((ship_width + stroke_size, ship_height + stroke_size), pygame.SRCALPHA)
        pygame.draw.polygon(ship_surface, Colors.fill_color, polygon_points_shifted)
        pygame.draw.polygon(ship_surface, Colors.drawing_color, polygon_points_shifted, stroke_size)
        rect = ship_surface.get_rect(center=(position))

        
        return ship_surface, rect
    
    
    def collision_begins(self):
        self._is_colliding = True
     
    
    def collision_ends(self):
        if self._is_colliding:
            
            self._collision_force = min(self._collision_force, self.MAX_COLLISION_FORCE)
            penalty_point = self._collision_force / (2 * self.MAX_COLLISION_FORCE)
            self._register_damage(penalty_point)
        
        self._is_colliding = False
        self._collision_force = 0
       
    
    def get_collision_impulse(self, normal_impulse):
        self._collision_force = max(normal_impulse, self._collision_force)
        
        
    def _handle_mapped_key_press(self, event:pygame.event.Event, ship_action:ShipActions, key_map:dict, on_button_down:callable, on_button_up:callable):
        key_map_value = key_map[ship_action]
        key_map_key = next((k for k, v in MiscConfig.button_to_event_map.items() if v == key_map_value), None)
        
        if str(key_map_key).casefold().startswith('m'):
            key = int(key_map_key.split('_')[1])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == key:
                on_button_down()
                
            if event.type == pygame.MOUSEBUTTONUP and event.button == key:
                on_button_up()
                
        else:
            key = int(key_map_key)
            if event.type == pygame.KEYDOWN and event.key == key:
                on_button_down()
                
            if event.type == pygame.KEYUP and event.key == key:
                on_button_up()
        
    def _set_ship_boost(self, value:bool):
        self._boosting = value
        
    def _set_ship_cannon(self, value:bool):
        self._cannon_fire_strategy.shooting = value
        
    def _set_ship_rocket(self, value:bool):
        self._rocket_fire_strategy.shooting = value
        
    def _set_ship_steer(self, value:bool):
        self._steer_on = value
        

        
    def handle_event(self, event: pygame.event.Event, key_map : dict):
        self._handle_mapped_key_press(event, ShipActions.Boost, key_map, lambda: self._set_ship_boost(True), lambda: self._set_ship_boost(False))
        self._handle_mapped_key_press(event, ShipActions.Cannon, key_map, lambda: self._set_ship_cannon(True), lambda: self._set_ship_cannon(False))
        self._handle_mapped_key_press(event, ShipActions.Rocket, key_map, lambda: self._set_ship_rocket(True), lambda: self._set_ship_rocket(False))
        self._handle_mapped_key_press(event, ShipActions.Steer, key_map, lambda: self._set_ship_steer(True), lambda: self._set_ship_steer(False))
      
                
        
       
    def _fire_cannon(self):
        SoundController.ship_weapon_channel().play(SoundController.laser_fire_sound)
        cannon_position = to_pixel_position(self._ship_body_box2D.GetWorldPoint((-5/GlobalConfig.world_scale, 15/GlobalConfig.world_scale)), GlobalConfig.world_scale, GlobalConfig.height)
        cannon_position = self._camera.watch(cannon_position)
        cannon = Cannon(self.direction, cannon_position, self._camera)
        self._register_projectile(cannon)
        
    def _fire_missile(self):
        xPos = -10 if self.rocket_alternate else 10
        self.rocket_alternate = not self.rocket_alternate
        
        rocket_position = to_pixel_position(self._ship_body_box2D.GetWorldPoint((xPos/GlobalConfig.world_scale, 15/GlobalConfig.world_scale)), GlobalConfig.world_scale, GlobalConfig.height)
        rocket_position = self._camera.watch(rocket_position)
        missile = Rocket(rocket_position, self.direction, self._camera)
        self._register_projectile(missile)
        SoundController.ship_weapon_channel().play(SoundController.rocket_fire_sound)
        
    @property
    def position(self):
        return self._position
        
    @property
    def direction(self):
        return v_norm(v_to_component(- self._ship_body_box2D.angle - math.pi / 2))
        
    @property
    def alive(self):
        return self._alive
    
    def dispose(self):
        self._alive = False
        self._ship_surface = None
        self._world.DestroyBody(self._ship_body_box2D)

       
   
    def update(self, ship_level):
        
        self._ship_level_watcher.watch(ship_level)
        
        self._steer_ship()
        
        self.in_boundary = check_box2D_object_in_bounds(self._ship_body_box2D)
        
        if self.in_boundary:
            self._cannon_fire_strategy.update(self._fire_cannon)
            self._rocket_fire_strategy.update(self._fire_missile)
          
    
        self._boost_ship(self._ship_body_box2D, self._boosting, self.BOOST_FORCE, self.SHIP_BASE_POINT)
        self._kick_back_thrust(self._ship_body_box2D, self.ROCKET_KICK_BACK_RANGE, self.ROCKET_KICK_BACK_FORCE, self.SHIP_BASE_POINT)
        Helper.cap_box2D_body_speed(self._ship_body_box2D, self.MAXSPEED)
            
        # wrap_box2D_object(self._ship_body_box2D)   
        
        self._position = to_pixel_position(self._ship_body_box2D.position, GlobalConfig.world_scale, GlobalConfig.height) 
        self._position = self._camera.watch(self.position)
        
    
    def draw(self, screen:pygame.surface.Surface):
      
        
        degree_angle = math.degrees(self._ship_body_box2D.angle - math.pi)
        
        if self._boosting == True:
            self._draw_flame(screen, degree_angle)
            
        
        self.image = pygame.transform.rotate(self._ship_surface, degree_angle)
        self.rect = self.image.get_rect(center=self._position)
        screen.blit(self.image, self.rect.topleft) 
        
        # if self._boosting == True:
        #     self._draw_flare(screen)
        
        
        
        if self._debugDraw:
            debug_draw_box2D_bodies(screen, self._box2D_bodies_debug_list)
        
            
    def _draw_flame(self, screen:pygame.surface.Surface, angle:float):
        rocket_pos = to_pixel_position(self._ship_body_box2D .GetWorldPoint((.2, self.SHIP_BASE_POINT - 2)), GlobalConfig.world_scale, GlobalConfig.height)
        self.animation_handler.animate(rocket_pos, angle, screen)
        
        
    def _draw_flare(self, screen:pygame.surface.Surface):
        rocket_pos = to_pixel_position(self._ship_body_box2D .GetWorldPoint((0, self.SHIP_BASE_POINT-.5)), GlobalConfig.world_scale, GlobalConfig.height)
        rect = self.flare_image.get_rect(center=rocket_pos)
        screen.blit(self.flare_image, rect)
   
    def _boost_ship(self, ship_body:Box2D.b2Body, boosting:bool, boost_force:int, ship_base_position:float):
        
        if SoundController.ship_boost_channel().get_busy() == False and boosting == True:
        
            # self._sound_strategy.channel2().play(self._sound_strategy.ship_movement_sound())
            SoundController.ship_boost_channel().play(SoundController.ship_movement_sound, -1, fade_ms=500)
            # pygame.mixer.music.set_pos(random.random())

        elif SoundController.ship_boost_channel().get_busy() == True and boosting == False:
       
            SoundController.ship_boost_channel().stop()
            
        
        if boosting == False:
            return
        
        force_point = ship_body.GetWorldPoint((0, ship_base_position))
        thrust_vector = boost_force * v_to_component(ship_body.angle + math.pi / 2)
        ship_body.ApplyForce(thrust_vector, force_point, True)
        
        
      
        
    def _kick_back_thrust(self, shipBody:Box2D.b2Body, rocket_kick_back_range, rocket_kick_back_force, ship_base_position):
        
        thrust_direction = - v_to_component(shipBody.angle + math.pi / 2)
        
        ray_cast_start = shipBody.GetWorldPoint((0, ship_base_position))
        rayCastEnd = ray_cast_start + (rocket_kick_back_range * thrust_direction)
        # self.debugDrawRayCast(rayCastStart, rayCastEnd, screen)
       
        ray_cast_callback = RaycastCallback()
        self._world.RayCast(ray_cast_callback, ray_cast_start, rayCastEnd)
        
        ray_cast_hit =  ray_cast_callback.fixture and ray_cast_callback.fixture.body != self._ship_body_box2D
        if self._boosting and ray_cast_hit:
           
            # apply anti thrust force
            distance_from_ship = (ray_cast_callback.point - ray_cast_start).length
            k_b_impact = rocket_kick_back_force * (1 - distance_from_ship / rocket_kick_back_range)
            k_b_magnitude = k_b_impact * thrust_direction
            
            hit_body = ray_cast_callback.fixture.body
            hit_body.ApplyForce(k_b_magnitude, ray_cast_callback.point, True)
       
    
    def _debug_draw_ray_cast(self, ray_cast_start, ray_cast_end, screen):
        ray_cast_start_in_pixel = to_pixel_position(ray_cast_start, GlobalConfig.world_scale, GlobalConfig.height)
        ray_cast_end_in_pixel = to_pixel_position(ray_cast_end, GlobalConfig.world_scale, GlobalConfig.height)
        pygame.draw.line(screen, (255, 10, 10), ray_cast_start_in_pixel, ray_cast_end_in_pixel)
       
        
    def _steer_ship(self):
        if self._steer_on == True:
            # calculate ship angle to mouse
            mouse_dir = np.array(pygame.mouse.get_pos()) - np.array(self.position)
            angle_to_mouse = v_angle_diff(self.direction, mouse_dir)
            
            # min_angle_unit = 0.017
            min_angle_unit = 0.017
            damping_range = math.radians(30)
            damping_rate = 0.1
            unit_turn_rate = math.radians(.05)
            
            if angle_to_mouse <= min_angle_unit:
                self._ship_body_box2D.angle = -v_to_angle(v_rotate(mouse_dir, math.pi / 2))
            else:
           
                angle_dot = v_dot(self.direction, v_rotate(mouse_dir, math.pi / 2))
                if angle_dot > 1:
                    if angle_to_mouse <= damping_range:
                        # self._turn_force = (angle_to_mouse / damping_range) * (min_angle_unit / 2)
                        self._turn_force = (angle_to_mouse / damping_range) * damping_rate
                    else: 
                        self._turn_force += unit_turn_rate
                        
                elif angle_dot < 1:
                  
                    if angle_to_mouse <= damping_range:
                        # self._turn_force = -(angle_to_mouse / damping_range ) * (min_angle_unit / 2)
                        self._turn_force = -(angle_to_mouse / damping_range ) * damping_rate
                    else: 
                        self._turn_force -= unit_turn_rate
                    
                self._turn_force = clamp(-self.TURN_RATE, self.TURN_RATE, self._turn_force,)
                
        else:
            self._turn_force *= .95
            if abs(self._turn_force) <= .005:
                self._turn_force = 0
            
        self._ship_body_box2D.angle += self._turn_force
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # if self._mouse_down == True:
        #     # calculate ship angle to mouse
        #     mouse_dir = np.array(pygame.mouse.get_pos()) - np.array(self.position)
        #     angle_to_mouse = angle_diff(self.direction, mouse_dir)
            
        #     self._turn_force += math.radians(1)
        #     tr = math.radians(5)
        #     self._turn_force = min(self._turn_force, tr)
        #     angle_dot = dot(self.direction, rotate_vec(mouse_dir, math.pi / 2))
        #     if angle_dot > 1:
        #         self._ship_body_box2D.angle += self._turn_force
        #         self.steering1 = Steering.steeringRight
        #     elif angle_dot < 1:
        #         self._ship_body_box2D.angle -= self._turn_force
        #         self.steering1 = Steering.steeringLeft
                
        # else:   
        #     self._turn_force *= .8
        #     if self._turn_force <= .0001:
        #         self._turn_force = 0
        #         self.steering1 = Steering.noSteering
                
        #     if self.steering1 == Steering.steeringRight:
        #         self._ship_body_box2D.angle += self._turn_force
        #     elif self.steering1 == Steering.steeringLeft:
        #         self._ship_body_box2D.angle -= self._turn_force
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        #          self._turn_force += math.radians(.2)
        #     self._turn_force = min(self._turn_force, self.TURN_RATE)
        #     angle_dot = dot(self.direction, rotate_vec(mouse_dir, math.pi / 2))
        #     if angle_dot > 1:
        #         self._ship_body_box2D.angle += self._turn_force
        #         self.steering1 = Steering.steeringRight
        #     elif angle_dot < 1:
        #         self._ship_body_box2D.angle -= self._turn_force
        #         self.steering1 = Steering.steeringLeft
                
        # else:   
        #     self._turn_force *= .8
        #     if self._turn_force <= .0001:
        #         self._turn_force = 0
        #         self.steering1 = Steering.noSteering
                
        #     if self.steering1 == Steering.steeringRight:
        #         self._ship_body_box2D.angle += self._turn_force
        #     elif self.steering1 == Steering.steeringLeft:
        #         self._ship_body_box2D.angle -= self._turn_force
            
        
                
      
                
        
                
        # self._ship_body_box2D.angle += self._turn_force
            
            # self._turn_force = max(self._turn_force, 0)
            
            
            
        
            
            
                
            
            
                
            
            
            # increment the turn rate
      
        
        
        # self._turn_force += .2
        # self._turn_force = min(self._turn_force, self.TURN_RATE)
        
        # if steering == Steering.steeringRight:
        #     self._ship_body_box2D.angle -= math.radians(self._turn_force)
        # elif steering == Steering.steeringLeft:
        #     self._ship_body_box2D.angle += math.radians(self._turn_force)
        # elif steering == Steering.noSteering:
        #     self._turn_force = 0
    
        