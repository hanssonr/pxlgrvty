"""
A Filterclass for handling collisionfiltering with box2d

Author: Rickard Hansson, rkh.hansson@gmail.com
"""
class Filter(object):
    
    CATEGORY_FX = 0x0001
    CATEGORY_WALLS = 0x0002
    
    MASK_FX = CATEGORY_WALLS
    MASK_WALLS = CATEGORY_FX