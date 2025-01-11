
# from PIL import Image, ImageFilter, ImageEnhance, ImageChops


import json
import math
import os
import sys
import Box2D
# from packages.cryptography import  cryptography
import numpy as np
import pygame

from config.GlobalConfig import GlobalConfig
from strategies.encryptionStrategy import EncryptionStrategy
from utils.colors import Colors
from customEnum import ShipActions


class Helper():
    def __init__(self):
        pass
        
        
    def resource_path():
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return base_path
    
    @staticmethod
    def invert_y_axis(vec):
        return np.array((vec[0], -vec[1]))
    
    @staticmethod
    def convert_pixel_frame_to_meters_second(val):
        return (val * GlobalConfig.fps) / GlobalConfig.world_scale
    
    @staticmethod
    def convert_meters_second_to_pixel_frame(val):
        return (val * GlobalConfig.world_scale) / GlobalConfig.fps
    
    # @staticmethod
    # def add_glow5(surface:pygame.surface.Surface, intensity:int = 5, radius:float = 5):

    #     img_str = pygame.image.tostring(surface, "RGBA", False)
    #     image = Image.frombytes('RGBA', surface.get_size(), img_str)
    #     # Load the image with transparency
    #     # image = Image.open(input_image).convert("RGBA")

    #     # Increase the canvas size to accommodate the glow
    #     border_size = 20  # Adjust as needed for more glow
    #     new_size = (image.width + 2 * border_size, image.height + 2 * border_size)
    #     glow_base = Image.new("RGBA", new_size, (0, 0, 0, 0))
    #     glow_base.paste(image, (border_size, border_size))

    #     # Extract the alpha channel
    #     alpha = glow_base.getchannel("A")

    #     # Create a mask for the edges (outer edges only)
    #     # Dilate the alpha to grow outward
    #     dilated = alpha.filter(ImageFilter.MaxFilter(intensity))  # Slight expansion
    #     # Subtract the original alpha from the dilated one to isolate edges
    #     edges = ImageChops.subtract(dilated, alpha)

    #     # Apply a Gaussian blur to the edges to create the glow
    #     glow = edges.filter(ImageFilter.GaussianBlur(radius=radius))

    #     # Add color to the glow (e.g., a soft white glow)
    #     colored_glow = Image.new("RGBA", new_size, (255, 255, 255, 0))
    #     colored_glow.putalpha(glow)

    #     # Combine the glow with the original image
    #     final_image = Image.alpha_composite(glow_base, colored_glow)
        
    #     final_image = final_image.tobytes()
    #     return pygame.image.fromstring(final_image, new_size, 'RGBA')

    
    
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
    def save_data(file_name, data:dict, key = None):
        
        if key != None:
            data = EncryptionStrategy.encrypt_json(data, key)
        else:
            data = json.dumps(data)
            
        with open(file_name, 'w') as file:
            file.write(data)
            # json.dump(data, file)
        
    @staticmethod
    def load_data(file_name, key = None):
        try:
            with open(file_name, 'r') as file:
                data = file.read()
               
            if key != None:
                return EncryptionStrategy.decrypt_json(data, key)
            else:
                return json.loads(data)
                # return json.load(file)
                # return {ShipActions(int(i)) : value for i, value in serialized_key_map.items()}
        except FileNotFoundError:
            print('file not found')
            return None
            print('other errors')
        except :
            return None
        # except Fernet.InvalidToken:
        #     return None
        
    # @staticmethod
    # def log_level(value):
    #     return math.log(value)
    
    
    @staticmethod
    def asymptotic_value(min_value, max_value, rate, time):
        return max_value - (max_value - min_value) * math.exp(-rate * time)


    @staticmethod
    def cap_box2D_body_speed(body:Box2D.b2Body, max_speed):
        velocity = body.linearVelocity
        velocity_magnitude = velocity.length
        
        if velocity_magnitude > max_speed:
            velocity.Normalize()
            velocity *= max_speed
            
        body.linearVelocity = velocity
            
    @staticmethod
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

    @staticmethod
    def calculate_interception_vector(target_speed, target_velocity, target_position, source_position, source_speed):
        
        target_source_distance = source_position - target_position
        d = np.linalg.norm(target_source_distance)
        
        a = np.square(source_speed) - np.square(target_speed)
        b = 2 * np.dot(target_source_distance, target_velocity)
        c = - np.square(d)
        
        if a == 0:
            # target speed and bullet speed are thesame
            # a quadratic equation is not possible because their
            # can be only one solution in this case
            t = -c / b
            # time can't be negative
            if t <= 0:
                
                print('negative time')
                return
        else:
            b_squar_4ac = np.square(b) - 4 * a * c
        
            if (b_squar_4ac) < 0:
                # no sulution
                print('no solution')
                return
            
            root_b_square_4ac =  math.sqrt(b_squar_4ac)
            two_a = 2 * a
                    
            # their are always two solutions
            t1 = - (b + root_b_square_4ac) / two_a
            t2 = - (b - root_b_square_4ac) / two_a
           
            if (t1 <=  0 and t2 <= 0):
                print('negative time')
                # no solution
                return
            # always choose the smallest non negative t
            if t1 < 0:
                t = t2
            elif t2 < 0:
                t = t1
            else:
                t = min(t1, t2)
            
        intersept_point = target_position + target_velocity * t
        source_velocity = (intersept_point - source_position) / t
        return source_velocity
        


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

