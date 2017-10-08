"""
OptionsScreen shows of the different things users can change in the game

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.Pgl import *
from Box2D import b2Vec2
from screen.MenuItems import Button, CheckButton, ListCreator, ListItem, Volume, Label, ChoiceWidget
import pygame, screen.MenuScreen
from libs.SoundManager import SoundManager, SoundID
from libs.Options import Updaterate
from screen.BaseMenuScreen import BaseMenuScreen

class OptionScreen(BaseMenuScreen):

    def __init__(self, game):
        super(OptionScreen, self).__init__(game)

        self.mMenuItems = []
        self.mMenuItems.append(Button("back", 0.5, 8.5, b2Vec2(2,1), lambda:self.goBack()))
        self.mMenuItems.append(Button("apply", 13.5, 8.5, b2Vec2(2,1), lambda:self.__applyOptions()))
        self.mMenuItems.append(Button("defaults", 11, 8.5, b2Vec2(2,1), lambda:self.__defaultOptions()))

        self.mMenuItems.append(CheckButton("fullscreen on/off", 7, 3.5, b2Vec2(0.5,0.5), Pgl.options.fullscreen, lambda x: Pgl.options.setFullscreen(x)))
        self.mMenuItems.append(CheckButton("music on/off", 7, 4, b2Vec2(0.5,0.5), Pgl.options.music, lambda x: Pgl.options.setMusic(x), [lambda x: SoundManager.getInstance().pauseMusic(x)]))
        self.mMenuItems.append(CheckButton("sound on/off", 7, 4.5, b2Vec2(0.5,0.5), Pgl.options.sound, lambda x: Pgl.options.setSound(x)))

        self.mResolutionList = ListCreator(2, 8, 3.5, b2Vec2(3,0.5), self.__getResolutionList(), Pgl.options.resolution)

        self.mUpdaterate = ChoiceWidget("updaterate:", 4, 6.5, [Updaterate.SLOW, Updaterate.MEDIUM, Updaterate.FAST],
                                         Updaterate.convertSpeedToInt(Pgl.options.updaterate),
                                         lambda x: Pgl.options.setUpdaterate(Updaterate.convertIntToSpeed(x)))

        self.mMusicVolume = Volume("Music volume:", 7, 6.5, Pgl.options.musicvolume, lambda x: Pgl.options.setMusicVolume(x), [lambda:SoundManager.getInstance().changeMusicVolume()])
        self.mSoundVolume = Volume("Sound volume:", 10, 6.5, Pgl.options.soundvolume, lambda x: Pgl.options.setSoundVolume(x), [lambda:SoundManager.getInstance().playSound(SoundID.JUMP)])

        self.mMenuItems.extend(self.mMusicVolume.mVolumeItems)
        self.mMenuItems.extend(self.mSoundVolume.mVolumeItems)
        self.mMenuItems.extend(self.mResolutionList.mListItem)
        self.mMenuItems.extend(self.mUpdaterate.mWidgedItems)

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

    def __defaultOptions(self):
        Pgl.options.setDefaultOptions()
        self.__applyOptions()

    def __fullscreen(self, mi):
        mi.mActive = not mi.mActive
        Pgl.options.fullscreen = mi.mActive

    def mouseClick(self, pos):
            mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))

            for mi in self.mMenuItems:
                if mi.rect.collidepoint(mmp):
                    mi.mAction()

    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))

        for mi in self.mMenuItems:
            if isinstance(mi, Button):
                mi.mActive = False
                if mi.rect.collidepoint(mmp):
                    mi.mActive = True

    def keyInput(self, key):
        pass

    def goBack(self):
        self.mGame.setScreen(screen.MenuScreen.MenuScreen(self.mGame))

class Option(object):
    FULLSCREEN = 0
    MUSIC = 1
    SOUND = 2
    RESOLUTION = 3
