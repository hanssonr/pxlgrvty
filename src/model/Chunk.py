"""
A chunk that contains information about the tiles that are in a certain area of the map

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

class Chunk(object):
    
    def __init__(self, pos, tiles):
        self.mPos = pos
        self.mTiles = tiles
        
    
    def __getPosition(self):
        return self.mPos
    
    def __getTiles(self):
        return self.mTiles
    
    def __setTile(self, tile):
        self.mTiles.append(tile)
    
    
    tiles = property(__getTiles, __setTile)
    position = property(__getPosition, None)