def v_normalize(vec:tuple):
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


def to_box2D_coordinate(position, scale:float, screenHeight):
    return Box2D.b2Vec2([position[0] / scale, (screenHeight - position[1]) / scale])


def to_pixel_coordinate(position:tuple, scale:float, screenHeight):
    return Box2D.b2Vec2([position[0] * scale, screenHeight - (position[1] * scale)])

def WHToPixel(w, h, scale):
    return Box2D.b2Vec2([w * scale * 2, h * scale * 2])

def WHToWorld(w, h, scale):
    return Box2D.b2Vec2([w / scale / 2, h / scale / 2])

def debug_draw_box2D_bodies(screen:pygame.Surface, box2D_bodies_debug_list:list):
    for box2D_body in box2D_bodies_debug_list:
        for fixture in box2D_body.fixtures:
            shape = fixture.shape
            
            position = to_pixel_coordinate(box2D_body.position, GlobalConfig.world_scale, GlobalConfig.height)
            if isinstance(shape, Box2D.b2CircleShape):
                radius = shape.radius * GlobalConfig.world_scale
                pygame.draw.circle(screen, Colors.debug_color, position, radius)
                
                line_end = position[0] + math.cos(box2D_body.angle - math.pi) * radius,\
                            position[1] - math.sin(box2D_body.angle - math.pi) * radius
                            
                pygame.draw.line(screen, Colors.drawing_color, position, line_end, 2)
            
            elif isinstance(shape, Box2D.b2PolygonShape):
                coordPoints = [(box2D_body.transform * v) for v in shape.vertices]
                coordPoints = [to_pixel_coordinate(v, GlobalConfig.world_scale, GlobalConfig.height) for v in coordPoints ]
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
        body.position = ((GlobalConfig.width - buffer) / GlobalConfig.world_scale + (bodyWidth ) / 2, position.y)
    elif left > GlobalConfig.width/GlobalConfig.world_scale:
        body.position = ((-bodyWidth + buffer)/ 2, position.y)
    
    if top < 0:
        body.position = (position.x, (GlobalConfig.height - buffer) / GlobalConfig.world_scale + (bodyHeight) / 2)
    elif bottom > GlobalConfig.height / GlobalConfig.world_scale:
        body.position = (position.x, (-bodyHeight + buffer) / 2)
            
            
