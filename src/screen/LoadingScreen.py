"""
LoadingScreen, initialize the gameresources such as graphics and sounds

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.SoundManager import SoundManager
from screen.MenuScreen import MenuScreen
from Resources import Resources

class LoadingScreen(object):

    loadingTime = 1

    def __init__(self, game):
        self.mGame = game
        Resources.getInstance().loadGameResources()
        SoundManager.getInstance().initialize()

    def update(self, delta):
        self.loadingTime = self.loadingTime - delta
        self.mGame.setScreen(MenuScreen(self.mGame))

    def render(self, delta):
        pass
