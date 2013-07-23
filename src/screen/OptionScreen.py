from Resources import *
from libs.Pgl import *
from model.Camera import Camera
from controller.MenuInput import MenuInput
from Box2D import b2Vec2
from MenuItems import Button, CheckButton, MenuAction, CheckbuttonAction, ListCreator, ListItem, ListItemAction
from libs.Animation import Animation
import LevelScreen, libs.Sprite as Sprite, pygame, MenuScreen, json

class OptionScreen(object):
    
    def __init__(self, game):
        pygame.mouse.set_visible(False)
        self.mGame = game
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.screenFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 3.0)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        self.mMenuItems = []
        
        self.arrow = Sprite.Sprite(Resources.getInstance().mArrow) 
        self.arrow.setSize(self.mCamera.getScaledSize((self.arrow.getWidth()/float(self.arrow.getHeight())) * 0.5, 0.5))
        
        self.button = Animation(Resources.getInstance().mMenuButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1))
        self.checkbutton = Animation(Resources.getInstance().mCheckButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1))
        
        self.mMenuItems.append(Button("back", 0.5, 8.5, b2Vec2(2,1), MenuAction.BACK))
        self.mMenuItems.append(Button("apply", 13.5, 8.5, b2Vec2(2,1), MenuAction.APPLY))
        self.mMenuItems.append(Button("defaults", 11, 8.5, b2Vec2(2,1), MenuAction.DEFAULTS))
        
        self.mMenuItems.append(CheckButton("fullscreen on/off", 7, 3.5, b2Vec2(0.5,0.5), CheckbuttonAction.FULLSCREEN, Pgl.options.fullscreen))
        self.mMenuItems.append(CheckButton("music on/off", 7, 4, b2Vec2(0.5,0.5), CheckbuttonAction.MUSIC, Pgl.options.music))
        self.mMenuItems.append(CheckButton("sound on/off", 7, 4.5, b2Vec2(0.5,0.5), CheckbuttonAction.SOUND, Pgl.options.sound))
        
        self.mResolutionList = ListCreator(8, 3.5, b2Vec2(3,0.5), self.__getResolutionList())
        self.mMenuItems.extend(self.mResolutionList.mListItem)
        
        self.mGame.input = MenuInput(self)

    def __readOptions(self):
        options = []
        optionData = None
        
        try:
            with open("assets/state/options.json", "r") as readstate:
                optionData = json.load(readstate)
        except (IOError, ValueError):
            with open("assets/state/options.json", "w+") as writestate:
                json.dump({"FULLSCREEN": False, "MUSIC": True, "SOUND": True, "RESOLUTION":"640x480"}, writestate)
            
        finally:
            with open("assets/state/options.json", "r") as readstate:
                optionData = json.load(readstate)
        options.append(optionData["FULLSCREEN"])
        options.append(optionData["MUSIC"])
        options.append(optionData["SOUND"])
        options.append(optionData["RESOLUTION"])
        return options
    
    def __getResolutionList(self):
        for mi in self.mMenuItems:
            if mi.mAction == CheckbuttonAction.FULLSCREEN:
                if mi.mActive:
                    return ["640x480", "800x600", "1440x900", "1920x1080"]
                else:
                    return ["640x400", "800x500", "1280x800", "1680x1050"]
    
    def __writeOptions(self):
        with open("assets/state/options.json", "w+") as state:
                json.dump({"FULLSCREEN":self.options[Option.FULLSCREEN], "MUSIC":self.options[Option.MUSIC], "SOUND":self.options[Option.SOUND], "RESOLUTION":self.options[Option.RESOLUTION]}, state)
    
    def update(self, delta):            
        pos = self.mGame.input.getMousePosition()
        self.arrow.setPosition(pos[0], pos[1])
        self.mouseOver(pos)
    
    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        
        #title
        title = self.titleFont.render("options", 0, (255,255,255))
        size = self.titleFont.size("options")
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))
        
        #menuitems
        for mi in self.mMenuItems:
            viewpos = self.mCamera.getViewCoords(b2Vec2(mi.x, mi.y))
            color = None
            txtsize = self.screenFont.size(str(mi.mText))
            iDraw = self.button
            if isinstance(mi, Button):
                color = (255,255,255) if mi.mActive else (141,60,1)
                txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x + mi.size.x / 2 - (txtsize[0] / self.mCamera.scale.x) / 2.0, mi.y + mi.size.y / 2 - (txtsize[1] / self.mCamera.scale.y) / 2.0))
            elif isinstance(mi, CheckButton):
                color = (255,255,255) if mi.mActive else (150,150,150)
                iDraw = self.checkbutton
                txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x - mi.size.x / 2 - (txtsize[0] / self.mCamera.scale.x), mi.y + mi.size.y / 2 - (txtsize[1] / self.mCamera.scale.y) / 2.0))
            elif isinstance(mi, ListItem):
                color = (255,255,255) if mi.mActive else (150,150,150)
                txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x + mi.size.x / 2 - (txtsize[0] / self.mCamera.scale.x) / 2.0, mi.y + mi.size.y / 2 - (txtsize[1] / self.mCamera.scale.y) / 2.0))
            
            if mi.mActive:
                iDraw.freeze(1, 0)
            else:
                iDraw.freeze(0, 0)
            
            iDraw.setSize(self.mCamera.getScaledSize(mi.size.x, mi.size.y))  
            iDraw.draw(delta, viewpos)
              
            btntxt = self.screenFont.render(str(mi.mText), 0, color)
            Pgl.app.surface.blit(btntxt, (txtpos.x, txtpos.y))
            
        
        self.arrow.draw()
        
    def __applyOptions(self):
        Pgl.app.fullscreen(Pgl.options.fullscreen, Pgl.options.getResolutionAsList())
        #turn on/off sound and music
        Pgl.options.writeOptions()
        self.mGame.setScreen(OptionScreen(self.mGame))
            
    def mouseClick(self, pos):
            mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
            
            for mi in self.mMenuItems:
                if mi.rect.collidepoint(mmp):
                    
                    if mi.mAction == MenuAction.BACK:
                        self.mGame.setScreen(MenuScreen.MenuScreen(self.mGame))
                    elif mi.mAction == MenuAction.APPLY:
                        self.__applyOptions()
                    elif mi.mAction == MenuAction.DEFAULTS:
                        Pgl.options.setDefaultOptions()
                        self.__applyOptions()
                    elif mi.mAction == CheckbuttonAction.FULLSCREEN:
                        mi.mActive = not mi.mActive
                        Pgl.options.fullscreen = mi.mActive
                        
                        toRemove = []
                        for x in self.mMenuItems:
                            if isinstance(x, ListItem):
                                toRemove.append(x)
                        
                        for i in toRemove:
                            self.mMenuItems.remove(i)
                            
                        self.mResolutionList = ListCreator(8, 3.5, b2Vec2(3,0.5), self.__getResolutionList())
                        self.mMenuItems.extend(self.mResolutionList.mListItem)          
                        
                    elif mi.mAction == CheckbuttonAction.MUSIC:
                        mi.mActive = not mi.mActive
                        Pgl.options.music = mi.mActive
                    elif mi.mAction == CheckbuttonAction.SOUND:
                        mi.mActive = not mi.mActive
                        Pgl.options.sound = mi.mActive
                    elif mi.mAction == ListItemAction.ACTION:
                        for listItem in self.mMenuItems:
                            if isinstance(listItem, ListItem):
                                listItem.mActive = False
                        mi.mActive = True
                        Pgl.options.resolution = mi.mText
                    break
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for mi in self.mMenuItems:
            if isinstance(mi, Button):
                mi.mActive = False
                if mi.rect.collidepoint(mmp):
                    mi.mActive = True
                    
class Option(object):
    FULLSCREEN = 0
    MUSIC = 1
    SOUND = 2
    RESOLUTION = 3
    
    