def check_box2D_object_in_bounds(body:Box2D.b2Body):
    left, top, right, bottom = get_body_bounds(body)
    
    if right < 0 or left > GlobalConfig.width/GlobalConfig.world_scale or top < 0 or bottom > GlobalConfig.height / GlobalConfig.world_scale:
        return False

    return True
    

    

            

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                

    # @staticmethod
    # def draw_with_glow(screen:pygame.surface.Surface, blur_screen:pygame.surface.Surface, item:pygame.surface.Surface, pos:tuple = (0, 0)):
    #     aux_scale = .3
    #     aux_dimension = int(GlobalConfig.width * aux_scale), int(GlobalConfig.height * aux_scale)
    #     blur_screen.blit(item, pos)
    #     resized = pygame.transform.scale(blur_screen, aux_dimension)
    #     img_str = pygame.image.tostring(resized, "RGB", False)
    #     im1 = Image.frombytes('RGB', aux_dimension, img_str)
        
    #     im1 = im1.filter(ImageFilter.GaussianBlur(6))
        
    #     im1 = im1.tobytes()
    #     pil_blured = pygame.image.fromstring(im1, aux_dimension, "RGB")
    #     # pil_blured = pygame.image.fromstring(im1, (230, 110), "RGB")
    #     final = pygame.transform.scale(pil_blured, (GlobalConfig.width, GlobalConfig.height))
        
    #     screen.blit(blur_screen, (0, 0))
    #     screen.blit(final, (0,0), special_flags = pygame.BLEND_RGBA_ADD)
        
    # @staticmethod
    # def draw_with_glow_2(screen:pygame.surface.Surface, surface:pygame.surface.Surface, pos:tuple, glow_color:tuple, blur_radius:int):
       
    #     glow_surface = surface.copy()
    #     # glow_surface.fill((255, 255, 255))
    #     # pygame.draw.circle(glow_surface, glow_color, (surface.get_width() // 2, surface.get_height() // 2), 50)
        
    #     glow_array = pygame.surfarray.array3d(glow_surface)
    #     # glow_array = pygame.image.tostring(glow_surface, "RGB", False)
    #     print(glow_array)
    #     cv2.GaussianBlur(glow_array, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=glow_array)
    #     # cv2.blur(glow_array, ksize=(5, 5), dst=glow_array)
    #     # glow_array = cv2.GaussianBlur(glow_array, (0, 0), blur_radius)
    #     glow_surface = pygame.surfarray.make_surface(glow_array)
        
    #     screen.blit(surface, pos)
    #     screen.blit(glow_surface, pos, special_flags = pygame.BLEND_ADD)
            
        
        
        
        
        
            
    # @staticmethod   
    # def simple_blur(surface, blur_radius=5):
    #     """Apply a simple box blur to a surface"""
    #     target = surface.copy()
    #     size = surface.get_size()
        
    #     surf_array = pygame.surfarray.pixels3d(target)
    #     for x in range(blur_radius, size[0] - blur_radius):
    #         for y in range(blur_radius, size[1] - blur_radius):
    #             # Average the surrounding pixels
    #             for c in range(3):  # For each color channel
    #                 total = 0
    #                 for dx in range(-blur_radius, blur_radius + 1):
    #                     for dy in range(-blur_radius, blur_radius + 1):
    #                         total += surf_array[x + dx, y + dy, c]
    #                 surf_array[x, y, c] = total // ((blur_radius * 2 + 1) ** 2)
        
    #     del surf_array
    #     return target

    # @staticmethod
    # def create_bloom(surface, blur_passes=3, blur_radius=3, intensity=2.0):
    #     """Create a bloom effect by blurring multiple times"""
    #     bloom = surface.copy()
        
    #     # Apply multiple passes of blur
    #     for _ in range(blur_passes):
    #         bloom = Helper.simple_blur(bloom, blur_radius)
        
    #     # Increase the brightness
    #     bloom_array = pygame.surfarray.pixels3d(bloom)
    #     bloom_array[:] = np.minimum(bloom_array * intensity, 255)
    #     del bloom_array
        
    #     return bloom
            
        
        
        
        
    # @staticmethod
    # def create_bloom_surface(surface, intensity=3.0, threshold=50, blur_size=31, sigma=10):
    #     """
    #     Creates a bloom effect from the given surface with enhanced parameters.
        
    #     Args:
    #         surface: The pygame surface to apply bloom to
    #         intensity: Bloom intensity (default: 2.0)
    #         threshold: Brightness threshold for bloom (default: 50)
    #         blur_size: Size of the blur kernel (default: 31)
    #         sigma: Gaussian blur sigma (default: 10)
        
    #     Returns:
    #         A new surface with the bloom effect applied
    #     """
    #     surf_array = pygame.surfarray.array3d(surface)
    #     grayscale = np.mean(surf_array, axis=2)
    #     bright_mask = grayscale > threshold
        
    #     bloom_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    #     bloom_array = pygame.surfarray.pixels3d(bloom_surf)
        
    #     x, y = np.meshgrid(np.linspace(-blur_size, blur_size, 2*blur_size+1),
    #                     np.linspace(-blur_size, blur_size, 2*blur_size+1))
    #     gaussian = np.exp(-(x**2 + y**2)/(2*sigma**2))
    #     gaussian = gaussian / gaussian.sum()
        
    #     for i in range(3):
    #         channel = surf_array[:,:,i] * bright_mask
    #         blurred = np.zeros_like(channel)
            
    #         for x in range(blur_size, channel.shape[0]-blur_size):
    #             for y in range(blur_size, channel.shape[1]-blur_size):
    #                 if bright_mask[x,y]:
    #                     window = channel[x-blur_size:x+blur_size+1,
    #                                 y-blur_size:y+blur_size+1]
    #                     blurred[x,y] = np.sum(window * gaussian)
            
    #         bloom_array[:,:,i] = blurred * intensity
        
    #     del bloom_array
    #     del surf_array
        
    #     return bloom_surf
        
        
    # @staticmethod
    # def create_bloom_surface(surface, intensity=1.0, threshold=128):
    #     """
    #     Creates a bloom effect from the given surface.
        
    #     Args:
    #         surface: The pygame surface to apply bloom to
    #         intensity: Bloom intensity (default: 1.0)
    #         threshold: Brightness threshold for bloom (default: 128)
        
    #     Returns:
    #         A new surface with the bloom effect applied
    #     """
    #     # Convert surface to array for manipulation
    #     surf_array = pygame.surfarray.array3d(surface)
        
    #     # Create grayscale version to determine brightness
    #     grayscale = np.mean(surf_array, axis=2)
        
    #     # Create mask for bright pixels
    #     bright_mask = grayscale > threshold
        
    #     # Create bloom surface
    #     bloom_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    #     bloom_array = pygame.surfarray.pixels3d(bloom_surf)

        
    #     # Apply gaussian blur to bright areas
    #     blur_size = 15
    #     sigma = 5
        
    #     # Create gaussian kernel
    #     x, y = np.meshgrid(np.linspace(-blur_size, blur_size, 2*blur_size+1),
    #                     np.linspace(-blur_size, blur_size, 2*blur_size+1))
    #     gaussian = np.exp(-(x**2 + y**2)/(2*sigma**2))
    #     gaussian = gaussian / gaussian.sum()
        
    #     # Apply blur to each color channel
    #     for i in range(3):
    #         channel = surf_array[:,:,i] * bright_mask
    #         blurred = np.zeros_like(channel)
            
    #         # Convolve with gaussian kernel
    #         for x in range(blur_size, channel.shape[0]-blur_size):
    #             for y in range(blur_size, channel.shape[1]-blur_size):
    #                 if bright_mask[x,y]:
    #                     window = channel[x-blur_size:x+blur_size+1,
    #                                 y-blur_size:y+blur_size+1]
    #                     blurred[x,y] = np.sum(window * gaussian)
            
    #         # surfarray.pixels3d(bloom_surf)[:,:,i] = blurred * intensity
    #         bloom_array[:,:,i] = blurred * intensity
            
    #     del bloom_array
    #     del surf_array
        
    #     return bloom_surf
            
    # @staticmethod
    # def apply_bloom(surface, bloom_surface):
    #     """
    #     Combines the original surface with its bloom effect.
        
    #     Args:
    #         surface: Original surface
    #         bloom_surface: Pre-computed bloom surface
        
    #     Returns:
    #         New surface with bloom effect applied
    #     """
    #     result = surface.copy()
    #     result.blit(bloom_surface, (0,0), special_flags=pygame.BLEND_RGB_ADD)
    #     return result
            
            
        
            
            
 