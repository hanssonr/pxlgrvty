"""
Core class of the game. Instantiates pygame with a surface and runs the gameloop
also handles the fullscreen changing and updaterate timing

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

import pygame
from libs.Options import Options
from Pgl import *

class PygameApplication(object):
    
    __mWidth = None
    __mHeight = None
    __mRunning = False
    __mSurface = None
    __mGame = None
    __mTimestep = None
    __mFps = None
    __mUpdaterate = None
    
    def __init__(self, game):        
        self.__mGame = game
        
        Pgl.app = self
        Pgl.options = Options()
        self.changeResolution(Pgl.options.fullscreen, Pgl.options.getResolutionAsList())
        
        self.__mUpdaterate = Pgl.options.updaterate
        self.__mRunning = True
        self.__mainloop()
    
    def __mainloop(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        pygame.display.set_caption("pxlgrvty")
        
        Pgl.clock = pygame.time.Clock()
        self.__mGame.create()
        
        
        while self.__mRunning:
            #Pgl.options.updaterate
            delta = Pgl.clock.tick(60) / 1000.0

            if self.__mGame.input != None:
                self.__mGame.input.update()   
                            
            self.__mGame.update(delta)
            self.__mGame.render(delta)

            pygame.display.flip()
        pygame.quit()
    
    def stop(self):
        self.__mRunning = False
        
    def setUpdaterate(self, rate):
        self.__mUpdaterate = rate
    
    def changeResolution(self, fullscreen, resolution):
        try:
            if fullscreen:
                self.__mSurface = pygame.display.set_mode((resolution[0], resolution[1]), pygame.FULLSCREEN)
            else: 
                self.__mSurface = pygame.display.set_mode((resolution[0], resolution[1]))
        except:
            Pgl.options.setDefaultOptions()
            res = Pgl.options.getResolutionAsList()
            self.__mSurface = pygame.display.set_mode((res[0], res[1]))
            Pgl.width, Pgl.height = res[0], res[1]
        else:
            Pgl.width, Pgl.height = resolution[0], resolution[1]
            
    surface = property(lambda self: self.__mSurface)
    
    
    
    
