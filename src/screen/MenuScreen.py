from Resources import *
from libs.Pgl import *
from model.Camera import Camera
from controller.MenuInput import MenuInput
from Box2D import b2Vec2
from MenuItems import TableCreator, MenuAction
from libs.Animation import Animation
import LevelScreen, OptionScreen, InstructionScreen
from libs.Sprite import Sprite
from libs.SoundManager import SoundManager, MusicID
from BaseMenuScreen import *

class MenuScreen(BaseMenuScreen):
    
    def __init__(self, game):  
        super(MenuScreen, self).__init__(game)
        self.mButtonTable = TableCreator(self.modelsize, 1, 4, 
                                         ["new game", "options", "instructions", "exit"], 
                                         [MenuAction.NEWGAME, MenuAction.OPTIONS, MenuAction.INSTRUCTIONS, MenuAction.EXIT])
        
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
                    if btn.mAction == MenuAction.NEWGAME:
                        self.mGame.setScreen(LevelScreen.LevelScreen(self.mGame))
                    elif btn.mAction == MenuAction.INSTRUCTIONS:
                        self.mGame.setScreen(InstructionScreen.InstructionScreen(self.mGame))
                    elif btn.mAction == MenuAction.OPTIONS:
                        self.mGame.setScreen(OptionScreen.OptionScreen(self.mGame))
                    elif btn.mAction == MenuAction.EXIT:
                        Pgl.app.stop()
                    break
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtonTable.mButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                btn.mActive = True
                
    def keyInput(self, key):
        pass