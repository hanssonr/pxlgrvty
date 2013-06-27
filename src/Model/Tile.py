from Box2D.Box2D import b2EdgeShape, b2Body, b2Vec2
from Model.Camera import *

class Tile(object):
    
    TILE_SIZE = 1.0
    
    def __init__(self, world, position, tiletype):
        self.mWorld = world
        self.mPosition = b2Vec2(position.x + self.TILE_SIZE/2, position.y + self.TILE_SIZE/2)
        self.mTiletype = tiletype
        
        if tiletype != TileType.EMPTY:
            self.__createTile()
            
        
    
    def __createTile(self):
        self.mBody = self.mWorld.CreateStaticBody(position = self.mPosition)
        self.mBody.CreatePolygonFixture(box=(self.TILE_SIZE/2, self.TILE_SIZE/2))
        self.mBody.userData = self


class TileType(object):
    EMPTY = 0
    WALL = 1