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
    
    def __init__(self, x, y, size, items):
        self.mListItem = []
        self.mItems = items
        self.pos = b2Vec2(x,y)
        
        counter = 0
        for resolution in self.mItems:
            self.mListItem.append(ListItem(counter, x, y + (counter * size.y), size, resolution))
            counter += 1


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