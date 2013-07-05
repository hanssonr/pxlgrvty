
class Chunk(object):
    
    def __init__(self, pos):
        self.pos = pos
        
    
    def __getPosition(self):
        return self.pos
    
    def __getTiles(self):
        return self.tiles
    
    def __setTile(self, tile):
        self.tiles.append(tile)
    
    
    tiles = property(__getTiles, __setTile)
    position = property(__getPosition, None)