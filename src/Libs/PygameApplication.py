import pygame
from Pgl import *
import pygl2d

class PygameApplication(object):
    
    width = None
    height = None
    running = False
    surface = None
    
    game = None
    
    def __init__(self, game, width, height, fps):
        Pgl.app = self
        Pgl.width = width
        Pgl.height = height
        
        self.game = game
        self.width = width
        self.height = height
        self.fps = fps
        
        self.running = True
        self.__mainloop()
        
    
    def __mainloop(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        #pygl2d.window.init([self.width, self.height], caption='pxlgrvty')
        Pgl.clock = pygame.time.Clock()
        
        self.game.create()
        while self.running:
            delta = Pgl.clock.tick(self.fps) / 1000.0

            if self.game.input != None:
                self.game.input.update()
                            
            self.game.update(delta)
            
            #pygl2d.window.begin_draw()
            self.game.render(delta)
            pygame.display.flip()
            #pygl2d.window.end_draw()
                
        pygame.quit()
    
    def stop(self):
        self.running = False
    
    