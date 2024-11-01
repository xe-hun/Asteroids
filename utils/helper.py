

from collections import namedtuple
import json
import math
import Box2D
import numpy as np
import pygame

from config import Colors, ControllerConfig, GlobalConfig
from constant import HEIGHT, SHAKE_EVENT, WIDTH, WSCALE
from customEnum import ShipActions


class Helper():
    def __init__(self):
        pass
    
    @staticmethod
    def cap_box2D_body_speed(body:Box2D.b2Body, max_speed):
        velocity = body.linearVelocity
        velocity_magnitude = velocity.length
        
        if velocity_magnitude > max_speed:
            velocity.Normalize()
            velocity *= max_speed
            
        body.linearVelocity = velocity
           
    
     
    @staticmethod
    def save_key_map(file_name, key_map):
        serialized_key_map = {key.value: value for key, value in key_map.items()}
        with open(file_name, 'w') as file:
            json.dump(serialized_key_map, file)
            
    @staticmethod
    def load_key_map(file_name):
        try:
            with open(file_name, 'r') as file:
                serialized_key_map = json.load(file)
                return {ShipActions(int(i)) : value for i, value in serialized_key_map.items()}
        except FileNotFoundError:
            print('file not found')
            return None
        
        
    @staticmethod
    def log_level(value):
        return math.log(value)
    
    
    @staticmethod
    def asymptotic_value(min_value, max_value, rate, time):
        return max_value - (max_value - min_value) * math.exp(-rate * time)


def scale(surface: pygame.Surface, factor):
    if factor == 1:
        return surface
    else:
        width, height = surface.get_width() * factor, surface.get_height() * factor
        return pygame.transform.scale(surface, (int(width), int(height)))


def v_mag(vec:tuple):
    if vec[0] == 0 and vec[1] == 0:
        return 0
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

def v_to_angle(vec:tuple):
    return math.atan2(vec[1], vec[0])


def v_perpendicular(vec:tuple):
    return np.array((vec[1], -vec[0]))

def v_norm(vec:tuple):
    magnitude = v_mag(vec)
    if magnitude == 0:
        return np.array((0, 0))
    return np.array((vec[0] / magnitude, vec[1] / magnitude))

def v_dot(vec1:tuple, vec2:tuple):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def v_angle_diff(vec1:tuple, vec2:tuple):
    magnitude1 = v_mag(vec1)
    magnitude2 = v_mag(vec2)
    
    if magnitude1 * magnitude2 == 0:
        return 0
    
    cosAngle = v_dot(vec1, vec2) / (magnitude1 * magnitude2)
    
    cosAngle = clamp(-1, 1, cosAngle)
    
    angle = math.acos(cosAngle)
    return angle

def v_rotate(vec:tuple, rate:tuple):
    x = vec[0]
    y = vec[1]
    return np.array(
        (x * math.cos(rate) - y * math.sin(rate),
        x * math.sin(rate) + y * math.cos(rate),)
    )

def v_to_component(angle:float):
    return Box2D.b2Vec2(
        math.cos(angle),
        math.sin(angle),
    )
    
def clamp(minVal, maxVal, val):
    return (min(maxVal, max(minVal, val)))
    
def map_value(minVar, maxVar, minDest, maxDest, var):
    return ((var - minVar) / (maxVar - minVar) * (maxDest - minDest)) + minDest


def to_box2D_position(position, scale:float, screenHeight):
    return Box2D.b2Vec2([position[0] / scale, (screenHeight - position[1]) / scale])


def to_pixel_position(position:tuple, scale:float, screenHeight):
    return Box2D.b2Vec2([position[0] * scale, screenHeight - (position[1] * scale)])

def WHToPixel(w, h, scale):
    return Box2D.b2Vec2([w * scale * 2, h * scale * 2])

def WHToWorld(w, h, scale):
    return Box2D.b2Vec2([w / scale / 2, h / scale / 2])

def debug_draw_box2D_bodies(screen:pygame.Surface, box2D_bodies_debug_list:list):
    for box2D_body in box2D_bodies_debug_list:
        for fixture in box2D_body.fixtures:
            shape = fixture.shape
            
            position = to_pixel_position(box2D_body.position, GlobalConfig.world_scale, GlobalConfig.height)
            if isinstance(shape, Box2D.b2CircleShape):
                radius = shape.radius * GlobalConfig.world_scale
                pygame.draw.circle(screen, Colors.debug_color, position, radius)
                
                line_end = position[0] + math.cos(box2D_body.angle - math.pi) * radius,\
                            position[1] - math.sin(box2D_body.angle - math.pi) * radius
                            
                pygame.draw.line(screen, Colors.drawing_color, position, line_end, 2)
            
            elif isinstance(shape, Box2D.b2PolygonShape):
                coordPoints = [(box2D_body.transform * v) for v in shape.vertices]
                coordPoints = [to_pixel_position(v, GlobalConfig.world_scale, GlobalConfig.height) for v in coordPoints ]
                pygame.draw.polygon(screen, Colors.debug_color, coordPoints)
                
            elif isinstance(shape, Box2D.b2EdgeShape):
                v1 = position + shape.vertex1 * GlobalConfig.world_scale
                v2 = position + shape.vertex2 * GlobalConfig.world_scale
                pygame.draw.line(screen, Colors.debug_color, v1, v2, 2)
            
            
def get_body_bounds(body:Box2D.b2Body):
    bounds = [fixture.shape.getAABB(body.transform, 0) for fixture in body.fixtures]
    left = min(bound.lowerBound.x for bound in bounds)
    right = max(bound.upperBound.x for bound in bounds)
    top = max(bound.upperBound.y for bound in bounds)
    bottom = min(bound.lowerBound.y for bound in bounds)
    return (left, top, right, bottom)
            
def wrap_box2D_object(body:Box2D.b2Body):
        left, top, right, bottom = get_body_bounds(body)
        buffer = 10
        
        position = body.position
        bodyWidth = right - left
        bodyHeight = top - bottom
        if right < 0:
            body.position = ((WIDTH - buffer) / WSCALE + (bodyWidth ) / 2, position.y)
        elif left > WIDTH/WSCALE:
            body.position = ((-bodyWidth + buffer)/ 2, position.y)
        
        if top < 0:
            body.position = (position.x, (HEIGHT - buffer) / WSCALE + (bodyHeight) / 2)
        elif bottom > HEIGHT / WSCALE:
            body.position = (position.x, (-bodyHeight + buffer) / 2)
            
            
def check_box2D_object_in_bounds(body:Box2D.b2Body):
        left, top, right, bottom = get_body_bounds(body)
        
        if right < 0 or left > WIDTH/WSCALE or top < 0 or bottom > HEIGHT / WSCALE:
            return False

        return True
            

def get_target_within_range(object_position:tuple, target_list:list, target_range:int):
    closest_locked_distance = float('inf')
    closest_un_locked_distance = float('inf')
    
    locked_target = None
    un_locked_target = None
    
    for t in target_list:
        distance = v_mag( (t.position[0] - object_position[0],
                            t.position[1] - object_position[1]))
        if t.is_locked_on == True:
            if distance < target_range and distance < closest_un_locked_distance:
                locked_target = t
                closest_un_locked_distance = distance
        else:
            if distance < target_range and distance < closest_locked_distance:
                un_locked_target = t
                closest_locked_distance = distance
                
    return un_locked_target if un_locked_target != None else locked_target

        
    
                
        
            
            
 