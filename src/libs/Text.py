"""
A text helpclass for displaying multiple lines of text with pygame
Takes a list of texts with color, size, font and spacing

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Box2D import b2Vec2

class Text(object):
    
    def __init__(self, textlist, pos, lineheight, surface):
        self.mTexts = []
        self.mPos = pos
        self.mLineheight = lineheight
        self.mSurface = surface
        
        self.width = 0
        self.height = 0
        
        y = 0
        
        for item in textlist:
            font = item[0]
            color = item[1]
            text = item[2]
            spacing = item[3]
            size = font.size("%s" % text)
            
            if size[0] > self.width: self.width = size[0]
            self.mTexts.append(TextObject(font.render(text, 1, color), b2Vec2(size[0], size[1]), b2Vec2(pos.x, y + spacing)))
            y += item[0].get_linesize() + spacing
            self.height += size[1] + spacing


    def renderleft(self, delta):
        for item in self.mTexts:
            self.mSurface.blit(item.fontrender, (self.mPos.x - self.width / 2.0, self.mPos.y + item.pos.y))
            
    def rendercentered(self, delta):
        for item in self.mTexts:
            self.mSurface.blit(item.fontrender, (item.pos.x - item.size.x / 2.0, self.mPos.y + item.pos.y))
                                                            
                                                            
class TextObject(object):
    
    def __init__(self, fontrender, size, pos):
        self.fontrender = fontrender
        self.size = size
        self.pos = pos