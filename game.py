import math
import random
import numpy as np
import pygame
import Box2D
from config import EventConfig
from strategies.penaltyStrategy import PenaltyStrategy
from strategies.spawnStrategy import SpawnStrategy
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
from constant import MAX_ASTEROID_PER_LEVEL, SHAKE_DURATION, SHAKE_EVENT, SHAKE_FREQUENCY, SHAKE_INTENSITY, WIDTH, HEIGHT, WSCALE, outline_color, background_color, FPS
from pages.hud import Hud
from gameObjects.ship import Ship


class Game():
    
    def __init__(self, controller:GameStateController):
        
        self._controller = controller
        self._hud = Hud(controller)
        
        self.VELOCITY_ITERATIONS = 10
        self.POSITION_ITERATIONS = 10
        
        self.TIME_TO_RESET_PENALTY = 4000

        self._max_asteroid_per_level = MAX_ASTEROID_PER_LEVEL        
        self._number_of_asteroid_spawned = 0
      
        self._camera = Camera(SHAKE_DURATION, SHAKE_INTENSITY, SHAKE_FREQUENCY)
        self._world = Box2D.b2World((0, 0), doSleep=True)
        self._world.contactFilter = CollisionFilter()
        self._world.contactListener = ContactListener()
        
        self._create_world_boundary()
        self._spawn_strategy = SpawnStrategy(self._spawn_asteroid, self._spawn_rocket_perk, self._spawn_upgrade_perk)
        
        
        
        
        self._ship = Ship(self._world, self._camera, self._register_projectile, self._register_ship_asteroid_collision, controller.report_projectile_fired, False)
  
        self._projectile_list = []
        self._asteroid_list = []
        self._particle_list = []
        self._perks_list = []
        
        pygame.time.set_timer(EventConfig.time_timer, 1000)
        
        self.background_stars = WorldStar()
        self._update_reticle()
        self._perk_delay = Delay()
       
        self._penalty_strategy = PenaltyStrategy(self._hud)
        
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
                    
                
    def _draw_projectiles(self, screen):
        for projectile in self._projectile_list:
            if projectile.alive == False:
                continue
            projectile.draw(screen)
                
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
                        self._controller.report_asteroid_destroyed()
                        if asteroid.can_break_apart():
                            asteroidA, asteroidB = asteroid.break_apart(debugDraw=False)
                            self._asteroid_list.append(asteroidA)
                            self._asteroid_list.append(asteroidB)
                        asteroid.dispose()
                        collisionDetected = True
                        break
            if collisionDetected == True:
                break;
              
                   
    def _ship_perks_collision(self):
        for perk in self._perks_list:
            if perk.alive == False:
                continue
            
            attraction_distance = 100
            if perk.target == None and v_mag(perk.position - self._ship.position) < attraction_distance:
                perk.set_target(self._ship)
               
            if pygame.sprite.collide_mask(perk, self._ship):
            
                if perk.perk_type == PerkType.upgrade:
                    # perks_collected, perks_completed = self._controller.report_rocket_perk_collected()
                    # self._hud.update_upgrade_perk_bar(self._controller.report_upgrade_perk_collected())
                    activity = self._controller.report_upgrade_perk_collected()
                    self._hud.register_activity(activity)
                
                if perk.perk_type == PerkType.rocket:
                    # self._hud.update_rocket_count(self._controller.report_rocket_perk_collected())
                    activity = self._controller.report_rocket_perk_collected()
                    self._hud.register_activity(activity)
                
                
                
                self._create_spark(perk.position, quantity=10, particle_size=1.5, max_perimeter = 65)
                perk.dispose()
                break;
            
            
    def _filter_items(self):   
        self._asteroid_list = [ast for ast in self._asteroid_list if ast.alive == True]
        self._projectile_list = [p for p in self._projectile_list if p.alive == True]
        self._particle_list = [p for p in self._particle_list if p.alive == True]
        self._perks_list = [p for p in self._perks_list if p.alive == True]
           
        
    def _spawn_asteroid(self):
        self._controller.report_asteroid_spawned()
        asteroid = Asteroid(self._world, self._camera, debug_draw=False)
        self._asteroid_list.append(asteroid)
    
    
    def _spawn_rocket_perk(self):
        spawn_position = (50 + random.random() * (WIDTH - 100), 50 + random.random() * (HEIGHT - 100))
        perk = Perk.rocket(spawn_position, self._camera)
        self._perks_list.append(perk)
        self._controller.report_rocket_perk_spawned()
        
        
    def _spawn_upgrade_perk(self):
        spawn_position = (50 + random.random() * (WIDTH - 100), 50 + random.random() * (HEIGHT - 100))
        perk = Perk.upgrade(spawn_position, self._camera)
        self._perks_list.append(perk)
        self._controller.report_upgrade_perk_spawned()
                
        
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
        
   
        
            
    def update_and_draw(self, screen):
        asteroids_alive = len(self._asteroid_list)
        if self._controller.level_is_in_progress_and_game_not_paused:
            
            self._world.Step(1.0/60, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
            self._projectile_asteroid_collision()
            self._ship_perks_collision()
            self._ship.update()
            self._update_projectiles()
            self._update_asteroids()
            self._update_particles()
            self._hud.update()
            self._update_reticle()
            self._update_perks()
            self._spawn_strategy.update(self._controller.level_time, self._controller.level, asteroids_alive)
            self._penalty_strategy.update(not self._ship.in_boundary)
            
            
        self._filter_items()
        self._hud.draw(screen)
        self._draw_perks(screen)
        self._draw_projectiles(screen)
        self._draw_asteroids(screen)
        self._draw_particles(screen)
        self._draw_reticle(screen)
        self._ship.draw(screen)
        self._hud.draw_pause_screen(screen)
        
        self._controller.update(asteroids_alive)
        
    def handle_events(self, event:pygame.event.Event):
        
        self._hud.handle_event(event)
        self._camera.handle_event(event)
        
        self._ship.handle_event(event, self._controller.key_map)
        self._controller.handle_event(event)
        
        