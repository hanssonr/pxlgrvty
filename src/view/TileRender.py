import pygame
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *

class TileRender(object):
    
    def __init__(self, camera, tiles):
        self.mCamera = camera
        self.mTiles = tiles
        
        self.tile = Sprite(Resources.getInstance().mMud, self.mCamera.spriteScale((1,1)))
        #self.tile.setSize(int(1 * self.mCamera.scale.x), int(1 * self.mCamera.scale.y))
        
        #self.tile = pygame.sprite.Sprite()
        #self.tile.image = pygame.image.load("assets/gfx/mud.png").convert()
        #self.tile.rect = self.tile.image.get_rect()
    
    def render(self, delta):
        for y in range(len(self.mTiles)):
            for x in range(len(self.mTiles[y])):
                if self.mTiles[y][x] == "#":
                    viewpos = self.mCamera.getViewCoordinats(b2Vec2(x, y))
                    self.tile.setPosition(viewpos.x, viewpos.y)
                    self.tile.draw(Pgl.app.surface)
