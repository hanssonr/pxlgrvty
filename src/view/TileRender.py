import pygame
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *
from model.Tile import Tile

class TileRender(object):
    
    def __init__(self, camera, tiles):
        self.mCamera = camera
        self.mTiles = tiles
        
        self.stonetile = Sprite(Resources.getInstance().mRock)
        self.mudtile = Sprite(Resources.getInstance().mMud)
        
    
    def render(self, delta):        
        for y in range(len(self.mTiles)):
            for x in range(len(self.mTiles[y])):
                if self.mTiles[y][x] == "#":
                    viewpos = self.mCamera.getViewCoords(b2Vec2(x, y))
                    self.stonetile.setSize(self.mCamera.getScaledSize(1,1))
                    self.mudtile.setSize(self.mCamera.getScaledSize(1,1)) 
                    try:
                        if self.mTiles[y+1][x] != "#" or self.mTiles[y-1][x] != "#" or self.mTiles[y][x-1] != "#" or self.mTiles[y][x+1] != "#":
                            self.mudtile.setPosition(viewpos.x, viewpos.y)
                            self.mudtile.draw(viewpos)
                        else:
                            self.stonetile.setPosition(viewpos.x, viewpos.y)
                            self.stonetile.draw(viewpos)
                    except:
                        pass
                        
                        
        
