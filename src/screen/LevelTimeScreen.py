from controller.MenuInput import MenuInput
from model.Camera import Camera
from libs.Pgl import *
import pygame, LevelScreen, json, GameScreen, model.Level as Level, EndScreen
from Box2D import b2Vec2
from Resources import Resources
from libs.Sprite import Sprite
from libs.Animation import Animation
from MenuItems import MenuAction, Button
from model.Time import Time
from libs.Crypt import Crypt
from libs.Id import Id

class LevelTimeScreen(object):
    
    def __init__(self, game, levelInt, currentTime = None):
        Id.getInstance().resetId()
        self.__mCrypt = Crypt()
        self.mCurrentTime = currentTime
        pygame.mouse.set_visible(False)
        self.mGame = game
        self.mCamera = Camera(Pgl.width, Pgl.height)
        self.modelsize = self.mCamera.getModelCoords(b2Vec2(Pgl.width, Pgl.height))
        self.mLevelInt = levelInt
        self.mButtons = []
        
        self.screenFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 3)
        self.timeFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x / 2)
        self.titleFont = Resources.getInstance().getScaledFont(self.mCamera.scale.x * 2.0)
        
        self.menubutton = Animation(Resources.getInstance().mMenuButton, 2, 1, 0, self.mCamera.getScaledSize(1, 1), False)
        self.arrow = Sprite(Resources.getInstance().mArrow) 
        self.arrow.setSize(self.mCamera.getScaledSize((self.arrow.getWidth()/float(self.arrow.getHeight())) * 0.5, 0.5))
        
        self.medallions = Animation(Resources.getInstance().mMedallions, 3, 3, 0, self.mCamera.getScaledSize(1, 1), False, False)
        
        self.mTime = Time(self.__readPlayerTime())
        
        if currentTime != None:
            self.__initializeFromGame()
        else:
            self.__initializeFromMenu()
              
        self.mLevelTimes = [Time(x) for x in self.__readLevelTimes()]
        self.mButtons.append(Button("back", 0.5, 8.5, b2Vec2(2,1), MenuAction.BACK))
        
        self.achivedMedallion = self.__calculateMedallion()
        self.mGame.input = MenuInput(self)
    
    def __initializeFromMenu(self):
        self.mButtons.append(Button("play", 13.5, 8.5, b2Vec2(2,1), MenuAction.NEWGAME))
    
    def __initializeFromGame(self):
        if self.mLevelInt < Level.Level.countLevels():
            self.mButtons.append(Button("next", 13.5, 8.5, b2Vec2(2,1), MenuAction.NEWGAME))
        else:
            self.mButtons.append(Button("end", 13.5, 8.5, b2Vec2(2,1), MenuAction.EXIT))
            
        self.mButtons.append(Button("retry", 11, 8.5, b2Vec2(2,1), MenuAction.RETRY))
        
        if self.mCurrentTime.isFaster(self.mTime):
            self.mTime = self.mCurrentTime
            found = False
            
            #check if level is in time.json
            data = None
            try:
                with open("assets/state/time.json", "rb") as readstate:
                    decryptedData = self.__mCrypt.decrypt(readstate.read())
                    data = json.loads(decryptedData)
                    
                    #leta efter tiden, finns den uppdatera
                    for time in data:
                        if time["ID"] == str(self.mLevelInt):
                            found = True
                            time["TIME"] = self.mCurrentTime.toString()
                            
                    if not found:
                        data.append({"ID":"%s" % str(self.mLevelInt), "TIME":"%s" % self.mCurrentTime.toString()})
            except Exception, e:
                print str(e)
                pass

            if data == None:
                data = '[{"ID":"%s", "TIME":"%s"}]' % (str(self.mLevelInt), self.mCurrentTime.toString())
            #update the file
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
        except Exception, e:
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
            
            timetxt = self.timeFont.render(self.mLevelTimes[x].toString(), 0 , (255,255,255))
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
                    if self.mCurrentTime != None:
                        self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt+1))
                    else:
                        self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
                elif btn.mAction == MenuAction.RETRY:
                    self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
                elif btn.mAction == MenuAction.EXIT:
                    self.mGame.setScreen(EndScreen.EndScreen(self.mGame))
                break
        
    def mouseOver(self, pos):
        mmp = self.mCamera.getModelCoords(b2Vec2(pos[0], pos[1]))
        
        for btn in self.mButtons:
            btn.mActive = False
            if btn.rect.collidepoint(mmp):
                btn.mActive = True
                
    def quickRetry(self):
        if self.mCurrentTime != None:
            self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
            
    def quickGame(self):
        if self.mLevelInt < Level.Level.countLevels():
            if self.mCurrentTime != None:
                self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt+1))
            else:
                self.mGame.setScreen(GameScreen.GameScreen(self.mGame, self.mLevelInt))
        else:
            self.mGame.setScreen(EndScreen.EndScreen(self.mGame))