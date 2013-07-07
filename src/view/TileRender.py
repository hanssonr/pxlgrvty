import pygame, random
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *
from model.Tile import Tile, TileType

class TileRender(object):
    
    def __init__(self, camera, tiles):
        self.mCamera = camera
        self.mTiles = tiles
        
        self.stonetile = Sprite(Resources.getInstance().mRock)
        self.mudtile = Sprite(Resources.getInstance().mMud)
        
    
    def render(self, delta):
        
        for tile in self.mTiles:
            if self.mCamera.isInFrustum(tile.position.x, tile.position.y):
                viewpos = self.mCamera.getViewCoords(b2Vec2(tile.position.x - 0.5, tile.position.y - 0.5))
                
                if tile.tiletype == TileType.WALL:
                    self.stonetile.setSize(self.mCamera.getScaledSize(1, 1))
                    self.stonetile.draw(viewpos)
                    
    def levelUpdate(self, tiles):
        self.mTiles = tiles
                        
        
