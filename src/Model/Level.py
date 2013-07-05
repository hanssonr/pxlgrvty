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
from model.Camera import Camera
from model.Chunk import Chunk


class Level(object):
    
    CHUNK_SIZE = 16
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
    
    
    mActiveChunks = []
    mActiveChunk = None
    mMapType = None
    
    def __init__(self, world, gravity, camera):
        self.mWorld = world
        self.mGravity = gravity
        self.mCamera = camera
        self.__loadLevel()
        
    def __loadLevel(self):
        self.__readLevel()
        
        if self.mMapType == MapType.PICTURE:
            self.__createPictureWorldCollision()
        else:
            self.__createTextWorldCollision()
        #self.__createPickups()
    
    def __readLevel(self):
        #check for pictures first
        if os.path.exists("Assets/Levels/level%d.png" % self.mCurrentLevel):
            self.mMap = pygame.image.load("Assets/Levels/level%d.png" % self.mCurrentLevel)
            self.mWidth, self.mHeight = self.mMap.get_size()
            self.mMapType = MapType.PICTURE
        else: #check for lvl-file
            parser = ConfigParser.ConfigParser()
            parser.read("Assets/Levels/level%d.lvl" % self.mCurrentLevel)
            self.mMap = parser.get("level", "map").replace(" ", "").split("\n")
            self.mPickups = parser.get("objects", "pickups")
            self.mWidth = len(self.mMap[0])
            self.mHeight = len(self.mMap)
            self.mMapType = MapType.TEXT
        
    
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
    
    
    def __createPictureWorldCollision(self):
        self.mMap.lock()
        
        chunkx = self.mWidth / self.CHUNK_SIZE
        chunky = self.mHeight / self.CHUNK_SIZE
        
        self.mChunks = []
        
        for cy in range(chunky):
            self.mChunks.append([])
            for cx in range(chunkx):
                self.mChunks[cy].append([])
                
                chunkmap = self.mMap.subsurface(Rect(cx * self.CHUNK_SIZE, cy * self.CHUNK_SIZE, self.CHUNK_SIZE, self.CHUNK_SIZE))
                chunktiles = []
                
                for y in range(chunkmap.get_width()):
                    for x in range(chunkmap.get_height()):
                        
                        r,g,b,a = chunkmap.get_at((x, y))
                        
                        if (r,g,b) != Color.WHITE:
                            pos = b2Vec2(x + cx * self.CHUNK_SIZE,y + cy * self.CHUNK_SIZE)
                            
                            if (r,g,b) == Color.WALL:
                                #Tile(self.mWorld, pos, TileType.WALL
                                chunktiles.append(TestTile(pos, TileType.WALL))
                            elif (r,g,b) == Color.STARTPOS:
                                self.mStartPos = pos
                            elif (r,g,b) == Color.BOX:
                                self.mObjects.append(Box(pos, self.mWorld, self.mGravity))
                
                self.mChunks[cy][cx].append(chunktiles)                          
                            
        """
            for y in range(self.mHeight):
                for x in range(self.mWidth):
                
                    r,g,b,a = self.mMap.get_at((x, y))
                
                    if (r,g,b) != Color.WHITE:
                        pos = b2Vec2(x, y)
                    
                        if (r,g,b) == Color.WALL:
                            self.mTiles.append(Tile(self.mWorld, pos, TileType.WALL))
                        elif (r,g,b) == Color.STARTPOS:
                            self.mStartPos = pos
                        elif (r,g,b) == Color.BOX:
                            self.mObjects.append(Box(pos, self.mWorld, self.mGravity))"""
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
    
    
    def loadChunks(self, camerapos):
        #x1, y1, x2, y2 = camerapos.x - Camera.CAMERA_WIDTH/2, camerapos.y - Camera.CAMERA_HEIGHT/2, camerapos.x + Camera.CAMERA_WIDTH/2, camerapos.y + Camera.CAMERA_HEIGHT/2
        
        tl = self.mCamera.getChunkPosition(self.mCamera.displacement.x, self.mCamera.displacement.y)
        bl = self.mCamera.getChunkPosition(self.mCamera.displacement.x, self.mCamera.displacement.y + Camera.CAMERA_HEIGHT)
        br = self.mCamera.getChunkPosition(self.mCamera.displacement.x + Camera.CAMERA_WIDTH, self.mCamera.displacement.y - Camera.CAMERA_HEIGHT)
        tr = self.mCamera.getChunkPosition(self.mCamera.displacement.x + Camera.CAMERA_WIDTH, self.mCamera.displacement.y)
        
        if len(self.mActiveChunks) > 0:
            if not any(x.position == tl for x in self.mActiveChunks):
                print "add TL"
                self.__addToChunkList(tl)
            if not any(x.position == br for x in self.mActiveChunks):
                print "add BR"
                self.__addToChunkList(br)
            if not any(x.position == tr for x in self.mActiveChunks):
                print "add TR"
                self.__addToChunkList(tr)
            if not any(x.position == bl for x in self.mActiveChunks):
                print "add BL"
                self.__addToChunkList(bl)
                
        else:
            self.__addToChunkList(camerapos)
            
            
        """
            for tilerows in self.mChunks[int(chunkpos.y)][int(chunkpos.x)]:
                for tile in tilerows:
                    print tile.type
                    #self.mTiles.append(Tile(self.mWorld, tile.pos, TileType.WALL))
                    #self.mTiles.append(Tile(self.mWorld, tile.pos, tile.type))"""
    
    def __addToChunkList(self, pos):
        x = int(pos.x)
        y = int(pos.y)
        
        if x >= 0 and x <= self.mWidth / self.CHUNK_SIZE and y >= 0 and y <= self.mHeight / self.CHUNK_SIZE:
            self.mActiveChunks.append(Chunk(pos))
            for tile in self.mChunks[y][x][0]:
                self.mTiles.append(Tile(self.mWorld, tile.pos, tile.type))
    
    def unloadChunks(self, chunkpos):
        pass
            
class ObjectType(object):
    NUGGET = "NUGGET"

class MapType(object):
    PICTURE = 0
    TEXT = 1
    
class TestTile(object):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
