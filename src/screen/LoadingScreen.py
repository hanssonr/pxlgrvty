"""
LoadingScreen, initialize the gameresources such as graphics and sounds

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Resources import *
from libs.Pgl import *
from libs.SoundManager import SoundManager
from screen.LevelScreen import LevelScreen
from screen.MenuScreen import MenuScreen
from screen.GameScreen import GameScreen
from screen.EndScreen import EndScreen

class LoadingScreen(object):
    
    loadingTime = 1
    
    def __init__(self, game):
        self.mGame = game
        Resources.getInstance().loadGameResources()
        SoundManager.getInstance().initialize()
    
    def update(self, delta):            
        self.loadingTime = self.loadingTime - delta
        #print self.loadingTime
        #if self.loadingTime < 0:
        self.mGame.setScreen(MenuScreen(self.mGame))
        #self.mGame.setScreen(GameScreen(self.mGame, 1))
        #self.mGame.setScreen(EndScreen(self.mGame))
        
    def render(self, delta):
        pass