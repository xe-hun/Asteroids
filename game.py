import math
import random
import numpy as np
import pygame
import Box2D
from config.event_config import  EventConfig
from config.controller_config import ControllerConfig
from gRouter import G_Router
from gameObjects.objectBase import ObjectBase
from pages.page_base import PageBase
from pages.pauseScreen import PauseScreen
from strategies.penaltyStrategy import PenaltyStrategy
from soundController import SoundController
from strategies.spawnStrategy import SpawnStrategy
from ui.timedList import TimedList
from utils.lerp import Lerp
from utils.delay import Delay
from effects.worldStar import WorldStar
from gameObjects.explosion import Explosion
from gameObjects.perk import Perk, PerkType
from gameObjects.rocket import Rocket
from gameObjects.sparks import Sparks
from gameStateController import GameStateController
from utils.helper import get_target_within_range, v_mag, v_to_angle
from utils.camera import Camera
from utils.box2DHelperClasses import CollisionFilter, ContactListener
from gameObjects.asteroid import Asteroid
from gameObjects.cannon import Cannon
from constant import MAX_ASTEROID_PER_LEVEL, SHAKE_DURATION, SHAKE_EVENT, SHAKE_FREQUENCY, SHAKE_INTENSITY, WIDTH, HEIGHT, WSCALE
from pages.hud import Hud
from gameObjects.ship import Ship


