from controller.MenuInput import MenuInput
from model.Camera import Camera
from libs.Pgl import *
import pygame, LevelScreen, json, ConfigParser, GameScreen
from Box2D import b2Vec2
from Resources import Resources
from libs.Sprite import Sprite
from libs.Animation import Animation
from MenuItems import MenuAction, Button
from model.Time import Time

class LevelTimeScreen(object):
    
    def __init__(self, game, levelInt):
        pygame.mouse.set_visible(False)
        self.mGame = game
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        self.mLevelInt = levelInt
        self.mButtons = []
        
        self.screenFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 2)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)
        
        self.menubutton = Animation(Resources.getInstance().mMenuButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False)
        self.arrow = Sprite(Resources.getInstance().mArrow) 
        self.arrow.setSize(self.mCamera.getScaledSize((self.arrow.getWidth()/float(self.arrow.getHeight())) * 0.5, 0.5))
        
        self.medallions = Animation(Resources.getInstance().mMedallions, 3, 3, 0, self.mCamera.getScaledSize(1, 1), False, False)

        self.mButtons.append(Button("back", 0.5, 8.5, b2Vec2(2,1), MenuAction.BACK))
        self.mButtons.append(Button("play", 13.5, 8.5, b2Vec2(2,1), MenuAction.NEWGAME))
        
        self.mTime = Time(self.__readPlayerTime())
        self.mLevelTimes = [Time(x) for x in self.__readLevelTimes()]
        
        self.achivedMedallion = self.__calculateMedallion()
        
        self.mGame.input = MenuInput(self)
    
    def __calculateMedallion(self):
        if self.mLevelTimes[0].compareTimes(self.mTime):
            return b2Vec2(0,0)
        elif self.mLevelTimes[1].compareTimes(self.mTime):
            return b2Vec2(1,0)
        elif self.mLevelTimes[2].compareTimes(self.mTime):
            return b2Vec2(2,0)
        else:
            return b2Vec2(0,2)
    
    def __readPlayerTime(self):
        pTime = None
        
        try:
            with open("assets/state/time.json", "r") as readstate:
                pTime = json.load(readstate)
                
            return pTime[str(self.mLevelInt)]["TIME"]
        except:
            pTime = "00:00:00"
        
        return pTime
    
    def __readLevelTimes(self):
        times = []
        parser = ConfigParser.ConfigParser()
        parser.read("assets/Levels/level%d.lvl" % self.mLevelInt)
        times.append(parser.get("time", "gold"))
        times.append(parser.get("time", "silver"))
        times.append(parser.get("time", "bronze"))
        return times
    
    def update(self, delta):
        pos = pygame.mouse.get_pos()
        self.arrow.setPosition(pos[0], pos[1])
        self.mouseOver(pos)
    
    def render(self, delta):
        #Pgl.app.surface.fill((167,74,20))
        Pgl.app.surface.fill((67,80,129))
        
        #header
        title = self.titleFont.render("level %s" % str(self.mLevelInt), 0, (255,255,255))
        size = self.titleFont.size("level %s" % str(self.mLevelInt))
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))
        
        #besttime
        best = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).render("Best time:", 0, (255, 255, 255))
        bestsize = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).size("Best time:")
        time = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).render(self.mTime.toString(), 0, (255,74,20))
        bestpos = self.mCamera.getViewCoords(b2Vec2(5, 3.5))
        timepos = self.mCamera.getViewCoords(b2Vec2(5.5, 3.5))
        Pgl.app.surface.blit(best, bestpos)
        Pgl.app.surface.blit(time, (timepos.x + bestsize[0], timepos.y))
        
        btnToDraw = self.menubutton
        for btn in self.mButtons:
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
        
        
        for x in range(len(self.mLevelTimes)):
            self.medallions.freeze(x, 1)
            
            timetxt = self.screenFont.render(self.mLevelTimes[x].toString(), 0 , (255,255,255))
            pos = self.mCamera.getViewCoords(b2Vec2(9, 5+x))
            Pgl.app.surface.blit(timetxt, (pos.x, pos.y))
            
            self.medallions.setSize(self.mCamera.getScaledSize(1,1))
            self.medallions.draw(delta, self.mCamera.getViewCoords(b2Vec2(8,4.6+x)))
        
        self.medallions.freeze(self.achivedMedallion.x, self.achivedMedallion.y)
        self.medallions.setSize(self.mCamera.getScaledSize(3,3))
        self.medallions.draw(delta, self.mCamera.getViewCoords(b2Vec2(4.9,4.6)))
        self.arrow.draw()

    def mouseClick(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtons:
            if btn.rect.collidepoint(mmp):
                if btn.mAction == MenuAction.BACK:
                    self.mGame.setScreen(LevelScreen.LevelScreen(self.mGame))
                elif btn.mAction == MenuAction.NEWGAME:
                    self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
                break
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                btn.mActive = True