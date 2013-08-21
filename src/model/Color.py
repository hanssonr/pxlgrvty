"""
Color enumclass for reading out things from pixelcolordata

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

class Color(object):
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    
    #tilecolortypes
    STARTPOS = (0,255,0)
    ENDPOS = (255,0,0)
    BOX = (87,23,24)
    WALL = (0,0,0)