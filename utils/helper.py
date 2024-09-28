

from collections import namedtuple
import math

import numpy as np


def toComponent(angle):
    return np.array([
        math.cos(angle),
        math.sin(angle),
    ])
    
    
def mapValue(minVar, maxVar, minDest, maxDest, var):
    return ((var - minVar) / (maxVar - minVar) * (maxDest - minDest)) + minDest


def toWorldPos(position, scale:float, screenHeight):
        return np.array([position[0] / scale, (screenHeight - position[1]) / scale])


def toPixelPos(position:tuple, scale:float, screenHeight):
    return np.array([position[0] * scale, screenHeight - (position[1] * scale)])

def WHToPixel(w, h, scale):
    return np.array([w * scale * 2, h * scale * 2])

def WHToWorld(w, h, scale):
    return np.array([w / scale / 2, h / scale / 2])
