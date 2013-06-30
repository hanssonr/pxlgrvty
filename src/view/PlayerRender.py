import pygame
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *
from model.entities.Player import *

class PlayerRender(object):
    
    def __init__(self, camera, player):
        self.mCamera = camera
        self.mPlayer = player
        
        self.player = Sprite(Resources.getInstance().mPlayer)
        self.player.setSize(int(Player.PLAYER_WIDTH * self.mCamera.scale.x), int(Player.PLAYER_HEIGHT * self.mCamera.scale.y)) 
    
    def render(self, delta):
        viewpos = self.mCamera.getViewCoordinats(self.mPlayer.position)
        self.player.setPosition(viewpos.x - Player.PLAYER_WIDTH/2 * self.mCamera.scale.x, viewpos.y - Player.PLAYER_HEIGHT/2 * self.mCamera.scale.y)
        
        if self.mPlayer.mFacing == Facing.LEFT:
            if not self.player.flippedX():
                self.player.flip(True, False)
        elif self.mPlayer.mFacing == Facing.RIGHT:
            if self.player.flippedX():
                self.player.flip(False, False)
        
                
        if self.mPlayer.mUpsideDown == True:
            if not self.player.flippedY():
                if self.mPlayer.mFacing == Facing.LEFT:
                    self.player.flip(True, True)
                else:
                    self.player.flip(False, True)
        elif self.mPlayer.mUpsideDown == False:
            if self.player.flippedY():
                if self.mPlayer.mFacing == Facing.LEFT:
                    self.player.flip(False, False)
                else:
                    self.player.flip(True, False)
        
        self.player.draw()
        
