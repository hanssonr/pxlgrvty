
class RectF(object):
    
    def __str__(self):
        return "%.2f, %.2f, %.2f, %.2f" % (self.x, self.y, self.w, self.h)
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        
    
    def collidepoint(self, pos):
        return True if (pos.x > self.x and pos.x < self.x + self.w and
                pos.y > self.y and pos.y < self.y + self.h) else False 