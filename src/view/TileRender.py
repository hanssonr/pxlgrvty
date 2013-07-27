import pygame, random
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *
from model.Tile import Tile, TileType
from libs.Animation import Animation

class TileRender(object):
    
    def __init__(self, camera, tiles, tileset):
        self.mCamera = camera
        self.mTiles = tiles
        self.mTileSprite = Animation(pygame.image.load("assets/gfx/tiles/%s" % tileset).convert_alpha(), 3, 11, 0, self.mCamera.getScaledSize(1,1))
        
    
    def render(self, delta):
        self.mTileSprite.setSize(self.mCamera.getScaledSize(1,1))
        for tile in self.mTiles:
            if self.mCamera.isInFrustum(tile.position.x, tile.position.y):
                viewpos = self.mCamera.getViewCoords(b2Vec2(tile.position.x - 0.5, tile.position.y - 0.5))
                
                #walls
                if tile.tiletype == TileType. TL:
                    self.mTileSprite.freeze(0,0)
                elif tile.tiletype == TileType.T:
                    self.mTileSprite.freeze(1,0)
                elif tile.tiletype == TileType.TR:
                    self.mTileSprite.freeze(2,0)
                elif tile.tiletype == TileType.L:
                    self.mTileSprite.freeze(0,1)
                elif tile.tiletype == TileType.M:
                    random.seed(tile.position.x / tile.position.y)
                    if random.randint(0,9) > 3:
                        self.mTileSprite.freeze(1,1)
                    else:
                        self.mTileSprite.freeze(2,7)
                elif tile.tiletype == TileType.R:
                    self.mTileSprite.freeze(2,1)
                elif tile.tiletype == TileType.BL:
                    self.mTileSprite.freeze(0,2)
                elif tile.tiletype == TileType.B:
                    self.mTileSprite.freeze(1,2)
                elif tile.tiletype == TileType.BR:
                    self.mTileSprite.freeze(2,2)    
                    
                #grass    
                elif tile.tiletype == TileType.GL:
                    self.mTileSprite.freeze(0,3)
                elif tile.tiletype == TileType.GM:
                    self.mTileSprite.freeze(1,3)
                elif tile.tiletype == TileType.GR:
                    self.mTileSprite.freeze(2,3)
                
                #edge    
                elif tile.tiletype == TileType.ETL:
                    self.mTileSprite.freeze(0,4)
                elif tile.tiletype == TileType.ET:
                    self.mTileSprite.freeze(1,4)
                elif tile.tiletype == TileType.ETR:
                    self.mTileSprite.freeze(2,4)
                elif tile.tiletype == TileType.EL:
                    self.mTileSprite.freeze(0,5)
                elif tile.tiletype == TileType.EM:
                    self.mTileSprite.freeze(1,5)
                elif tile.tiletype == TileType.ER:
                    self.mTileSprite.freeze(2,5)
                elif tile.tiletype == TileType.EBL:
                    self.mTileSprite.freeze(0,6)
                elif tile.tiletype == TileType.EB:
                    self.mTileSprite.freeze(1,6)
                elif tile.tiletype == TileType.EBR:
                    self.mTileSprite.freeze(2,6)
                
                #single
                elif tile.tiletype == TileType.S:
                    self.mTileSprite.freeze(1,5)
                elif tile.tiletype == TileType.SG:
                    self.mTileSprite.freeze(1,7)
                elif tile.tiletype == TileType.SL:
                    self.mTileSprite.freeze(0,8)
                elif tile.tiletype == TileType.SM:
                    self.mTileSprite.freeze(1,8)
                elif tile.tiletype == TileType.SR:
                    self.mTileSprite.freeze(2,8)
                elif tile.tiletype == TileType.SGL:
                    self.mTileSprite.freeze(0,9)
                elif tile.tiletype == TileType.SGM:
                    self.mTileSprite.freeze(1,9)
                elif tile.tiletype == TileType.SGR:
                    self.mTileSprite.freeze(2,9)
                elif tile.tiletype == TileType.SVB:
                    self.mTileSprite.freeze(0,10)
                elif tile.tiletype == TileType.SVM:
                    self.mTileSprite.freeze(1,10)
                elif tile.tiletype == TileType.SVT:
                    self.mTileSprite.freeze(2,10)
                    
                elif tile.tiletype == TileType.GRAVITYZONE:
                    self.mTileSprite.freeze(2,7)
                    
                self.mTileSprite.draw(delta, viewpos)
                    
    def levelUpdate(self, tiles, tileset):
        self.mTiles = tiles
        self.mTileSprite = Animation(pygame.image.load("assets/gfx/tiles/%s" % tileset).convert_alpha(), 3, 11, 0, self.mCamera.getScaledSize(1,1))
        
                        
        
