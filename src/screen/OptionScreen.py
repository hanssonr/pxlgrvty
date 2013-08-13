from Resources import *
from libs.Pgl import *
from model.Camera import Camera
from controller.MenuInput import MenuInput
from Box2D import b2Vec2
from MenuItems import Button, CheckButton, MenuAction, CheckbuttonAction, ListCreator, ListItem, ListItemAction, Volume, VolumeAction, Label
from libs.Animation import Animation
import LevelScreen, libs.Sprite as Sprite, pygame, MenuScreen, json
from libs.SoundManager import SoundManager, SoundID
from BaseMenuScreen import BaseMenuScreen

class OptionScreen(BaseMenuScreen):
    
    def __init__(self, game):
        super(OptionScreen, self).__init__(game)
       
        self.mMenuItems = []
        self.mMenuItems.append(Button("back", 0.5, 8.5, b2Vec2(2,1), MenuAction.BACK))
        self.mMenuItems.append(Button("apply", 13.5, 8.5, b2Vec2(2,1), MenuAction.APPLY))
        self.mMenuItems.append(Button("defaults", 11, 8.5, b2Vec2(2,1), MenuAction.DEFAULTS))
        
        self.mMenuItems.append(CheckButton("fullscreen on/off", 7, 3.5, b2Vec2(0.5,0.5), CheckbuttonAction.FULLSCREEN, Pgl.options.fullscreen))
        self.mMenuItems.append(CheckButton("music on/off", 7, 4, b2Vec2(0.5,0.5), CheckbuttonAction.MUSIC, Pgl.options.music))
        self.mMenuItems.append(CheckButton("sound on/off", 7, 4.5, b2Vec2(0.5,0.5), CheckbuttonAction.SOUND, Pgl.options.sound))
        
        self.mResolutionList = ListCreator(2, 8, 3.5, b2Vec2(3,0.5), self.__getResolutionList(), Pgl.options.resolution)
        self.mMusicVolume = Volume("Music volume:", 5, 7, [["-", VolumeAction.MUSIC_VOLUME_DOWN], ["+", VolumeAction.MUSIC_VOLUME_UP]], Pgl.options.musicvolume)
        self.mSoundVolume = Volume("Sound volume:", 8, 7, [["-", VolumeAction.SOUND_VOLUME_DOWN], ["+", VolumeAction.SOUND_VOLUME_UP]], Pgl.options.soundvolume)
        self.mMenuItems.extend(self.mMusicVolume.mVolumeItems)
        self.mMenuItems.extend(self.mSoundVolume.mVolumeItems)
        self.mMenuItems.extend(self.mResolutionList.mListItem)
        
        #title
        self.title = self.titleFont.render("options", 0, (255,255,255))
        self.size = self.titleFont.size("options")
        self.titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
 
    
    def __getResolutionList(self):
        return ["%sx%s" % (x[0], x[1]) for x in pygame.display.list_modes()]
    
    def update(self, delta):
        BaseMenuScreen.update(self, delta)       
    
    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        
        Pgl.app.surface.blit(self.title, (self.titlepos.x - self.size[0] / 2.0, self.titlepos.y - self.size[1] / 2.0))
        
        #menuitems
        for mi in self.mMenuItems:
            viewpos = self.mCamera.getViewCoords(b2Vec2(mi.x, mi.y))
            color = None
            txtsize = self.screenFont.size(str(mi.mText))
            iDraw = self.menubutton
            if isinstance(mi, Button):
                color = (255,255,255) if mi.mActive else (141,60,1)
                txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x + mi.size.x / 2 - (txtsize[0] / self.mCamera.scale.x) / 2.0, mi.y + mi.size.y / 2 - (txtsize[1] / self.mCamera.scale.y) / 2.0))
            elif isinstance(mi, CheckButton):
                color = (255,255,255) if mi.mActive else (150,150,150)
                iDraw = self.checkbutton
                txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x - mi.size.x / 2 - (txtsize[0] / self.mCamera.scale.x), mi.y + mi.size.y / 2 - (txtsize[1] / self.mCamera.scale.y) / 2.0))
            elif isinstance(mi, ListItem):
                if self.mResolutionList.isInViewRect(mi):
                    color = (255,255,255) if mi.mActive else (141,60,1)
                    txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x + mi.size.x / 2 - (txtsize[0] / self.mCamera.scale.x) / 2.0, mi.y + mi.size.y / 2 - (txtsize[1] / self.mCamera.scale.y) / 2.0))
                else:
                    continue
            elif isinstance(mi, Label):
                color = (255,255,255)
                txtpos = self.mCamera.getViewCoords(b2Vec2(mi.x, mi.y - (txtsize[1] / self.mCamera.scale.y) / 2.0))
            
            if not isinstance(mi,Label):
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
        Pgl.app.changeResolution(Pgl.options.fullscreen, Pgl.options.getResolutionAsList())
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
                    elif mi.mAction == CheckbuttonAction.MUSIC:
                        mi.mActive = not mi.mActive
                        Pgl.options.music = mi.mActive
                        SoundManager.getInstance().pauseMusic(not mi.mActive)
                    elif mi.mAction == CheckbuttonAction.SOUND:
                        mi.mActive = not mi.mActive
                        Pgl.options.sound = mi.mActive
                    elif mi.mAction == VolumeAction.MUSIC_VOLUME_UP:
                        self.mMusicVolume.higher()
                        Pgl.options.musicvolume = self.mMusicVolume.amount
                        SoundManager.getInstance().changeMusicVolume()
                    elif mi.mAction == VolumeAction.MUSIC_VOLUME_DOWN:
                        self.mMusicVolume.lower()
                        Pgl.options.musicvolume = self.mMusicVolume.amount
                        SoundManager.getInstance().changeMusicVolume()
                    elif mi.mAction == VolumeAction.SOUND_VOLUME_UP:
                        self.mSoundVolume.higher()
                        Pgl.options.soundvolume = self.mSoundVolume.amount
                        SoundManager.getInstance().playSound(SoundID.JUMP)
                    elif mi.mAction == VolumeAction.SOUND_VOLUME_DOWN:
                        self.mSoundVolume.lower()
                        Pgl.options.soundvolume = self.mSoundVolume.amount
                        SoundManager.getInstance().playSound(SoundID.JUMP)
                    elif mi.mAction == ListItemAction.ACTION:
                        for listItem in self.mMenuItems:
                            if isinstance(listItem, ListItem):
                                listItem.mActive = False
                        mi.mActive = True
                        Pgl.options.resolution = mi.mText
                    elif mi.mAction == ListItemAction.UP:
                        self.mResolutionList.scrollUp()
                    elif mi.mAction == ListItemAction.DOWN:
                        self.mResolutionList.scrollDown()
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
    
    