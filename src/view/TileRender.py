"""
Class that draws different tiles depending on their tiletype

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

import random, pygame
from pygame import Rect
from model.Tile import TileType
from libs.Animation import Animation
from libs.Sprite import Sprite
from Box2D import b2Vec2
from libs.Pgl import *
from Resources import Resources

class TileRender(object):

    def __init__(self, camera, level):
        self.mCamera = camera
        self.levelUpdate(level)
        self.level = level

    def render(self, delta):

        x = self.mCamera.displacement.x * self.mCamera.scale.x
        y = self.mCamera.displacement.y * self.mCamera.scale.y
        w = self.mCamera.CAMERA_WIDTH * self.mCamera.scale.x
        h = self.mCamera.CAMERA_HEIGHT * self.mCamera.scale.y

        rect = Rect(x, y, w, h)
        Pgl.app.surface.blit(self.sf, (0, 0), rect)

    def levelUpdate(self, level):
        self.mTiles = level.mAllTiles
        self.mTileSprite = Animation(pygame.image.load(Resources.getInstance().resource_path("assets/gfx/tiles/%s" % level.mCurrentTileset)).convert_alpha(), 3, 11, 0, self.mCamera.getScaledSize(1,1))

        width = int(level.mWidth * self.mCamera.scale.x)
        height = int(level.mHeight * self.mCamera.scale.y)

        scale = self.mCamera.getScaledSize(1,1)
        self.sf = pygame.Surface((width, height), flags=pygame.SRCALPHA);
        self.mCamera.displacement = b2Vec2(0,0);

        for tile in self.mTiles:

            viewpos = self.mCamera.getViewCoords(b2Vec2(tile.position.x - 0.5, tile.position.y - 0.5))

            #walls
            if tile.tiletype == TileType.TL:
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


            area = self.mTileSprite.getRect()
            toDraw = self.mTileSprite.image.subsurface(area)
            toDraw = pygame.transform.scale(toDraw, (int(scale.x), int(scale.y)))
            self.sf.blit(toDraw, (viewpos.x, viewpos.y))
