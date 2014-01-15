"""
Enumclass for different type of directiondata

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

class GravityDirection(object):
    UP, RIGHT, DOWN, LEFT = range(4)  
 
class MoveDirection(object):
    UP, RIGHT, DOWN, LEFT = range(1, 5)

class Direction(object):
    UP = -1
    RIGHT = 1
    DOWN = 1
    LEFT = -1

class Facing(object):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    
    @staticmethod
    def convertFromVector2(vec):
        if vec.x > 0:
            return Facing.RIGHT
        if vec.x < 0:
            return Facing.LEFT
        if vec.y > 0:
            return Facing.DOWN
        if vec.y < 0:
            return Facing.UP
    
    
    
    