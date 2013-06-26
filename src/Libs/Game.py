class Game(object):
    
    mScreen = None
    mGame = None
    
    def __init__(self, game):
        self.mGame = game
    
    def update(self, delta):
        if not self.mScreen == None:
            self.mScreen.update(delta)
            
    def render(self, delta):
        if not self.mScreen == None:
            self.mScreen.render(delta)
    
    def setScreen(self, screen):
        self.mScreen = screen
    
    def getScreen(self):
        return self.mScreen