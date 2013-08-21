"""
MenuScreen shows the first menu in the game with buttons such as instructions, new game, options and exit

Author: Rickard Hansson, rkh.hansson@gmail.com
"""
from Box2D import b2Vec2
from libs.Pgl import *
from screen.BaseMenuScreen import BaseMenuScreen
from MenuItems import TableCreator
import LevelScreen, OptionScreen, InstructionScreen, EndScreen


class MenuScreen(BaseMenuScreen):
    
    def __init__(self, game):  
        super(MenuScreen, self).__init__(game)
        self.mButtonTable = TableCreator(b2Vec2(self.modelsize.x, self.modelsize.y + 2), 1, 5, 
                                         ["new game", "options", "instructions", "credits", "exit"], 
                                         [lambda: self.mGame.setScreen(LevelScreen.LevelScreen(self.mGame)),
                                           lambda: self.mGame.setScreen(OptionScreen.OptionScreen(self.mGame)),
                                           lambda: self.mGame.setScreen(InstructionScreen.InstructionScreen(self.mGame)),
                                           lambda: self.mGame.setScreen(EndScreen.EndScreen(self.mGame)),
                                           lambda: Pgl.app.stop()])
        
        #title
        self.title = self.titleFont.render("pxlgrvty", 0, (255,255,255))
        self.size = self.titleFont.size("pxlgrvty")
        self.titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
    
    def update(self, delta):            
        BaseMenuScreen.update(self, delta)
    
    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        Pgl.app.surface.blit(self.title, (self.titlepos.x - self.size[0] / 2.0, self.titlepos.y - self.size[1] / 2.0))
        
        #buttons
        self.menubutton.setSize(self.mCamera.getScaledSize(self.mButtonTable.mButtonSize.x, self.mButtonTable.mButtonSize.y))
        for btn in self.mButtonTable.mButtons:
            viewpos = self.mCamera.getViewCoords(b2Vec2(btn.x, btn.y))
            
            color = None
            if btn.mActive:
                self.menubutton.freeze(1, 0)
                color = (255,255,255)
            else:
                self.menubutton.freeze(0, 0)
                color = (141,60,1)
            self.menubutton.draw(delta, viewpos)
        
            btntxt = self.screenFont.render(str(btn.mText), 0, color)
            size = self.screenFont.size(str(btn.mText))
            txtpos = self.mCamera.getViewCoords(b2Vec2(btn.x + btn.size.x / 2 - (size[0] / self.mCamera.scale.x) / 2.0, 
                                                       btn.y + btn.size.y / 2 - (size[1] / self.mCamera.scale.y) / 2.0))
            Pgl.app.surface.blit(btntxt, (txtpos.x, txtpos.y))
            
        self.arrow.draw()
            
    def mouseClick(self, pos):
            mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
            
            for btn in self.mButtonTable.mButtons:
                if btn.rect.collidepoint(mmp):
                    btn.mAction()
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtonTable.mButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                btn.mActive = True
                
    def keyInput(self, key):
        pass