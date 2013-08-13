from Box2D.Box2D import *
from model.Filter import *

class Tile(object):
    
    TILE_SIZE = 1.0
    mCollideableWalls = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    mBody = None
    
    def __init__(self, world, position, tiletype):
        self.mWorld = world
        self.mPosition = b2Vec2(position.x + self.TILE_SIZE/2, position.y + self.TILE_SIZE/2)
        self.mTiletype = tiletype
    
    def create(self):
        if self.__isWall(self.mTiletype):
            self.__createTile()
        elif self.mTiletype == TileType.GRAVITYZONE:
            self.__createGravityZone()
    
    def destroy(self):
        if self.__isWall(self.mTiletype):
            self.mWorld.DestroyBody(self.mBody)
        
    def __isWall(self, tiletype):
        return True if any(t == tiletype for t in self.mCollideableWalls) else False
                
    def __createTile(self):
        tl = b2Vec2(-self.TILE_SIZE/2, -self.TILE_SIZE/2)
        tr = b2Vec2(self.TILE_SIZE/2, -self.TILE_SIZE/2)
        br = b2Vec2(self.TILE_SIZE/2, self.TILE_SIZE/2)
        bl = b2Vec2(-self.TILE_SIZE/2, self.TILE_SIZE/2)
        
        shape = b2ChainShape()
        shape.vertices = (bl, br, tr, tl)
        fd = b2FixtureDef()
        fd.categoryBits = Filter.CATEGORY_WALLS
        fd.maskBits = Filter.MASK_WALLS
        fd.shape = shape
        
        self.mBody = self.mWorld.CreateStaticBody(position = self.mPosition)
        
        self.mBody.CreateFixture(fd)
        self.mBody.userData = self
        
    
    def __createGravityZone(self):
        self.mBody = self.mWorld.CreateStaticBody(position = self.mPosition)
        shape = b2PolygonShape()
        shape.SetAsBox(self.TILE_SIZE/2, self.TILE_SIZE/2)
        fd = b2FixtureDef()
        fd.shape = shape
        fd.isSensor = True
        fd.bullet = True
        fd.userData = TileType.GRAVITYZONE
        self.mBody.CreateFixture(fd)
    
    def __getPosition(self):
        return self.mPosition
    
    def __getType(self):
        return self.mTiletype
    
    position = property(__getPosition, None)
    tiletype = property(__getType, None)


class TileType(object):
    EMPTY = 0
    S = 1       #single
    SG = 2      #singlegrass
    TL = 3      #topleft
    T = 4       #top
    TR = 5      #topright
    L = 6       #left
    M = 7       #middle
    R = 8       #right
    BL = 9      #bottomleft
    B = 10      #bottom
    BR = 11     #bottomright
    GL = 12     #grassleft
    GM = 13     #grassmiddle
    GR = 14     #grassright
    ETL = 15    #edgetopleft
    ET = 16     #edgetop
    ETR = 17    #edgetopright
    EL = 18     #edgeleft
    EM = 19     #edgemiddle
    ER = 20     #edgeright
    EBL = 21    #edgebottomleft
    EB = 22     #edgebottom
    EBR = 23    #edgebottomright
    SL = 24     #singleleft
    SM = 25     #singlemiddle
    SR = 26     #singleright
    SGL = 27    #singlegrassleft
    SGM = 28    #singlegrassmiddle
    SGR = 29    #singlegrassright
    SVM = 30     #singleverticalmiddle
    SVT = 31    #singleverticaltop
    SVB = 32    #singleverticalbottom
    
    GRAVITYZONE = 99
    