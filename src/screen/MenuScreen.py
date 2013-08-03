from Resources import *
from libs.Pgl import *
from model.Camera import Camera
from controller.MenuInput import MenuInput
from Box2D import b2Vec2
from MenuItems import TableCreator, MenuAction
from libs.Animation import Animation
import LevelScreen, libs.Sprite as Sprite, OptionScreen, InstructionScreen
from libs.SoundManager import SoundManager, MusicID

class MenuScreen(object):
    
    def __init__(self, game):
        SoundManager.getInstance().playMenuMusic()
        pygame.mouse.set_visible(False)
        self.mGame = game
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.screenFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 3.0)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 3.0)
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        self.mButtonTable = TableCreator(self.modelsize, 1, 4, ["new game", "options", "instructions", "exit"], [MenuAction.NEWGAME, MenuAction.OPTIONS, MenuAction.INSTRUCTIONS, MenuAction.EXIT])
        
        self.arrow = Sprite.Sprite(Resources.getInstance().mArrow) 
        self.arrow.setSize(self.mCamera.getScaledSize((self.arrow.getWidth()/float(self.arrow.getHeight())) * 0.5, 0.5))
        
        self.button = Animation(Resources.getInstance().mMenuButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1))
        self.mGame.input = MenuInput(self)

    
    def update(self, delta):            
        pos = self.mGame.input.getMousePosition()
        self.arrow.setPosition(pos[0], pos[1])
        self.mouseOver(pos)
    
    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        
        #title
        title = self.titleFont.render("pxlgrvty", 0, (255,255,255))
        size = self.titleFont.size("pxlgrvty")
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))
        
        #buttons
        self.button.setSize(self.mCamera.getScaledSize(self.mButtonTable.mButtonSize.x, self.mButtonTable.mButtonSize.y))
        for btn in self.mButtonTable.mButtons:
            viewpos = self.mCamera.getViewCoords(b2Vec2(btn.x, btn.y))
            
            color = None
            if btn.mActive:
                self.button.freeze(1, 0)
                color = (255,255,255)
            else:
                self.button.freeze(0, 0)
                color = (141,60,1)
            self.button.draw(delta, viewpos)
        
            btntxt = self.screenFont.render(str(btn.mText), 0, color)
            size = self.screenFont.size(str(btn.mText))
            txtpos = self.mCamera.getViewCoords(b2Vec2(btn.x + btn.size.x / 2 - (size[0] / self.mCamera.scale.x) / 2.0, btn.y + btn.size.y / 2 - (size[1] / self.mCamera.scale.y) / 2.0))
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
                
    def quickRetry(self):
        pass
            
    def quickGame(self):
        self.mGame.setScreen(LevelScreen.LevelScreen(self.mGame))