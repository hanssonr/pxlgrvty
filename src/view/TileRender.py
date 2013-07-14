import pygame, random
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *
from model.Tile import Tile, TileType
from libs.Animation import Animation

class TileRender(object):
    
    def __init__(self, camera, tiles):
        self.mCamera = camera
        self.mTiles = tiles
        self.dirt = Animation(Resources.getInstance().mDirtTiles, 3, 11, 0, self.mCamera.getScaledSize(1,1))
        
    
    def render(self, delta):
        self.dirt.setSize(self.mCamera.getScaledSize(1,1))
        for tile in self.mTiles:
            if self.mCamera.isInFrustum(tile.position.x, tile.position.y):
                viewpos = self.mCamera.getViewCoords(b2Vec2(tile.position.x - 0.5, tile.position.y - 0.5))
                
                #walls
                if tile.tiletype == TileType. TL:
                    self.dirt.freeze(0,0)
                elif tile.tiletype == TileType.T:
                    self.dirt.freeze(1,0)
                elif tile.tiletype == TileType.TR:
                    self.dirt.freeze(2,0)
                elif tile.tiletype == TileType.L:
                    self.dirt.freeze(0,1)
                elif tile.tiletype == TileType.M:
                    self.dirt.freeze(1,1)
                elif tile.tiletype == TileType.R:
                    self.dirt.freeze(2,1)
                elif tile.tiletype == TileType.BL:
                    self.dirt.freeze(0,2)
                elif tile.tiletype == TileType.B:
                    self.dirt.freeze(1,2)
                elif tile.tiletype == TileType.BR:
                    self.dirt.freeze(2,2)    
                    
                #grass    
                elif tile.tiletype == TileType.GL:
                    self.dirt.freeze(0,3)
                elif tile.tiletype == TileType.GM:
                    self.dirt.freeze(1,3)
                elif tile.tiletype == TileType.GR:
                    self.dirt.freeze(2,3)
                
                #edge    
                elif tile.tiletype == TileType.ETL:
                    self.dirt.freeze(0,4)
                elif tile.tiletype == TileType.ET:
                    self.dirt.freeze(1,4)
                elif tile.tiletype == TileType.ETR:
                    self.dirt.freeze(2,4)
                elif tile.tiletype == TileType.EL:
                    self.dirt.freeze(0,5)
                elif tile.tiletype == TileType.EM:
                    self.dirt.freeze(1,5)
                elif tile.tiletype == TileType.ER:
                    self.dirt.freeze(2,5)
                elif tile.tiletype == TileType.EBL:
                    self.dirt.freeze(0,6)
                elif tile.tiletype == TileType.EB:
                    self.dirt.freeze(1,6)
                elif tile.tiletype == TileType.EBR:
                    self.dirt.freeze(2,6)
                
                #single
                elif tile.tiletype == TileType.S:
                    self.dirt.freeze(1,5)
                elif tile.tiletype == TileType.SG:
                    self.dirt.freeze(1,7)
                elif tile.tiletype == TileType.SL:
                    self.dirt.freeze(0,8)
                elif tile.tiletype == TileType.SM:
                    self.dirt.freeze(1,8)
                elif tile.tiletype == TileType.SR:
                    self.dirt.freeze(2,8)
                elif tile.tiletype == TileType.SGL:
                    self.dirt.freeze(0,9)
                elif tile.tiletype == TileType.SGM:
                    self.dirt.freeze(1,9)
                elif tile.tiletype == TileType.SGR:
                    self.dirt.freeze(2,9)
                elif tile.tiletype == TileType.SVB:
                    self.dirt.freeze(0,10)
                elif tile.tiletype == TileType.SVM:
                    self.dirt.freeze(1,10)
                elif tile.tiletype == TileType.SVT:
                    self.dirt.freeze(2,10)
                    
                elif tile.tiletype == TileType.GRAVITYZONE:
                    self.dirt.freeze(2,7)
                    
                self.dirt.draw(delta, viewpos)
                    
    def levelUpdate(self, tiles):
        self.mTiles = tiles
        
                        
        
