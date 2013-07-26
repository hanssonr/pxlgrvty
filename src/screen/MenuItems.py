from Box2D import b2Vec2
from libs.RectF import RectF

class TableCreator(object):
    mButtons = None
    mButtonSize = None
    
    def __init__(self, modelsize, buttonPerColumn, nrOfButtons, texts, actions):
        self.mButtons = []
        self.mButtonSize = b2Vec2(3,1)
        self.mRows = max(1, nrOfButtons / buttonPerColumn)
        self.mCols = min(nrOfButtons, buttonPerColumn)
        width = self.mButtonSize.x * self.mCols
        height = self.mButtonSize.y * self.mRows
        count = 0
        for y in range(self.mRows):
            for x in range(self.mCols):
                mx = x * self.mButtonSize.x + modelsize.x / 2.0 - width / 2.0
                my = y * self.mButtonSize.y + modelsize.y / 2.0 - height / 2.0
                self.mButtons.append(Button(texts[count], mx, my, self.mButtonSize, actions[count]))
                count += 1
    

"""
x = pos
y = pos
size = size per listitem
items = list containing resolutions
"""
class ListCreator(object):
    mItems = None
    mListItem = None
    
    def __init__(self, listheight, x, y, itemsize, items):
        self.viewRect = RectF(x, y, itemsize.x, listheight)
        self.itemSize = itemsize
        self.mListItem = []
        self.mItems = items
        self.pos = b2Vec2(x,y)
        
        self.mListItem.append(Button("+", x + itemsize.x, y, b2Vec2(0.5,0.5), ListItemAction.UP))
        self.mListItem.append(Button("-", x + itemsize.x, y + listheight - itemsize.y, b2Vec2(0.5,0.5), ListItemAction.DOWN))
        
        counter = 0
        for resolution in self.mItems:
            self.mListItem.append(ListItem(counter, x, y + (counter * itemsize.y), itemsize, resolution))
            counter += 1
    
    def isInViewRect(self, item):
        return self.viewRect.collidepoint(b2Vec2((item.x + item.size.x / 2.0, item.y + item.size.y / 2.0)))
    
    def scrollUp(self):
        for fi in self.mListItem:
            if isinstance(fi, ListItem):
                if fi.rect.y == self.viewRect.y:
                    return
                break
        
        for li in self.mListItem:
            if isinstance(li, ListItem):
                li.y += li.size.y
                li.rect.y = li.y
    
    def scrollDown(self):
        if self.mListItem[len(self.mListItem)-1].rect.y == self.viewRect.y + self.viewRect.h - self.itemSize.y:
            return
        
        for li in self.mListItem:
            if isinstance(li, ListItem):
                li.y -= li.size.y
                li.rect.y = li.y


class ListItem(object):
    
    def __init__(self, id, x, y, size, resolution):
        self.mId = id
        self.x, self.y = x, y
        self.size = size
        self.mText = resolution
        self.mAction = ListItemAction.ACTION
        self.mActive = False
        self.rect = RectF(x, y, size.x, size.y)

class Button(object):
    
    def __init__(self, text, x, y, size, action):
        self.mActive = False
        self.mText = text
        self.x, self.y = x, y
        self.size = size
        self.rect = RectF(x, y, size.x, size.y)
        self.mAction = action
        
class CheckButton(object):
    
    def __init__(self, text, x, y, size, action, checked):
        self.mAction = action
        self.mActive = checked
        self.mText = text
        self.x, self.y = x, y 
        self.size = size
        self.rect = RectF(x, y, size.x, size.y)

class MenuAction(object):
    NEWGAME = "MenuAction::NEWGAME"
    RETRY = "MenuAction::RETRY"
    OPTIONS = "MenuAction::OPTIONS"
    EXIT = "MenuAction::EXIT"
    BACK = "MenuAction::BACK"
    APPLY = "MenuAction::APPLY"
    INSTRUCTIONS = "MenuAction::INSTRUCTIONS"
    DEFAULTS = "MenuAction::DEFAULTS"
    
class CheckbuttonAction(object):
    FULLSCREEN = "CheckbuttonAction::FULLSCREEN"
    MUSIC = "CheckbuttonAction::MUSIC"
    SOUND = "CheckbuttonAction::SOUND"


class ListItemAction(object):
    ACTION = "ListItemAction::ACTION"
    UP = "ListItemAction::UP"
    DOWN = "ListItemAction::DOWN"