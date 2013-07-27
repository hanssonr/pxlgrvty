import pygame
from libs.Pgl import *
from libs.Sprite import *
from model.Camera import *
from Resources import *
from model.entities.Player import *
from libs.Animation import Animation

class PlayerRender(object):
    
    def __init__(self, camera, player):
        self.mCamera = camera
        self.mPlayer = player
        self.playerAnimation = Animation(Resources.getInstance().mPxl, 4, 2, 0.5, self.mCamera.getScaledSize(0.5,0.6))
        
    
    def render(self, delta):
        if self.mPlayer.alive:
            size = b2Vec2(self.mPlayer.size.x, self.mPlayer.size.y)
            
            if self.mPlayer.mBodyDirection == GravityDirection.RIGHT or self.mPlayer.mBodyDirection == GravityDirection.LEFT:
                size.Set(size.y, size.x)
             
            viewpos = self.mCamera.getViewCoords(b2Vec2(self.mPlayer.position.x - size.x/2, self.mPlayer.position.y - size.y/2))
            self.playerAnimation.setSize(self.mCamera.getScaledSize(size.x, size.y))
            
            if self.mPlayer.mPlayerState == PlayerState.IDLE:
                self.playerAnimation.freeze(0)
            elif self.mPlayer.mPlayerState == PlayerState.FALLING:
                self.playerAnimation.freeze(0, 1)
            else:
                self.playerAnimation.gotoRow(0)
                self.playerAnimation.continueAnimation()
    
            self.__flipAndRotate()
            
            self.playerAnimation.draw(delta, viewpos)
            
                
    def __flipAndRotate(self):
        #Down
        if self.mPlayer.mBodyDirection == GravityDirection.DOWN:
            if self.playerAnimation.getRotation() != 0:
                self.playerAnimation.rotate(0)
            
            if self.mPlayer.mFacing == Facing.RIGHT:
                if self.playerAnimation.flippedX() == True:
                    self.playerAnimation.flipX()
            else:
                if self.playerAnimation.flippedX() == False:
                    self.playerAnimation.flipX()
        
        #Up
        if self.mPlayer.mBodyDirection == GravityDirection.UP:
            if self.playerAnimation.getRotation() != 180:
                self.playerAnimation.rotate(180)
            
            if self.mPlayer.mFacing == Facing.RIGHT:
                if self.playerAnimation.flippedX() == False:
                    self.playerAnimation.flipX()
            else:
                if self.playerAnimation.flippedX() == True:
                    self.playerAnimation.flipX()
        
        #Left
        if self.mPlayer.mBodyDirection == GravityDirection.LEFT:
            if self.playerAnimation.getRotation() != -90:
                self.playerAnimation.rotate(-90)
            
            if self.mPlayer.mFacing == Facing.RIGHT:
                if self.playerAnimation.flippedX() == True:
                    self.playerAnimation.flipX()
            else:
                if self.playerAnimation.flippedX() == False:
                    self.playerAnimation.flipX()
        
        #Right
        if self.mPlayer.mBodyDirection == GravityDirection.RIGHT:
            if self.playerAnimation.getRotation() != 90:
                self.playerAnimation.rotate(90)
            
            if self.mPlayer.mFacing == Facing.RIGHT:
                if self.playerAnimation.flippedX() == True:
                    self.playerAnimation.flipX()
            else:
                if self.playerAnimation.flippedX() == False:
                    self.playerAnimation.flipX()
