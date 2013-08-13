import pygame, os, json
from libs.Options import Options
from pygame.locals import *
from Pgl import *

class PygameApplication(object):
    
    width = None
    height = None
    running = False
    surface = None
    game = None
    timestep = None
    
    def __init__(self, game, fps):        
        self.game = game
        self.fps = fps
        self.renderstep = 1.0 / self.fps
        
        Pgl.app = self
        Pgl.options = Options()
        self.changeResolution(Pgl.options.fullscreen, Pgl.options.getResolutionAsList())
        
        self.running = True
        self.__mainloop()
    
    def __mainloop(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        pygame.display.set_caption("pxlgrvty")
        
        Pgl.clock = pygame.time.Clock()
        self.game.create()
        
        rdt = 0
        while self.running:
            dt = Pgl.clock.tick(60) / 1000.0

            rdt += dt
            if self.game.input != None:
                self.game.input.update()   
                                
            self.game.update(dt)
            
            if rdt >= self.renderstep:
                self.game.render(rdt)
                rdt = 0

            pygame.display.flip()
        pygame.quit()
    
    def stop(self):
        self.running = False
        
    def setRenderStep(self, rdt):
        self.renderstep = rdt
    
    def changeResolution(self, fullscreen, resolution):
        try:
            if fullscreen:
                self.surface = pygame.display.set_mode((resolution[0], resolution[1]), FULLSCREEN)
            else: 
                self.surface = pygame.display.set_mode((resolution[0], resolution[1]))
        except:
            Pgl.options.setDefaultOptions()
            res = Pgl.options.getResolutionAsList()
            self.surface = pygame.display.set_mode((res[0], res[1]))
            Pgl.width, Pgl.height = res[0], res[1]
        else:
            Pgl.width, Pgl.height = resolution[0], resolution[1]
