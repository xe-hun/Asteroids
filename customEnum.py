
from enum import Enum


class ShipActions(Enum):
    Boost = 1
    Cannon = 2
    Rocket = 3
    Steer = 4
    

class Steering(Enum):
    steeringLeft = 1
    steeringRight = 2
    noSteering = 3