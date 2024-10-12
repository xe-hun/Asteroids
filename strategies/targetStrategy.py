

from utils.helper import mag


class TargetStrategy():
    def __init__(self, objectPosition:tuple, targetPositionList:list, targetRange:int):
        shortestDistance = float('inf')
        self.target = None
        
        for targetPosition in targetPositionList:
            distance = mag( (targetPosition[0] - objectPosition[0],
                           targetPosition[1] - objectPosition[1]))
                
            if distance < targetRange and distance < shortestDistance:
                self.target = targetPosition
                shortestDistance = distance
                    
            
    def targetPosition(self):
        return self.target