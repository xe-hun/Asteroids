

from collections import namedtuple
import math


# def toComponent(angle):
#     return namedtuple('toComponent', ['x', 'y'])(
#         x=math.cos(angle),
#         y=math.sin(angle)
#     )
    
def mapValue(minVar, maxVar, minDest, maxDest, var):
    return var / (maxVar - minVar) * (maxDest - minDest) + minDest