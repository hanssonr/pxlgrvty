"""
http://qq.readthedocs.org/en/latest/tiles.html#map-definition
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tile import Tile, TileType
from Box2D import b2Vec2
import ConfigParser, json
from model.entities.Box import Box
from model.entities.Nugget import Nugget


class Level(object):
    
    __mMaxLevels = 3 #read out from all the .lvl files later
    mCurrentLevel = 1
    mTiles = []
    mMap = None
    mWidth = None
    mHeight = None
    mStartPos = None
    mPickups = None
    mObjects = []
    
    def __init__(self, world, gravity):
        self.mWorld = world
        self.mGravity = gravity
        self.__loadLevel()
        
    def __loadLevel(self):
        self.__readLevel()
        self.__createWorldCollision()
        self.__createPickups()
    
    def __readLevel(self):
        parser = ConfigParser.ConfigParser()
        parser.read("Assets/Levels/level%d.lvl" % self.mCurrentLevel)
        self.mMap = parser.get("level", "map").replace(" ", "").split("\n")
        self.mPickups = parser.get("objects", "pickups")
        self.width = len(self.mMap[0])
        self.height = len(self.mMap)
        
    
    def __createWorldCollision(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.mMap[y][x] == "#":

                    #do only necessary collisions
                    if x == 0:
                        if self.mMap[y][x+1] != "#":
                            Tile(self.mWorld, b2Vec2(x, y), TileType.WALL)
                            continue
                    elif x == self.width-1:
                        if self.mMap[y][x-1] != "#":
                            Tile(self.mWorld, b2Vec2(x, y), TileType.WALL)
                            continue
                    
                    if y == 0:
                        if self.mMap[y+1][x] != "#":
                            Tile(self.mWorld, b2Vec2(x, y), TileType.WALL)
                            continue
                    elif y == self.height-1:
                        if self.mMap[y-1][x] != "#":
                            Tile(self.mWorld, b2Vec2(x, y), TileType.WALL)
                            continue
                    
                    if y > 0 and y < self.height-1 and x > 0 and x < self.width-1:
                        if self.mMap[y-1][x] != "#" or self.mMap[y+1][x] != "#" or self.mMap[y][x-1] != "#" or self.mMap[y][x+1] != "#":  
                            Tile(self.mWorld, b2Vec2(x, y), TileType.WALL)
                            
                elif self.mMap[y][x] == "S":
                    self.mStartPos = (x, y)
                elif self.mMap[y][x] == "*":
                    Tile(self.mWorld, b2Vec2(x, y), TileType.GRAVITYZONE)
                elif self.mMap[y][x] == "B":
                    self.mObjects.append(Box(b2Vec2(x, y), self.mWorld, self.mGravity))
    
    def __createPickups(self):
        objects = json.loads(self.mPickups)
        
        if len(objects) > 0:
            for obj in range(len(objects)):
                x, y = objects[obj]["POS"].split(",")
                type = objects[obj]["TYPE"]
                
                if type == ObjectType.NUGGET:
                    self.mObjects.append(Nugget((x,y), self.mWorld))
                    
    
    def nextLevel(self):
        if self.mCurrentLevel < self.__mMaxLevels:
            self.mCurrentLevel += 1
            self.__loadLevel(self)
            
class ObjectType(object):
    NUGGET = "NUGGET"
