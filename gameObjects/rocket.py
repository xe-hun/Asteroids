       
import math
import numpy as np
import pygame
from config.GlobalConfig import GlobalConfig
from config.RocketConfig import RocketConfig
# from rocketConfig import RocketConfig
from utils.delay import Delay
from gameObjects.objectBase import ObjectBase, ProjectileBase
from gameObjects.smoke import Smoke
from utils.camera import Camera
from utils.helper import v_angle_diff, v_dot, v_norm, v_rotate, scale


class Rocket(pygame.sprite.Sprite, ObjectBase, ProjectileBase):
    def __init__(self, start_position:tuple, start_direction:tuple, camera:Camera):
        
        super().__init__()
        
        self._camera = camera
        
        self._surface = scale(pygame.image.load(RocketConfig.image_path).convert_alpha(), .2)
        self.image = self._surface.copy()
        self.rect = self.image.get_rect()
        
        self._speed = RocketConfig.speed
        self._angle = 0
        self._position = np.array(start_position)
        self._camera_adjusted_position = self._position.copy()
        self._updated_direction = start_direction
        self._direction = self._updated_direction
        self._turn_rate = math.radians(RocketConfig.turn_rate_degrees)
        self.rect = self.image.get_rect()
        self._target = None
        self._alive = True
        self._smoke = Smoke()
        self.flare_image = scale(pygame.image.load(RocketConfig.flare_path).convert_alpha(), .3)
        self.flare_delay = Delay()
        self.rocket_on = False
        self._rocket_life = RocketConfig.rocket_life
        self._rocket_life_delay = Delay()
        
        
    def to_world_pos(self, vec:tuple):
        return self._camera_adjusted_position + v_rotate(vec, self._angle)
    
    def _draw_flare(self, screen:pygame.surface.Surface):
        rect = self.flare_image.get_rect(center=self.to_world_pos((-7, .2)))
        screen.blit(self.flare_image, rect)
    
    @property
    def has_target(self):
        return self._target is not None
        
    def set_target(self, target):
        if target != None:
            target.rocket_lock(self)
        self._target = target
        
    def _update_target(self):
        
        if self.has_target == False or self._target.alive == False:
            self._target = None
            return
        
        _target_position = np.array(self._target.position)
        self._updated_direction = v_norm(_target_position - self._position)
        
        if v_angle_diff(self._direction, self._updated_direction) < self._turn_rate:
            self._direction = self._updated_direction
        else:
            dotProd = v_dot(self._direction, v_rotate(self._updated_direction, math.pi / 2))
                
            if dotProd > 0:
                self._direction = v_rotate(self._direction, -self._turn_rate)
            elif dotProd < 0:
                self._direction = v_rotate(self._direction, self._turn_rate)
        
    def _on_count_down(self):
        self._rocket_life -= 1
        if self._rocket_life <= 0:
            self._rocket_life_delay = None
            self.dispose()
        
    
    def update(self):
        if self._rocket_life_delay != None:
            self._rocket_life_delay.delay(1000, self._on_count_down, True)
        
        
        self.rocket_on = self.flare_delay.delay(200).is_done
        
        if self.rocket_on:
            speed = self._speed
        else:
            speed = self._speed * .8
    
        self._update_target()
        velocity = self._direction * speed
        self._angle = math.atan2(self._direction[1], self._direction[0])
  
        self._position += velocity
        self._camera_adjusted_position = self._camera.watch(self._position)
        
        self._smoke.update(self.direction, velocity, self._camera_adjusted_position)
        

        
    
    def draw(self, screen:pygame.surface.Surface, glow_screen:pygame.surface.Surface):
        
        if self.rocket_on:
            self._draw_flare(screen)
       
        self.image = pygame.transform.rotate(self._surface, -math.degrees(self._angle))
        self.rect = self.image.get_rect(center = (self._camera_adjusted_position[0], self._camera_adjusted_position[1]))
        screen.blit(self.image, self.rect.topleft)
        
        if self.rocket_on:
            self._smoke.draw(screen)
        
     
        
    @property
    def position(self):
        return self._position
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def alive(self):
        return self._alive
    
    def dispose(self):
        self._alive = False
        
    def is_out_of_screen(self):
        if self._position[0] > GlobalConfig.width or self._position[0] < 0 or \
            self._position[1] > GlobalConfig.height or self._position[1] < 0:
                return True
        else:
            return False
        
    
    
    