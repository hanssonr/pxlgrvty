"""
http://qq.readthedocs.org/en/latest/tiles.html#map-definition
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tile import Tile, TileType
from Box2D import b2Vec2
import ConfigParser, json, os, pygame
from model.entities.Box import Box
from model.entities.Nugget import Nugget
from Color import Color
from pygame import Rect
from model.Chunk import Chunk
from model.ChunkHandler import ChunkHandler


class Level(object):
    
    CHUNK_SIZE = 8
    __mMaxLevels = 3 #read out from all the .lvl files later
    mCurrentLevel = 1
    mTiles = []
    mMap = None
    mWidth = None
    mHeight = None
    mStartPos = None
    mPickups = None
    mObjects = []
    mChunks = None
    
    mChunkHandler = None
    
    
    mActiveChunks = []
    mActiveChunk = None
    mMapType = None
    
    def __init__(self, world, gravity):
        self.mWorld = world
        self.mGravity = gravity
        self.mChunkHandler = ChunkHandler(world, self.CHUNK_SIZE)
        self.__loadLevel()
        
    def __loadLevel(self):
        self.__readLevel()
        
        if self.mMapType == MapType.PICTURE:
            self.__createPictureWorldCollision()
            self.mChunkHandler.activateChunk(self.mChunkHandler.getChunk(self.mChunkHandler.getChunkPosition(self.mStartPos)))
            self.mTiles = self.mChunkHandler.mActiveTiles
        else:
            self.__createTextWorldCollision()
        self.__createPickups()
        

    """ Reads in enemies, pickups and if there's not a picture specified, worldcollision """
    def __readLevel(self):
        parser = ConfigParser.ConfigParser()
        parser.read("Assets/Levels/level%d.lvl" % self.mCurrentLevel)
        self.mPickups = parser.get("objects", "pickups")
        
        #Mapcollision
        #check for pictures first
        if os.path.exists("Assets/Levels/level%d.png" % self.mCurrentLevel):
            self.mMap = pygame.image.load("Assets/Levels/level%d.png" % self.mCurrentLevel)
            self.mWidth, self.mHeight = self.mMap.get_size()
            self.mMapType = MapType.PICTURE
        else: #check for lvl-file
            self.mMap = parser.get("level", "map").replace(" ", "").split("\n")
            self.mWidth = len(self.mMap[0])
            self.mHeight = len(self.mMap)
            self.mMapType = MapType.TEXT
    
    
    def update(self, playerpos):
        if self.mMapType == MapType.PICTURE:
            self.mChunkHandler.manageChunks(playerpos)
        
    
    def __createTextWorldCollision(self):
        for y in range(self.mHeight):
            for x in range(self.mWidth):
                
                if self.mMap[y][x] == "#":

                    #do only necessary collisions
                    if x == 0:
                        if self.mMap[y][x+1] != "#":
                            self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.WALL))
                            continue
                    elif x == self.mWidth-1:
                        if self.mMap[y][x-1] != "#":
                            self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.WALL))
                            continue
                    
                    if y == 0:
                        if self.mMap[y+1][x] != "#":
                            self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.WALL))
                            continue
                    elif y == self.mHeight-1:
                        if self.mMap[y-1][x] != "#":
                            self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.WALL))
                            continue
                    
                    if y > 0 and y < self.mHeight-1 and x > 0 and x < self.mWidth-1:
                        if self.mMap[y-1][x] != "#" or self.mMap[y+1][x] != "#" or self.mMap[y][x-1] != "#" or self.mMap[y][x+1] != "#":  
                            self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.WALL))
                            
                elif self.mMap[y][x] == "S":
                    self.mStartPos = (x, y)
                elif self.mMap[y][x] == "*":
                    self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.GRAVITYZONE))
                elif self.mMap[y][x] == "B":
                    self.mObjects.append(Box(b2Vec2(x, y), self.mWorld, self.mGravity))
        
        for tile in self.mTiles:
            tile.create()
    
    
    def __createPictureWorldCollision(self):
        self.mMap.lock()
        
        chunkx = self.mWidth / self.CHUNK_SIZE
        chunky = self.mHeight / self.CHUNK_SIZE
        
        for cy in range(chunky):
            self.mChunkHandler.chunkslist.append([])
            for cx in range(chunkx):
                self.mChunkHandler.chunkslist[cy].append([])
                
                chunkmap = self.mMap.subsurface(Rect(cx * self.CHUNK_SIZE, cy * self.CHUNK_SIZE, self.CHUNK_SIZE, self.CHUNK_SIZE))
                chunktiles = []
                
                for y in range(chunkmap.get_width()):
                    for x in range(chunkmap.get_height()):
                        
                        r,g,b,a = chunkmap.get_at((x, y))
                        
                        if (r,g,b) != Color.WHITE:
                            pos = b2Vec2(x + cx * self.CHUNK_SIZE, y + cy * self.CHUNK_SIZE)
                            
                            if (r,g,b) == Color.WALL:
                                chunktiles.append(Tile(self.mWorld, pos, TileType.WALL))
                            elif (r,g,b) == Color.STARTPOS:
                                self.mStartPos = pos
                            elif (r,g,b) == Color.BOX:
                                print "box"
                                self.mObjects.append(Box(pos, self.mWorld, self.mGravity))
                
                self.mChunkHandler.chunkslist[cy][cx] = (Chunk(b2Vec2(cx, cy), chunktiles))                          
        self.mMap.unlock()
    
    def __createPickups(self):
        objects = json.loads(self.mPickups)
        
        if len(objects) > 0:
            for obj in range(len(objects)):
                x, y = objects[obj]["POS"].split(",")
                objtype = objects[obj]["TYPE"]
                
                if objtype == ObjectType.NUGGET:
                    self.mObjects.append(Nugget((x,y), self.mWorld))
                    
    
    def nextLevel(self):
        if self.mCurrentLevel < self.__mMaxLevels:
            self.mCurrentLevel += 1
            self.__loadLevel(self)
            
    def isInActiveChunks(self, position):
        return self.mChunkHandler.isPositionInActiveChunks(position)
    

class ObjectType(object):
    NUGGET = "NUGGET"

class MapType(object):
    PICTURE = 0
    TEXT = 1
