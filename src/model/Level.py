"""
Levelclass, reads the levelfiles and creates collision from either txt-files or pictures
Handles the update of the chunks that gets created if picturecollision is done

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.Tile import Tile, TileType
from Box2D import b2Vec2
import configparser, json, os, pygame
from model.entities.Box import Box
from model.entities.Crystal import Crystal
from model.entities.SpikeBox import SpikeBox
from model.entities.Spike import Spike
from model.entities.Saw import Saw
from model.entities.Laser import Laser
from model.Color import Color
from pygame import Rect
from model.Chunk import Chunk
from model.ChunkHandler import ChunkHandler
from libs.Crypt import Crypt
from Resources import Resources


class Level(object):

    CHUNK_SIZE = 8
    mMaxLevels = None
    mCurrentLevel = None
    mTiles = None
    mMap = None
    mWidth = None
    mHeight = None
    mStartPos = None
    mEndPos = None
    mEnemies = None
    mObjects = None
    mLevelDone = None
    mChunkHandler = None
    mMapType = None
    mCurrentTileset = None
    mSwirlActive = None
    mAllTiles = None

    #dataholders
    mPickupData = None
    mEnemyData = None
    mBoxData = None

    #crypt/decrypt
    __mCrypt = None

    def __init__(self, world, gravity, lvl):
        self.__mCrypt = Crypt()
        self.mMaxLevels = self.countLevels()
        self.mSwirlActive = False
        self.mLevelDone = False
        self.mTiles = []
        self.mObjects = []
        self.mEnemies = []
        self.mWorld = world
        self.mGravity = gravity
        self.mCurrentLevel = lvl
        self.mAllTiles = []

        self.__loadLevel()

    def __loadLevel(self):
        self.mChunkHandler = ChunkHandler(self.mWorld, self.CHUNK_SIZE)
        self.__readLevel()

        if self.mMapType == MapType.PICTURE:
            self.__createPictureWorldCollision()
            print("startpos: ", self.mStartPos)
            self.mChunkHandler.activateChunk(self.mChunkHandler.getChunk(self.mChunkHandler.getChunkPosition(self.mStartPos)))
            self.mTiles = self.mChunkHandler.mActiveTiles
        else:
            self.__createTextWorldCollision()
        self.__createPickups()
        self.__createEnemies()
        self.__createBoxes()

    """
        Reads in enemies, pickups and if there's not a picture specified, worldcollision
        http://qq.readthedocs.org/en/latest/tiles.html#map-definition
    """
    def __readLevel(self):
        parser = self.__mCrypt.dectryptParser(self.mCurrentLevel)
        self.mCurrentTileset = parser.get("level", "tileset")
        self.mBackground = parser.get("level", "bg")
        bgcolor = pygame.image.load(Resources.getInstance().resource_path("assets/gfx/%s" % self.mBackground))
        self.mBackgroundcolor = bgcolor.get_at((0, 0))
        self.mPickupData = parser.get("objects", "pickups")
        self.mEnemyData = parser.get("objects", "enemies")
        self.mBoxData = parser.get("objects", "boxes")

        #Mapcollision
        #check for pictures first
        if os.path.exists(Resources.getInstance().resource_path("assets/levels/level%d.png" % self.mCurrentLevel)):
            self.mMap = pygame.image.load(Resources.getInstance().resource_path("assets/levels/level%d.png" % self.mCurrentLevel))
            self.mWidth, self.mHeight = self.mMap.get_size()
            self.mMapType = MapType.PICTURE
        else: #check for lvl-file
            self.mMap = parser.get("level", "map").replace(" ", "").split("\n")
            self.mWidth = len(self.mMap[0])
            self.mHeight = len(self.mMap)
            self.mMapType = MapType.TEXT

    def __unloadCurrentLevel(self):
        self.mEndPos = None
        self.mStartPos = None
        self.mSwirlActive = False
        self.__unloadEntities()
        for tile in self.mTiles:
            tile.destroy()

        self.mTiles = []

    def __unloadEntities(self):
        for obj in self.mObjects:
            if obj.alive:
                self.mWorld.DestroyBody(obj.getBody())

        for e in self.mEnemies:
            self.mWorld.DestroyBody(e.getBody())

        self.mObjects = []
        self.mEnemies = []


    def update(self, delta, playerpos):
        if self.mMapType == MapType.PICTURE:
            self.mChunkHandler.manageChunks(playerpos)

        if not self.mLevelDone:
            self.checkLevelCompletion(playerpos)
        else:
            self.mLevelDone = False
            return True


    def checkLevelCompletion(self, pos):
        done = True
        for o in self.mObjects:
            if isinstance(o, Crystal):
                if o.alive:
                    done = False
                    break

        if done:
            self.mSwirlActive = True

            if (pos.x > self.mEndPos.x and pos.x < self.mEndPos.x + Tile.TILE_SIZE and
                pos.y > self.mEndPos.y and pos.y < self.mEndPos.y + Tile.TILE_SIZE):
                    self.__updateLevelLockState()
                    self.mLevelDone = True

    #updates the statefile if a level is cleared
    def __updateLevelLockState(self):
        with open(Resources.getInstance().resource_path("assets/state/state.json"), "rb") as state:
            decryptedData = self.__mCrypt.decrypt(state.read())
            lvldata = json.loads(decryptedData)

        if int(lvldata["LVL"]) <= self.mCurrentLevel:
            with open(Resources.getInstance().resource_path("assets/state/state.json"), "wb") as data:
                lvl = min(self.mCurrentLevel+1, self.mMaxLevels)
                data.write(self.__mCrypt.encrypt('{"LVL":"%s"}' % (str(lvl))))

    #create collisiontiles from txt-file
    def __createTextWorldCollision(self):
        for y in range(self.mHeight):
            for x in range(self.mWidth):

                if self.mMap[y][x] == "#":
                    self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), self.__calculateTileType(x, y)))
                elif self.mMap[y][x] == "S":
                    self.mStartPos = b2Vec2(x, y)
                elif self.mMap[y][x] == "E":
                    self.mEndPos = b2Vec2(x, y)
                elif self.mMap[y][x] == "*":
                    self.mTiles.append(Tile(self.mWorld, b2Vec2(x, y), TileType.GRAVITYZONE))
                elif self.mMap[y][x] == "B":
                    self.mObjects.append(Box(b2Vec2(x, y), self.mWorld, self.mGravity))

        for tile in self.mTiles:
            tile.create()

    #create collisiontiles from picture and divid em into chunks
    def __createPictureWorldCollision(self):
        self.mMap.lock()

        chunkx = self.mWidth / self.CHUNK_SIZE
        chunky = self.mHeight / self.CHUNK_SIZE

        for cy in range(int(chunky)):
            self.mChunkHandler.chunkslist.append([])
            for cx in range(int(chunkx)):
                self.mChunkHandler.chunkslist[cy].append([])

                chunkmap = self.mMap.subsurface(Rect(cx * self.CHUNK_SIZE, cy * self.CHUNK_SIZE, self.CHUNK_SIZE, self.CHUNK_SIZE))
                chunktiles = []

                for y in range(chunkmap.get_height()):
                    for x in range(chunkmap.get_width()):

                        r,g,b,a = chunkmap.get_at((x, y))

                        #mapx / mapy
                        mx = x + cx * self.CHUNK_SIZE
                        my = y + cy * self.CHUNK_SIZE

                        if (r,g,b) != Color.WHITE:

                            pos = b2Vec2(mx, my)

                            if (r,g,b) == Color.WALL:
                                self.mAllTiles.append(Tile(self.mWorld, pos, self.__calculateTileType(mx, my)))
                                chunktiles.append(Tile(self.mWorld, pos, self.__calculateTileType(mx, my)))
                            elif (r,g,b) == Color.STARTPOS:
                                self.mStartPos = pos
                            elif (r,g,b) == Color.ENDPOS:
                                self.mEndPos = pos

                self.mChunkHandler.chunkslist[cy][cx] = Chunk(b2Vec2(cx, cy), chunktiles)
        self.mMap.unlock()

    def __isWallType(self, tile):
        if self.mMapType == MapType.PICTURE:
            return True if tile == Color.WALL else False
        else:
            return True if tile == "#" else False

    def __accessMap(self, x, y):
        if self.mMapType == MapType.PICTURE:
            return self.mMap.get_at((x, y))
        else:
            return self.mMap[y][x]

    def __calculateTileType(self, mx, my):
        tiletype = TileType.M

        #left edge
        if mx == 0:
            if my == 0:
                tiletype = TileType.ETL
            elif my == self.mHeight-1:
                tiletype = TileType.EBL
            elif self.__isWallType(self.__accessMap(mx+1, my)) or self.__isWallType(self.__accessMap(mx+1, my)):
                tiletype = TileType.EL
            else:
                tiletype = TileType.R

        #right edge
        elif mx == self.mWidth-1:
            if my == 0:
                tiletype = TileType.ETR
            elif my == self.mHeight-1:
                tiletype = TileType.EBR
            elif self.__isWallType(self.__accessMap(mx-1, my)):
                tiletype = TileType.ER
            else:
                tiletype = TileType.L

        #top
        elif my == 0:
            if not self.__isWallType(self.__accessMap(mx, my+1)):
                tiletype = TileType.B
            else:
                tiletype = TileType.ET

        #bottom
        elif my == self.mHeight-1:
            if not self.__isWallType(self.__accessMap(mx, my-1)):
                tiletype = TileType.GM
            else:
                tiletype = TileType.EB

        if my > 0 and my < self.mHeight-1 and mx > 0 and mx < self.mWidth-1:

            #only under
            if not self.__isWallType(self.__accessMap(mx, my-1)) and self.__isWallType(self.__accessMap(mx, my+1)):

                #only right side
                if not self.__isWallType(self.__accessMap(mx-1, my)) and self.__isWallType(self.__accessMap(mx+1, my)):
                    tiletype = TileType.GL

                #only left side
                elif not self.__isWallType(self.__accessMap(mx+1, my)) and self.__isWallType(self.__accessMap(mx-1, my)):
                    tiletype = TileType.GR

                #neither sides
                elif not self.__isWallType(self.__accessMap(mx+1, my)) and not self.__isWallType(self.__accessMap(mx-1, my)):
                    tiletype = TileType.SVT
                else:
                    tiletype = TileType.GM

            #only over
            elif self.__isWallType(self.__accessMap(mx, my-1)) and not self.__isWallType(self.__accessMap(mx, my+1)):

                #only right side
                if not self.__isWallType(self.__accessMap(mx-1, my)) and self.__isWallType(self.__accessMap(mx+1, my)):
                    tiletype = TileType.BL

                #only left side
                elif not self.__isWallType(self.__accessMap(mx+1, my)) and self.__isWallType(self.__accessMap(mx-1, my)):
                    tiletype = TileType.BR

                #neither sides
                elif not self.__isWallType(self.__accessMap(mx+1, my)) and not self.__isWallType(self.__accessMap(mx-1, my)):
                    tiletype = TileType.SVB
                else:
                    tiletype = TileType.B

            #not over nor under
            elif not self.__isWallType(self.__accessMap(mx, my-1)) and not self.__isWallType(self.__accessMap(mx, my+1)):

                #neither sides
                if not self.__isWallType(self.__accessMap(mx-1, my)) and not self.__isWallType(self.__accessMap(mx+1, my)):
                    tiletype = TileType.SG

                #only right side
                elif not self.__isWallType(self.__accessMap(mx-1, my)) and self.__isWallType(self.__accessMap(mx+1, my)):
                    tiletype = TileType.SGL

                #only left side
                elif not self.__isWallType(self.__accessMap(mx+1, my)) and self.__isWallType(self.__accessMap(mx-1, my)):
                    tiletype = TileType.SGR
                else:
                    tiletype = TileType.SGM
            else:

                #only left side
                if not self.__isWallType(self.__accessMap(mx+1, my)) and self.__isWallType(self.__accessMap(mx-1, my)):
                    tiletype = TileType.R

                #only right side
                elif not self.__isWallType(self.__accessMap(mx-1, my)) and self.__isWallType(self.__accessMap(mx+1, my)):
                    tiletype = TileType.L

                #neither sides
                elif not self.__isWallType(self.__accessMap(mx-1, my)) and not self.__isWallType(self.__accessMap(mx+1, my)):
                    tiletype = TileType.SVM

                else:
                    tiletype = TileType.M

        return tiletype

    def __createPickups(self):
        objects = json.loads(self.mPickupData)

        if len(objects) > 0:
            for obj in range(len(objects)):
                x, y = [float(i) for i in objects[obj]["POS"].split(",")]
                objtype = objects[obj]["TYPE"]

                if objtype == ObjectType.NUGGET:
                    self.mObjects.append(Crystal((x,y), self.mWorld))

    def __createEnemies(self):
        enemies = json.loads(self.mEnemyData)

        if len(enemies) > 0:
            for e in range(len(enemies)):
                x, y = [float(i) for i in enemies[e]["POS"].split(",")]
                etype = enemies[e]["TYPE"]

                if etype == EnemyType.SPIKEBOX:
                    speed = float(enemies[e]["SPEED"])
                    delay = float(enemies[e]["DELAY"])
                    ex, ey = [float(i) for i in enemies[e]["ENDPOS"].split(",")]
                    self.mEnemies.append(SpikeBox(self.mWorld, (x,y), (ex, ey), delay, speed))
                elif etype == EnemyType.SPIKE:
                    facing = int(enemies[e]["FACING"])
                    self.mEnemies.append(Spike(self.mWorld, (x,y), facing))
                elif etype == EnemyType.SAW:
                    pattern = [(k, v) for k,v in (str(enemies[e]["PATTERN"][x]).split(",") for x in range(len(enemies[e]["PATTERN"])))]
                    speed = float(enemies[e]["SPEED"])
                    radius = float(enemies[e]["RADIUS"])
                    self.mEnemies.append(Saw(self.mWorld, (x,y), pattern, radius, speed))
                elif etype == EnemyType.LASER:
                    ex, ey = [float(i) for i in enemies[e]["ENDPOS"].split(",")]
                    delay = float(enemies[e]["DELAY"])
                    triggertime = float(enemies[e]["T_TIMER"])
                    firingtime = float(enemies[e]["F_TIMER"])
                    self.mEnemies.append(Laser(self.mWorld, b2Vec2(x,y), b2Vec2(ex,ey), delay, triggertime, firingtime))

    def __createBoxes(self):
        boxes = json.loads(self.mBoxData)

        if len(boxes) > 0:
            for box in range(len(boxes)):
                x, y = [float(i) for i in boxes[box]["POS"].split(",")]
                self.mObjects.append(Box(b2Vec2(x, y), self.mWorld, self.mGravity))

    def nextLevel(self):
        if self.mCurrentLevel < self.mMaxLevels:
            self.__unloadCurrentLevel()
            self.mCurrentLevel += 1
            self.__loadLevel()

    def retryLevel(self):
        self.__unloadEntities()
        self.__createPickups()
        self.__createEnemies()
        #self.__createBoxes()
        self.mSwirlActive = False

    def isInActiveChunks(self, position):
        return True if self.mMapType == MapType.TEXT else self.mChunkHandler.isPositionInActiveChunks(position)

    @staticmethod
    def countLevels():
        lvls = 0
        for filename in os.listdir(Resources.getInstance().resource_path("assets/levels")):
            if filename.endswith(".lvl"):
                lvls += 1
        return lvls

class ObjectType(object):
    NUGGET = "NUGGET"

class EnemyType(object):
    SPIKEBOX = "SPIKEBOX"
    SPIKE = "SPIKE"
    SAW = "SAW"
    LASER = "LASER"

class MapType(object):
    PICTURE = 0
    TEXT = 1
