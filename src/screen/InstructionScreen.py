from libs.Animation import Animation
from libs.Sprite import Sprite
from Resources import Resources
from libs.Pgl import *
from model.Camera import Camera
from Box2D import b2Vec2
from controller.MenuInput import MenuInput
from MenuItems import Button, MenuAction
import pygame, MenuScreen
from BaseMenuScreen import BaseMenuScreen

class InstructionScreen(BaseMenuScreen):
    
    #crystal
    __crystalPos = None
    __crystalTimer = None
    __crystalDirection = None
    __crystalBlingTimer = None
    
    #player walking
    __walkPos = None
    __walkTimer = None
    __walkDirection = None
    
    #player jumping
    __jumpPos = None
    __jumpWaitTimer = None
    __jumpDirection = None
    
    #player gravity
    __gravityPos = None
    __gravityTimer = None
    __gravityDirection = None
    
    def __init__(self, game):
        super(InstructionScreen, self).__init__(game)   
        self.__mMenuItems = []
        self.__mMenuItems.append(Button("back", 0.5, 8.5, b2Vec2(2,1), MenuAction.BACK))
            
        self.__crystalPos = b2Vec2(9.5,5.8)
        self.__crystalDirection = b2Vec2(0,1)
        self.__crystalBlingTimer = 4.0
        self.__crystalTimer = 1.0
        self.crystal = Animation(Resources.getInstance().mCrystal, 5, 1, 0.6, self.mCamera.getScaledSize(0.6,0.6), False, True)
        
        self.portal = Animation(Resources.getInstance().mSwirlSheet, 3, 2, 0.6, self.mCamera.getScaledSize(1.5,1.5), False, True)
        
        self.__walkPos = b2Vec2(1,3)
        self.__walkTimer = 2.0
        self.__walkDirection = b2Vec2(1,0)
        self.playerWalk = Animation(Resources.getInstance().mPxl, 4, 2, 0.4, self.mCamera.getScaledSize(0.9, 1), True, True)
        
        self.__jumpPos = b2Vec2(9.5,3)
        self.__jumpStartPos = self.__jumpPos.copy()
        self.__jumpTimer = 0.5
        self.__jumpWaitTimer = 0.2
        self.__jumpDirection = b2Vec2(0,-1)
        self.playerjump = Animation(Resources.getInstance().mPxl, 4, 2, 0.4, self.mCamera.getScaledSize(0.9, 1), False, False)
        
        self.__gravityPos = b2Vec2(3, 6)
        self.__gravityTimer = 1.0
        self.__gravityDirection = b2Vec2(0,-1)
        self.playergravity = Animation(Resources.getInstance().mPxl, 4, 2, 0.4, self.mCamera.getScaledSize(.9, 1), False, False)
    
    def mouseClick(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.__mMenuItems:
            if btn.rect.collidepoint(mmp):
                if btn.mAction == MenuAction.BACK:
                    self.mGame.setScreen(MenuScreen.MenuScreen(self.mGame))
    
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.__mMenuItems:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                btn.mActive = True
                
    def keyInput(self, key):
        pass
    
    def update(self, delta):
        BaseMenuScreen.update(self, delta)
        
        #crystal
        self.__crystalTimer -= delta    
        if self.__crystalTimer < 0:
            self.__crystalTimer = 1.0
            self.__crystalDirection *= -1
            
        self.__crystalPos.y = self.__crystalPos.copy().y + (self.__crystalDirection.y * 0.01 / 2)
    
        if self.crystal.isAnimationDone():
            self.__crystalBlingTimer -= delta
            if self.__crystalBlingTimer < 0:
                self.__crystalBlingTimer = 4.0
                self.crystal.reset()
        
        #portal
        if self.portal.isAnimationDone():
            self.portal.gotoRow(1)
            self.portal.continueAnimation()
        
   
        #playerwalk
        self.__walkTimer -= delta
        if self.__walkTimer < 0:
            self.__walkTimer = 2.0
            self.__walkDirection *= -1
            self.playerWalk.flipX()
                
        self.__walkPos.x = self.__walkPos.copy().x + (self.__walkDirection.x * 0.03)
        
        #playerjump
        if self.__jumpWaitTimer > 0:
            self.__jumpWaitTimer -= delta
            self.playerjump.freeze(0, 0)
        else:
            self.playerjump.freeze(0,1)
            self.__jumpPos.y = self.__jumpPos.copy().y + (self.__jumpDirection.y * 0.05)
            
            if self.__jumpPos.y <= self.__jumpStartPos.y - 0.8:
                self.__jumpDirection.Set(0,1)
            
            if self.__jumpPos.y > self.__jumpStartPos.y:
                self.__jumpWaitTimer = 0.4
                self.__jumpPos = self.__jumpStartPos.copy()
                self.__jumpDirection *= -1
                
        #playergravity
        if self.__gravityTimer > 0:
            self.__gravityTimer -= delta
            self.playergravity.freeze(0,0)
        else:
            self.playergravity.freeze(0,1)
            if self.__gravityDirection.y < 0:  
                self.playergravity.rotate(180)
                if self.playergravity.flippedX() == False:
                    self.playergravity.flipX()
            elif self.__gravityDirection.y > 0:
                if self.playergravity.flippedX():
                    self.playergravity.flipX()
                self.playergravity.rotate(0)
            
            self.__gravityPos.y = self.__gravityPos.copy().y + (self.__gravityDirection.y * 0.05)
            
            if self.__gravityPos.y <= 4.3:
                self.__gravityDirection.Set(0,1)
                self.__gravityTimer = 1.0
            
            if self.__gravityPos.y > 6:
                self.__gravityPos.y = 6
                self.__gravityDirection.Set(0,-1)
                self.__gravityTimer = 1.0
                
    
        
    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        
        btnToDraw = self.menubutton
        for btn in self.__mMenuItems:
            viewpos = self.mCamera.getViewCoords(b2Vec2(btn.x, btn.y))
            btnToDraw.setSize(self.mCamera.getScaledSize(btn.size.x, btn.size.y))
            
            color = None
            if btn.mActive:
                btnToDraw.freeze(1, 0)
                color = (255,255,255)
            else:
                btnToDraw.freeze(0, 0)
                color = (141,60,1)
                
            btnToDraw.draw(delta, viewpos)
                   
            btntxt = self.screenFont.render(str(btn.mText), 0, color)
            size = self.screenFont.size(str(btn.mText))
            txtpos = self.mCamera.getViewCoords(b2Vec2(btn.x + btn.size.x / 2 - (size[0] / self.mCamera.scale.x) / 2.0, btn.y + btn.size.y / 2 - (size[1] / self.mCamera.scale.y) / 2.0))
            Pgl.app.surface.blit(btntxt, (txtpos.x, txtpos.y))
            

        title = self.titleFont.render("instructions", 0, (255,255,255))
        size = self.titleFont.size("instructions")
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))

        self.crystal.draw(delta, self.mCamera.getViewCoords(self.__crystalPos))
        crystalinfo = Resources.getInstance().getScaledFont(self.mCamera.scale.x).render("=", 0, (255,255,255))
        Pgl.app.surface.blit(crystalinfo, self.mCamera.getViewCoords(b2Vec2(11, 5.8)))
        
        self.portal.draw(delta, self.mCamera.getViewCoords(b2Vec2(12.5, 5.3)))
        portalinfo = self.infoFont.render("collect crystals to open portals", 0, (255,255,255))
        Pgl.app.surface.blit(portalinfo, self.mCamera.getViewCoords(b2Vec2(8,7)))

        self.playerWalk.draw(delta, self.mCamera.getViewCoords(self.__walkPos))
        moveinfo = self.infoFont.render("w,a,s,d - to move around!", 0, (255,255,255))
        Pgl.app.surface.blit(moveinfo, self.mCamera.getViewCoords(b2Vec2(1,4)))
        
        self.playerjump.draw(delta, self.mCamera.getViewCoords(self.__jumpPos))
        jumpinfo = self.infoFont.render("spacebar to jump!", 0, (255,255,255))
        Pgl.app.surface.blit(jumpinfo, self.mCamera.getViewCoords(b2Vec2(8,4)))
        
        self.playergravity.draw(delta, self.mCamera.getViewCoords(self.__gravityPos))
        gravinfo = self.infoFont.render("arrowkeys to shift gravity!", 0, (255,255,255))
        Pgl.app.surface.blit(gravinfo, self.mCamera.getViewCoords(b2Vec2(1,7)))
        
        self.arrow.draw()
        