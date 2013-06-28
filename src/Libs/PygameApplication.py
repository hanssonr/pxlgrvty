import pygame
from Pgl import *

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
        Pgl.clock = pygame.time.Clock()
        
        self.game.create()
        while self.running:
            delta = Pgl.clock.tick(self.fps) / 1000.0

            if self.game.input != None:
                self.game.input.update()
                            
            self.game.update(delta)
            self.game.render(delta)
            pygame.display.flip()
                
        pygame.quit()
    
    def stop(self):
        self.running = False
    
    