

from collections import namedtuple
import math
import Box2D
import pygame

from constant import HEIGHT, SHAKE_EVENT, WIDTH, WSCALE
# from utils.lerp import Lerp


def toComponent(angle):
    return Box2D.b2Vec2(
        math.cos(angle),
        math.sin(angle),
    )
    
def clamp(minVal, maxVal, val):
    return (min(maxVal, max(minVal, val)))
    
def mapValue(minVar, maxVar, minDest, maxDest, var):
    return ((var - minVar) / (maxVar - minVar) * (maxDest - minDest)) + minDest


def toWorldPos(position, scale:float, screenHeight):
    return Box2D.b2Vec2([position[0] / scale, (screenHeight - position[1]) / scale])


def toPixelPos(position:tuple, scale:float, screenHeight):
    return Box2D.b2Vec2([position[0] * scale, screenHeight - (position[1] * scale)])

def WHToPixel(w, h, scale):
    return Box2D.b2Vec2([w * scale * 2, h * scale * 2])

def WHToWorld(w, h, scale):
    return Box2D.b2Vec2([w / scale / 2, h / scale / 2])

def debugDrawBox2DBodies(screen:pygame.Surface, box2DBodiesDebugList:list):
    for box2DBody in box2DBodiesDebugList:
        for fixture in box2DBody.fixtures:
            shape = fixture.shape
            coordPoints = [(box2DBody.transform * v) for v in shape.vertices]
            coordPoints = [toPixelPos(v, WSCALE, HEIGHT) for v in coordPoints ]
            pygame.draw.polygon(screen, (50, 111, 50), coordPoints)
            
            
def getBodyBounds(ship:Box2D.b2Body):
    bounds = [fixture.shape.getAABB(ship.transform, 0) for fixture in ship.fixtures]
    left = min(bound.lowerBound.x for bound in bounds)
    right = max(bound.upperBound.x for bound in bounds)
    top = max(bound.upperBound.y for bound in bounds)
    bottom = min(bound.lowerBound.y for bound in bounds)
    return (left, top, right, bottom)
            
def warpBox2DObject(ship:Box2D.b2Body):
        left, top, right, bottom = getBodyBounds(ship)
        buffer = 10
        
        position = ship.position
        bodyWidth = right - left
        bodyHeight = top - bottom
        if right < 0:
            ship.position = ((WIDTH - buffer) / WSCALE + (bodyWidth ) / 2, position.y)
        elif left > WIDTH/WSCALE:
            ship.position = ((-bodyWidth + buffer)/ 2, position.y)
        
        if top < 0:
            ship.position = (position.x, (HEIGHT - buffer) / WSCALE + (bodyHeight) / 2)
        elif bottom > HEIGHT / WSCALE:
            ship.position = (position.x, (-bodyHeight + buffer) / 2)

        
        
                
        
            
            
 