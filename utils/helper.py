

from collections import namedtuple
import math


# def toComponent(angle):
#     return namedtuple('toComponent', ['x', 'y'])(
#         x=math.cos(angle),
#         y=math.sin(angle)
#     )
def mapValue(minVar, maxVar, minDest, maxDest, var):
    return ((var - minVar) / (maxVar - minVar) * (maxDest - minDest)) + minDest


def toWorldPos(position:tuple, scale:float, screenHeight):
        return position[0] / scale, (screenHeight - position[1]) / scale


def toPixelPos(position:tuple, scale:float, screenHeight):
    return (position[0] * scale, screenHeight - (position[1] * scale))

def WHToPixel(w, h, scale):
    return w * scale * 2, h * scale * 2

def WHToWorld(w, h, scale):
    return w / scale / 2, h / scale / 2
