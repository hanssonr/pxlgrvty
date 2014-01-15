"""
Floatrectangle class, creates rectangles out of float instead of intergers for more precision
Mainly used for buttons in menus

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

class RectF(object):
    
    def __str__(self):
        return "%.2f, %.2f, %.2f, %.2f" % (self.mX, self.mY, self.mW, self.mH)
    
    def __init__(self, x, y, width, height):
        self.mX = x
        self.mY = y
        self.mW = width
        self.mH = height
        
    
    def collidepoint(self, pos):
        return True if (pos.x > self.x and pos.x < self.x + self.w and
                pos.y > self.y and pos.y < self.y + self.h) else False 
                
    
    def __getX(self):
        return self.mX
    
    def __setX(self, aX):
        self.mX = aX
        
    def __getY(self):
        return self.mY
    
    def __setY(self, aX):
        self.mY = aX

    def __getW(self):
        return self.mW
    
    def __setW(self, aW):
        self.mW = aW
        
    def __getH(self):
        return self.mH
    
    def __setH(self, aH):
        self.mH = aH
    
    x = property(__getX, __setX)
    y = property(__getY, __setY)
    w = property(__getW, __setW)
    h = property(__getH, __setH)