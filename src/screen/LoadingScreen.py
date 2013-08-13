from Resources import *
from libs.Pgl import *
from libs.SoundManager import SoundManager
from screen.LevelScreen import LevelScreen
from screen.MenuScreen import MenuScreen
from screen.GameScreen import GameScreen

class LoadingScreen(object):
    
    loadingTime = 1
    
    def __init__(self, game):
        self.mGame = game
        Resources.getInstance().loadGameResources()
        SoundManager.getInstance().initialize()
        self.label = Resources.getInstance().mFont.render("Loading...", 1, (255,255,255))
    
    def update(self, delta):            
        self.loadingTime = self.loadingTime - delta
        #print self.loadingTime
        #if self.loadingTime < 0:
        self.mGame.setScreen(MenuScreen(self.mGame))
        #self.mGame.setScreen(GameScreen(self.mGame, 7))
        
    def render(self, delta):
        pass