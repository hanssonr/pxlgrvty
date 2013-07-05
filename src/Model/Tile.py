from Box2D.Box2D import *

class Tile(object):
    
    TILE_SIZE = 1.0
    
    def __init__(self, world, position, tiletype):
        self.mWorld = world
        self.mPosition = b2Vec2(position.x + self.TILE_SIZE/2, position.y + self.TILE_SIZE/2)
        self.mTiletype = tiletype
        
        if tiletype == TileType.WALL:
            self.__createTile()
        elif tiletype == TileType.GRAVITYZONE:
            self.__createGravityZone()
             
    def __createTile(self):
        self.mBody = self.mWorld.CreateStaticBody(position = self.mPosition)
        #self.mBody.CreatePolygonFixture(box=(self.TILE_SIZE/2, self.TILE_SIZE/2))
        self.mBody.userData = self
        
        tl = b2Vec2(-self.TILE_SIZE/2, -self.TILE_SIZE/2)
        tr = b2Vec2(self.TILE_SIZE/2, -self.TILE_SIZE/2)
        br = b2Vec2(self.TILE_SIZE/2, self.TILE_SIZE/2)
        bl = b2Vec2(-self.TILE_SIZE/2, self.TILE_SIZE/2)
        
        self.mBody.CreateEdgeChain((tl, bl, br, tr, tl))
        
    
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
    WALL = 1
    GRAVITYZONE = 2