class Game(PageBase):
    
    def __init__(self, timed_list:TimedList, game_controller:GameStateController):
        
        self._game_controller = game_controller
        self._hud = Hud(game_controller.game_level, game_controller.ship_rocket_count, game_controller.ship_level, game_controller.ship_upgrade_perk_collected)
        self._timed_list = timed_list
        
        self.VELOCITY_ITERATIONS = 10
        self.POSITION_ITERATIONS = 10
        

        self._number_of_asteroid_spawned = 0
      
        self._camera = Camera(SHAKE_DURATION, SHAKE_INTENSITY, SHAKE_FREQUENCY)
        self._world = Box2D.b2World((0, 0), doSleep=True)
        self._world.contactFilter = CollisionFilter()
        self._world.contactListener = ContactListener()
        
        self._create_world_boundary()
        self._spawn_strategy = SpawnStrategy(self._spawn_asteroid, self._spawn_rocket_perk, self._spawn_upgrade_perk)
        
        
        
        
   
        self._ship = Ship(self._world, self._camera, self._register_projectile, self._register_ship_asteroid_collision, game_controller.report_projectile_fired, self._game_controller.ship_level, False)
  
        self._projectile_list = [ObjectBase]
        self._asteroid_list = [ObjectBase]
        self._particle_list = [ObjectBase]
        self._perks_list = [ObjectBase]
        
        pygame.time.set_timer(EventConfig.time_timer, 1000)
        
        self.background_stars = WorldStar()
        self._update_reticle()
        self._perk_delay = Delay()
       
        self._penalty_strategy = PenaltyStrategy(self._hud)
        
        self.page_index:int = None
        
        
        
        # activity = self._controller.set_bonus_time(ControllerParameter.get_bonus_time(self._controller.previous_level_time))
        # self._timed_list.register_item(activity)

        
    def _create_world_boundary(self):
        
        width = WIDTH / WSCALE
        height = HEIGHT / WSCALE
        offset = 50
        
        self._world.CreateStaticBody(
            position = (0, 0),
            shapes=Box2D.b2ChainShape(
               
                vertices=[
                    (0 - offset,0-offset),
                    (width + offset, 0-offset),
                    (width + offset, height + offset),
                    (0 - offset, height + offset)
                ]
            )
            
        )
      
    
        
    def _register_projectile(self, projectile:Cannon | Rocket):
        self._projectile_list.append(projectile)
        
    def _register_ship_asteroid_collision(self, penalty):
        pygame.event.post(pygame.event.Event(SHAKE_EVENT))
        self._create_spark(self._ship.position)
        self._penalty_strategy.penalise_collision(penalty)
     
        
    def _update_projectiles(self):
        for projectile in self._projectile_list:
            
            if projectile.is_out_of_screen():
                projectile.dispose()
            
            if projectile.alive == False:
                continue
            
            projectile.update()
            if isinstance(projectile, Rocket):
                rocket = projectile
                if rocket.has_target == False:
                    target = get_target_within_range(rocket._position, self._asteroid_list, 100)
        
                    rocket.set_target(target)
                    
                
    def _draw_projectiles(self, screen, glow_screen):
        for projectile in self._projectile_list:
            if projectile.alive == False:
                continue
            projectile.draw(screen, glow_screen = glow_screen)
                
    def _projectile_asteroid_collision(self):
        collisionDetected = False
        
        for projectile in self._projectile_list:
            if projectile.alive == False:
                continue
           
            for asteroid in self._asteroid_list:
                if asteroid.alive == False:
                    continue
               
                if pygame.sprite.collide_mask(projectile, asteroid):
                
                    self._create_spark(projectile.position)
                    
                    projectile.dispose()
                    asteroid.take_damage()
                    
                    if asteroid.alive == False:
                        self._particle_list.append(Explosion(asteroid.position))
                        self._game_controller.report_asteroid_destroyed()
                        if asteroid.can_break_apart():
                            asteroids = asteroid.break_apart(self._game_controller.game_level, debug_draw = False)
                            for a in asteroids:
                                self._asteroid_list.append(a)
                       
                        asteroid.dispose()
                        collisionDetected = True
                        break
            if collisionDetected == True:
                break;
            
        
                    
    def _collect_perk(self, perk):
        if perk.perk_type == PerkType.upgrade:
                
            activity = self._game_controller.report_upgrade_perk_collected()
            self._timed_list.register_item(activity)
        
        if perk.perk_type == PerkType.rocket:
            activity = self._game_controller.report_rocket_perk_collected()
            self._timed_list.register_item(activity)
            
        SoundController.game_effect_channel().play(SoundController.perk_collected_sound)
            
        perk.dispose()
              
                   
    def _ship_perks_collision(self):
        for perk in self._perks_list:
            if perk.alive == False:
                continue
            
            attraction_distance = 100
            if perk.target == None and v_mag(perk.position - self._ship.position) < attraction_distance:
                perk.set_target(self._ship)
               
            if pygame.sprite.collide_mask(perk, self._ship):
            
                self._collect_perk(perk)
                
                self._create_spark(perk.position, quantity=10, particle_size=1.5, max_perimeter = 65)
                break;
            
    def _handle_level_completed_case(self):
        if self._is_level_completed:
            for perk in self._perks_list:
                if perk.alive == False:
                    continue
                
                self._collect_perk(perk)
                
         
                
                  
            
    def _filter_items(self):   
        self._asteroid_list = [ast for ast in self._asteroid_list if ast.alive == True]
        self._projectile_list = [p for p in self._projectile_list if p.alive == True]
        self._particle_list = [p for p in self._particle_list if p.alive == True]
        self._perks_list = [p for p in self._perks_list if p.alive == True]
           
        
    def _spawn_asteroid(self):
        self._game_controller.report_asteroid_spawned()
        asteroid = Asteroid(self._world, self._game_controller.game_level, self._camera, debug_draw=True)
        self._asteroid_list.append(asteroid)
    
    
    def _spawn_rocket_perk(self):
        spawn_position = (50 + random.random() * (WIDTH - 100), 50 + random.random() * (HEIGHT - 100))
        perk = Perk.rocket(spawn_position, self._camera)
        self._perks_list.append(perk)
        self._game_controller.report_rocket_perk_spawned()
        
        
    def _spawn_upgrade_perk(self):
        spawn_position = (50 + random.random() * (WIDTH - 100), 50 + random.random() * (HEIGHT - 100))
        perk = Perk.upgrade(spawn_position, self._camera)
        self._perks_list.append(perk)
        self._game_controller.report_upgrade_perk_spawned()
                
        
    def _create_spark(self, position, quantity:int = 5, start_perimeter:int = 6, max_perimeter:int = 60, particle_size:float = 1):
        sparks = Sparks.create_random(position, quantity, start_perimeter, max_perimeter, particle_size)
        self._particle_list.append(sparks)
    
        
    def _update_asteroids(self):
        for asteroid in self._asteroid_list:
            if asteroid.alive:
                asteroid.update()
                
            
    def _draw_asteroids(self, screen):
        for asteroid in self._asteroid_list:
            if asteroid.alive:
                asteroid.draw(screen)
                
    def _update_perks(self):
        for perk in self._perks_list:
            if perk.alive:
                perk.update()
                
            
    def _draw_perks(self, screen):
        for perk in self._perks_list:
            if perk.alive:
                perk.draw(screen)
                
                
    def _update_particles(self):
        for particle in self._particle_list:
            if particle.alive:
                particle.update()
                
            
    def _draw_particles(self, screen):
        for particle in self._particle_list:
            if particle.alive:
                particle.draw(screen)
                
            
    def _update_reticle(self):
        
        reticle_arm_lenght = 100
        reticle_position = self._ship.position + self._ship.direction * reticle_arm_lenght
        reticle_angle =  -math.degrees(v_to_angle(self._ship.direction)) - 90
        self._hud.reticle.update(reticle_position, reticle_angle)
    
    def _draw_reticle(self, screen):
        self._hud.reticle.draw(screen)
        
    @property
    def _can_spawn_asteroid(self):
       return len(self._asteroid_list) < ControllerConfig.max_asteroid_on_screen and not self._game_controller.asteroid_spawn_complete 
   
    @property
    def _is_level_completed(self):
        return self._game_controller.asteroid_spawn_complete and len(self._asteroid_list) <= 0
        
    def toggle_pause_state(self):
        if self._game_controller.game_paused == False:
            self._game_controller.game_paused = True
            self.page_index = G_Router.push(PauseScreen(self._game_controller))
        else:
            self._game_controller.game_paused = False 
            G_Router.pop(self.page_index)
            
    def _set_level_in_progress(self):
        self._game_controller.set_level_in_progress(True)
        
    # def _draw_pause_screen(self, screen):
    #     if self._controller.game_paused:
    #         if self._pause_screen == None:
    #             self._pause_screen = PauseScreen(self._controller)
    #         self._pause_screen.draw(screen)
    #     else:
    #         self._pause_screen = None
            
 
            
            
            
    def update(self, game_paused):
    
        if self._game_controller.level_is_in_progress_and_game_not_paused:
            
            self._world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
            self._projectile_asteroid_collision()
            self._ship_perks_collision()
            self._ship.update(self._game_controller.ship_level)
            self._update_projectiles()
            self._update_asteroids()
            self._update_particles()
            self._hud.update()
            self._update_reticle()
            self._update_perks()
            self._spawn_strategy.update(self._game_controller.level_time, self._can_spawn_asteroid, self._game_controller.game_level)
            self._penalty_strategy.update(not self._ship.in_boundary)
            self._timed_list.update()
            
      
           
        self._game_controller.update(self._is_level_completed)
        self._handle_level_completed_case()
        self._filter_items()
       
        
      
        
    def draw(self, screen, glow_screen):
        self._hud.draw(screen, self._game_controller.level_time,
                       self._game_controller.ship_rocket_count, self._game_controller.ship_level,
                       self._game_controller.ship_upgrade_perk_collected,
                       self._game_controller.game_paused,
                       self._game_controller.is_time_up,  self._set_level_in_progress)
        self._draw_perks(screen)
        self._draw_projectiles(screen, glow_screen = glow_screen)
        self._draw_asteroids(screen)
        self._draw_particles(screen)
        self._draw_reticle(screen)
        self._ship.draw(screen, glow_screen = glow_screen)
        
        if self._game_controller.level_is_in_progress:
            self._timed_list.draw(screen) 
        
    def handle_event(self, event:pygame.event.Event):
        
        self._hud.handle_event(event)
        self._camera.handle_event(event)
        
        self._ship.handle_event(event, self._game_controller.key_map)
        self._game_controller.handle_event(event)
        
    def handle_event_2(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause_state()
        
        