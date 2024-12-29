
import os

from utils.helper import Helper


class RocketConfig():
    image_path = os.path.join(Helper.resource_path(), 'images', 'rocket.png')
    flare_path = os.path.join(Helper.resource_path(), 'images', 'flare109.png')
    smoke_path = os.path.join(Helper.resource_path(), 'images', 'smoke.png')
    
 
    speed = 4
    turn_rate_degrees = 4
    
    # in seconds
    rocket_life = 5