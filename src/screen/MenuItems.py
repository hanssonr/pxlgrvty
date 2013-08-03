from Box2D import b2Vec2
from libs.RectF import RectF
from libs.Crypt import Crypt
import json

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
    
    def __init__(self, listheight, x, y, itemsize, items, reso):
        self.usedResolution = reso
        self.viewRect = RectF(x, y, itemsize.x, listheight)
        self.itemSize = itemsize
        self.mListItem = []
        self.mItems = items
        self.pos = b2Vec2(x,y)
        
        self.mListItem.append(Button("+", x + itemsize.x, y, b2Vec2(0.5,0.5), ListItemAction.UP))
        self.mListItem.append(Button("-", x + itemsize.x, y + listheight - itemsize.y, b2Vec2(0.5,0.5), ListItemAction.DOWN))
        
        counter = 0
        for resolution in self.mItems:
            active = True if resolution == self.usedResolution else False
            self.mListItem.append(ListItem(counter, x, y + (counter * itemsize.y), itemsize, resolution, active))
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
    
    def __init__(self, itemid, x, y, size, resolution, active):
        self.mId = itemid
        self.x, self.y = x, y
        self.size = size
        self.mText = resolution
        self.mAction = ListItemAction.ACTION
        self.mActive = active
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
    

class Label(object):
    def __init__(self, text, x, y):
        self.mText = text
        self.x, self.y = x, y
        self.mActive = True
        self.size = b2Vec2(0,0)
        self.rect = RectF(x, y, self.size.x, self.size.y)
        
    def updateText(self, text):
        self.mText = text
   
class Volume(object):
    
    def __init__(self, text, x, y, buttoninfo, baseamount):
        self.mVolumeItems = []
        self.amount = baseamount
        self.x, self.y = x, y
        
        buttonsize = 0.5
        self.mVolumeLabel = Label(str(self.amount) + "%", x + 1, y + buttonsize / 2.0)
        self.mVolumeItems.append(Label(text, x, y - buttonsize / 2.0))
        self.mVolumeItems.append(Button(buttoninfo[0][0], x, y, b2Vec2(buttonsize, buttonsize), buttoninfo[0][1]))
        self.mVolumeItems.append(Button(buttoninfo[1][0], x + 2, y, b2Vec2(buttonsize, buttonsize), buttoninfo[1][1]))
        self.mVolumeItems.append(self.mVolumeLabel)
    
    def lower(self):
        self.amount = 0 if self.amount - 5 < 0 else self.amount - 5
        self.mVolumeLabel.updateText(str(self.amount) + "%")
    
    def higher(self):
        self.amount = 100 if self.amount + 5 > 100 else self.amount + 5
        self.mVolumeLabel.updateText(str(self.amount) + "%")

class LevelTableCreator(object):
    mLevelButtons = None
    mButtonSize = None
    
    def __init__(self, modelsize, lvlPerColumn, nrOfLevels):
        self.__mCrypt = Crypt()
        self.mLevelButtons = []
        self.mButtonSize = b2Vec2(1,1)
        lock = self.__readLevelLockState()
        self.mRows = max(1, nrOfLevels / lvlPerColumn)
        self.mCols = min(nrOfLevels, lvlPerColumn)
        width = self.mButtonSize.x * self.mCols
        height = self.mButtonSize.y * self.mRows
        count = 1
        for y in range(self.mRows):
            for x in range(self.mCols):
                mx = x * self.mButtonSize.x + modelsize.x / 2.0 - width / 2.0
                my = y * self.mButtonSize.y + modelsize.y / 2.0 - height / 2.0
                self.mLevelButtons.append(LevelButton(count, mx, my, self.mButtonSize, False if count <= int(lock) else True))
                count += 1
        
    def __readLevelLockState(self):
            lvldata = None
        
            try:
                with open("assets/state/state.json", "rb") as state:
                    decryptedData = self.__mCrypt.decrypt(state.read())
                    lvldata = json.loads(decryptedData)
                    
                    try:
                        return lvldata["LVL"]
                    except:
                        raise IOError
            except (IOError):
                with open("assets/state/state.json", "wb+") as state:
                    data = self.__mCrypt.encrypt('{"LVL":"1"}')
                    state.write(data)
                    return 1    

class LevelButton(object):
    
    def __init__(self, text, x, y, size, locked):
        self.mLocked = locked
        self.mActive = False
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
    
class VolumeAction(object):
    MUSIC_VOLUME_UP = "VolumeAction::MVOLUP"
    MUSIC_VOLUME_DOWN = "VolumeAction::MVOLDOWN"
    SOUND_VOLUME_UP = "VolumeAction::SVOLUP"
    SOUND_VOLUME_DOWN = "VolumeAction::SVOLDOWN"