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
        
        self.tile = Sprite(Resources.getInstance().mMud)
        self.tile.setSize(int(1 * self.mCamera.scale.x), int(1 * self.mCamera.scale.y)) 
    
    def render(self, delta):        
        for y in range(len(self.mTiles)):
            for x in range(len(self.mTiles[y])):
                if self.mTiles[y][x] == "#":
                    viewpos = self.mCamera.getViewCoordinats(b2Vec2(x, y))
                     
                    self.tile.setPosition(viewpos.x, viewpos.y)
                    self.tile.draw()
        
