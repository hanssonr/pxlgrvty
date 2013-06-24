"""
http://qq.readthedocs.org/en/latest/tiles.html#map-definition
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tile import Tile
import ConfigParser, Box2D.b2
from Box2D.Box2D import b2Vec2

class Level(object):
    
    __mMaxLevels = 3 #read out from all the .lvl files later
    mCurrentLevel = 1
    mTiles = []
    mMap = None
    mWidth = None
    mHeight = None
    
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
        for y, row in enumerate(self.mMap):
            for x, column in enumerate(row):
                if self.mMap[y][x] == "#":
                    Tile(self.mWorld, b2Vec2(x,19-y), "#")
    
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