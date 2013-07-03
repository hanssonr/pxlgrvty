from Resources import *
from libs.Pgl import *
from screen.GameScreen import GameScreen

class LoadingScreen(object):
    
    loadingTime = 1
    
    def __init__(self, game):
        self.mGame = game
        Resources.getInstance().loadGameResources()
        self.label = Resources.getInstance().mFont.render("Loading...", 1, (255,255,255))
    
    def update(self, delta):            
        self.loadingTime = self.loadingTime - delta
        #print self.loadingTime
        #if self.loadingTime < 0:
        self.mGame.setScreen(GameScreen(self.mGame))
    
    def render(self, delta):
        pass
        #Pgl.app.surface.blit(self.label, (Pgl.width/2,Pgl.height/2))