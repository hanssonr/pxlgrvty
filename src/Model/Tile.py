
class Tile(object):
    
    TILE_SIZE = 1.0
    
    def __init__(self, world, position, tiletype):
        self.mWorld = world
        self.mPosition = position
        self.mTiletype = tiletype
        
        if tiletype != ".":
            self.__createTile()
            
        
    
    def __createTile(self):
        self.mBody = self.mWorld.CreateStaticBody(position = self.mPosition)
        self.mBody.CreatePolygonFixture(box=(self.TILE_SIZE/2, self.TILE_SIZE/2))
        self.mBody.userData = self