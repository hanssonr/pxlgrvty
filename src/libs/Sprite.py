import pygame

class Sprite(object):
    
    def __init__(self, image, size = None):
        self.image = image
        self.pos = image.get_rect()
        
        if size != None:
            self.setSize(size[0], size[1])
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)
    
    def setSize(self, width, height):
        self.image = pygame.transform.scale(self.image,(width, height))
    
    def setPosition(self, x, y):
        self.pos = (x, y)
    
    def setX(self, x):
        pass
    
    def setY(self, y):
        pass
    
    
    
    