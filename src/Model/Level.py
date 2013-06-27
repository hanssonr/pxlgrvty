"""
http://qq.readthedocs.org/en/latest/tiles.html#map-definition
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tile import *
import ConfigParser, Box2D.b2
from Box2D.Box2D import b2Vec2
from Camera import *

class Level(object):
    
    __mMaxLevels = 3 #read out from all the .lvl files later
    mCurrentLevel = 1
    mTiles = []
    mMap = None
    mWidth = None
    mHeight = None
    mStartPos = None
    mPickups = None
    
    def __init__(self, world):
        self.mWorld = world
        self.__loadLevel()
        
    def __loadLevel(self):
        self.__readLevel()
        self.__createWorldCollision()
    
    def __readLevel(self):
        parser = ConfigParser.ConfigParser()
        parser.read("Assets/Levels/level%d.lvl" % self.mCurrentLevel)
        self.mMap = parser.get("level", "map").replace(" ", "").split("\n")
        self.mPickups = parser.get("objects", "pickups") #TODO: use json or similar to extract info about enemies/pickup objects to the level
        self.mMap.reverse() #box2d have inverted y-axis
        """
        for section in parser.sections():
            if len(section) == 1:
                print "True"
                desc = dict(parser.items(section))
                print desc
                self.key[section] = desc
        """        
        self.width = len(self.mMap[0])
        self.height = len(self.mMap)
        
    
    def __createWorldCollision(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.mMap[y][x] == "#":
                    Tile(self.mWorld, b2Vec2(x, y), TileType.WALL)
                elif self.mMap[y][x] == "S":
                    self.mStartPos = (x, y)
    
    def nextLevel(self):
        if self.mCurrentLevel < self.__mMaxLevels:
            self.mCurrentLevel += 1
            self.__loadLevel(self)
    
    def getTile(self, x, y):
        pass
            
              
    def isCorner(self, pos):
        pass
    
    def isTop(self, pos):
        pass