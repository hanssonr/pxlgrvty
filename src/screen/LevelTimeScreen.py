"""
A screen that shows of a levels timecriteria, gets instantiated from either menus or the game

#from Game
shows the current time achieved and updates the time.json if a new record was beaten

#from Menu
shows of timecriterias and medals if achieved before

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.Pgl import *
import pygame, LevelScreen, json, GameScreen, model.Level as Level, EndScreen
from Box2D import b2Vec2
from Resources import Resources
from libs.Animation import Animation
from MenuItems import Button
from model.Time import Time
from libs.Crypt import Crypt
from libs.Id import Id
from BaseMenuScreen import BaseMenuScreen

class LevelTimeScreen(BaseMenuScreen):
    
    def __init__(self, game, levelInt, currentTime = None):
        Id.getInstance().resetId()
        
        self.__mCrypt = Crypt()
        self.mCurrentTime = currentTime
        
        self.mLevelInt = levelInt
        self.mButtons = []
        self.mTime = Time(self.__readPlayerTime())
        
        if currentTime != None:
            super(LevelTimeScreen, self).__init__(game, False)
            self.__initializeFromGame()
        else:
            super(LevelTimeScreen, self).__init__(game)
            self.__initializeFromMenu()
   
        self.medallions = Animation(Resources.getInstance().mMedallions, 3, 3, 0, self.mCamera.getScaledSize(3, 3), False, False)
        self.mLevelTimes = [Time(x) for x in self.__readLevelTimes()]
        self.mButtons.append(Button("back", 0.5, 8.5, b2Vec2(2,1), lambda: self.mGame.setScreen(LevelScreen.LevelScreen(self.mGame))))
        
        self.achivedMedallion = self.__calculateMedallion()
    
    def __initializeFromMenu(self):
        self.mButtons.append(Button("play", 13.5, 8.5, b2Vec2(2,1), lambda: self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))))
    
    def __initializeFromGame(self):
        if self.mLevelInt < Level.Level.countLevels():
            self.mButtons.append(Button("next", 13.5, 8.5, b2Vec2(2,1), lambda: self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt+1))))
        else:
            self.mButtons.append(Button("end", 13.5, 8.5, b2Vec2(2,1), lambda: self.mGame.setScreen(EndScreen.EndScreen(self.mGame))))
            
        self.mButtons.append(Button("retry", 11, 8.5, b2Vec2(2,1), lambda: self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))))
        
        if self.mCurrentTime.isFaster(self.mTime):
            self.mTime = self.mCurrentTime
            found = False
            
            data = None
            try:
                with open("assets/state/time.json", "rb") as readstate:
                    decryptedData = self.__mCrypt.decrypt(readstate.read())
                    data = json.loads(decryptedData)
                    
                    for time in data:
                        if time["ID"] == str(self.mLevelInt):
                            found = True
                            time["TIME"] = self.mCurrentTime.toString()
                            
                    if not found:
                        data.append({"ID":"%s" % str(self.mLevelInt), "TIME":"%s" % self.mCurrentTime.toString()})
            except Exception:
                pass

            if data == None:
                data = '[{"ID":"%s", "TIME":"%s"}]' % (str(self.mLevelInt), self.mCurrentTime.toString())

            with open("assets/state/time.json", "wb+") as writestate:
                writestate.write(self.__mCrypt.encrypt(json.dumps(data)))
        
    
    def __calculateMedallion(self):
        if self.mTime.isFaster(self.mLevelTimes[0]):
            return b2Vec2(0,0)
        elif self.mTime.isFaster(self.mLevelTimes[1]):
            return b2Vec2(1,0)
        elif self.mTime.isFaster(self.mLevelTimes[2]):
            return b2Vec2(2,0)
        else:
            return b2Vec2(0,2)
    
    def __readPlayerTime(self):
        pTime = None
        found = False
        
        try:
            with open("assets/state/time.json", "rb") as state:
                decryptedData = self.__mCrypt.decrypt(state.read())
                pTime = json.loads(decryptedData)
                
            for time in pTime:
                if time["ID"] == str(self.mLevelInt):
                    pTime = time["TIME"]
                    found = True
                    break
        except Exception:
            with open("assets/state/time.json", "wb+") as writer:
                writer.write(self.__mCrypt.encrypt("[]"))

        if not found:
            pTime = "00:00:00"
                   
        return pTime
    
    def __readLevelTimes(self):
        times = []
        parser = self.__mCrypt.dectryptParser(self.mLevelInt)
        times.append(parser.get("time", "gold"))
        times.append(parser.get("time", "silver"))
        times.append(parser.get("time", "bronze"))
        return times
    
    def update(self, delta):
        BaseMenuScreen.update(self, delta)
    
    def render(self, delta):
        Pgl.app.surface.fill((67,80,129))
        
        #header
        title = self.titleFont.render("level %s" % str(self.mLevelInt), 0, (255,255,255))
        size = self.titleFont.size("level %s" % str(self.mLevelInt))
        titlepos = self.mCamera.getViewCoords(b2Vec2(self.modelsize.x / 2.0, self.modelsize.y / 6))
        Pgl.app.surface.blit(title, (titlepos.x - size[0] / 2.0, titlepos.y - size[1] / 2.0))
        
        #current runningtime (if comming from gamescreen)
        if self.mCurrentTime != None:
            current = Resources.getInstance().getScaledFont(self.mCamera.mScale.x / 1.5).render("Current time:", 0, (255, 255, 255))
            currentsize = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).size("Current time:")
            ctime = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).render(self.mCurrentTime.toString(), 0, (255,74,20))
            currentpos = self.mCamera.getViewCoords(b2Vec2(5, 3.3))
            ctimepos = self.mCamera.getViewCoords(b2Vec2(5.5, 3.3))
            Pgl.app.surface.blit(current, currentpos)
            Pgl.app.surface.blit(ctime, (ctimepos.x + currentsize[0], ctimepos.y))
        
        #besttime
        best = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).render("Best time:", 0, (255, 255, 255))
        bestsize = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).size("Best time:")
        time = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 1.5).render(self.mTime.toString(), 0, (255,74,20))
        bestpos = self.mCamera.getViewCoords(b2Vec2(5, 3.8))
        timepos = self.mCamera.getViewCoords(b2Vec2(5.5, 3.8))
        Pgl.app.surface.blit(best, bestpos)
        Pgl.app.surface.blit(time, (timepos.x + bestsize[0], timepos.y))
        
        #buttons
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
        
        #small medallions
        for x in range(len(self.mLevelTimes)):
            self.medallions.freeze(x, 1)
            
            timetxt = self.infoFont.render(self.mLevelTimes[x].toString(), 0 , (255,255,255))
            pos = self.mCamera.getViewCoords(b2Vec2(9, 5+x))
            Pgl.app.surface.blit(timetxt, (pos.x, pos.y))
            
            self.medallions.setSize(self.mCamera.getScaledSize(1,1))
            self.medallions.draw(delta, self.mCamera.getViewCoords(b2Vec2(8,4.6+x)))
        
        self.medallions.freeze(self.achivedMedallion.x, self.achivedMedallion.y)
        self.medallions.setSize(self.mCamera.getScaledSize(3,3))
        self.medallions.draw(delta, self.mCamera.getViewCoords(b2Vec2(4.9,4.6)))
        self.arrow.draw()

    def mouseClick(self, pos):
        xy = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtons:
            if btn.rect.collidepoint(xy):
                btn.mAction()
        
    def mouseOver(self, pos):
        xy = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtons:
            btn.mActive = False
            if btn.rect.collidepoint(xy):
                btn.mActive = True
                
    def keyInput(self, key):
        if key == pygame.K_r:
            self.__quickRetry()
        elif key == pygame.K_SPACE:
            self.__quickGame()
                
    def __quickRetry(self):
        if self.mCurrentTime != None:
            self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
            
    def __quickGame(self):
        if self.mCurrentTime == None:
            self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
        else:
            if self.mLevelInt < Level.Level.countLevels():
                self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt+1))
            else:
                self.mGame.setScreen(EndScreen.EndScreen(self.mGame))