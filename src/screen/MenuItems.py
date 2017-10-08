"""
Helpclass, constructning items for menus

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from Box2D import b2Vec2
from libs.RectF import RectF
from libs.Crypt import Crypt
from libs.Pgl import *
import json
from Resources import Resources


class TableCreator(object):
    mButtons = None
    mButtonSize = None

    def __init__(self, modelsize, buttonPerColumn, nrOfButtons, texts, actions):
        self.mButtons = []
        self.mButtonSize = b2Vec2(3,1)
        self.mRows = int(max(1, nrOfButtons / buttonPerColumn))
        self.mCols = int(min(nrOfButtons, buttonPerColumn))
        width = self.mButtonSize.x * self.mCols
        height = self.mButtonSize.y * self.mRows
        count = 0

        for y in range(self.mRows):
            for x in range(self.mCols):
                mx = x * self.mButtonSize.x + modelsize.x / 2.0 - width / 2.0
                my = y * self.mButtonSize.y + modelsize.y / 2.0 - height / 2.0
                self.mButtons.append(Button(texts[count], mx, my, self.mButtonSize, actions[count]))
                count += 1

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

        self.mListItem.append(Button("+", x + itemsize.x, y, b2Vec2(0.5,0.5), lambda:self.scrollUp()))
        self.mListItem.append(Button("-", x + itemsize.x, y + listheight - itemsize.y, b2Vec2(0.5,0.5), lambda:self.scrollDown()))

        counter = 0
        for resolution in self.mItems:
            active = True if resolution == self.usedResolution else False
            self.mListItem.append(ListItem(counter, x, y + (counter * itemsize.y), itemsize, resolution, active, lambda x: self.onItemClick(x)))
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

    def onItemClick(self, clicked):
        if not self.isInViewRect(clicked): return
        for item in self.mListItem:
            if isinstance(item, ListItem):
                item.mActive = False

        clicked.mActive = True
        Pgl.options.resolution = clicked.mText


class ListItem(object):

    def __init__(self, itemid, x, y, size, resolution, active, action):
        self.mId = itemid
        self.x, self.y = x, y
        self.size = size
        self.mText = resolution
        self.mAction = lambda: action(self)
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

    def __init__(self, text, x, y, size, checked, pointer, funclist = None):
        self.mAction = lambda:self.onClick(pointer, funclist)
        self.mActive = checked
        self.mText = text
        self.x, self.y = x, y
        self.size = size
        self.rect = RectF(x, y, size.x, size.y)

    def onClick(self, pointer, funclist):
        self.mActive = not self.mActive
        pointer(self.mActive)

        if funclist != None:
            for func in funclist:
                func(not self.mActive)


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
    #TODO: inherit choicewidget

    def __init__(self, text, x, y, baseamount, pointer, funclist = None):
        self.mVolumeItems = []
        self.amount = baseamount
        self.x, self.y = x, y

        buttonsize = 0.5
        self.mVolumeLabel = Label(str(self.amount) + "%", x + 1, y + buttonsize / 2.0)
        self.mVolumeItems.append(Label(text, x, y - buttonsize / 2.0))
        self.mVolumeItems.append(Button("-", x, y, b2Vec2(buttonsize, buttonsize), lambda:self.lower(pointer, funclist)))
        self.mVolumeItems.append(Button("+", x + 2, y, b2Vec2(buttonsize, buttonsize), lambda:self.higher(pointer, funclist)))
        self.mVolumeItems.append(self.mVolumeLabel)

    def lower(self, pointer, funclist):
        self.amount = 0 if self.amount - 5 < 0 else self.amount - 5
        self.mVolumeLabel.updateText(str(self.amount) + "%")
        pointer(self.amount)

        if funclist != None:
            for func in funclist:
                func()


    def higher(self, pointer, funclist):
        self.amount = 100 if self.amount + 5 > 100 else self.amount + 5
        self.mVolumeLabel.updateText(str(self.amount) + "%")
        pointer(self.amount)

        if funclist != None:
            for func in funclist:
                func()

class ChoiceWidget(object):

    def __init__(self, text, x, y, choicelist, standardchoice, pointer):
        self.mChoices = choicelist
        self.__mCurrent = standardchoice
        self.mWidgedItems = []

        buttonsize = 0.5
        self.mChoiceLabel = Label(self.mChoices[self.__mCurrent], x + 1, y + buttonsize / 2.0)
        self.mWidgedItems.append(Label(text, x, y - buttonsize / 2.0))
        self.mWidgedItems.append(Button("-", x, y, b2Vec2(buttonsize, buttonsize), lambda:self.prev(pointer)))
        self.mWidgedItems.append(Button("+", x + 2, y, b2Vec2(buttonsize, buttonsize), lambda:self.next(pointer)))
        self.mWidgedItems.append(self.mChoiceLabel)

    def next(self, pointer):
        self.__mCurrent = self.__mCurrent if self.__mCurrent + 1 > len(self.mChoices)-1 else self.__mCurrent + 1
        self.mChoiceLabel.updateText(self.mChoices[self.__mCurrent])
        pointer(self.__mCurrent)

    def prev(self, pointer):
        self.__mCurrent = self.__mCurrent if self.__mCurrent - 1 < 0 else self.__mCurrent - 1
        self.mChoiceLabel.updateText(self.mChoices[self.__mCurrent])
        pointer(self.__mCurrent)

class LevelTableCreator(object):
    mLevelButtons = None
    mButtonSize = None

    def __init__(self, modelsize, lvlPerColumn, nrOfLevels, action):
        self.__mCrypt = Crypt()
        self.mLevelButtons = []
        self.mButtonSize = b2Vec2(1,1)
        lock = self.__readLevelLockState()
        self.mRows = int(max(1, nrOfLevels / lvlPerColumn))
        self.mCols = int(min(nrOfLevels, lvlPerColumn))
        width = self.mButtonSize.x * self.mCols
        height = self.mButtonSize.y * self.mRows
        count = 1
        for y in range(self.mRows):
            for x in range(self.mCols):
                mx = x * self.mButtonSize.x + modelsize.x / 2.0 - width / 2.0
                my = y * self.mButtonSize.y + modelsize.y / 2.0 - height / 2.0
                self.mLevelButtons.append(LevelButton(count, mx, my, self.mButtonSize, action, False if count <= int(lock) else True))
                count += 1

    def __readLevelLockState(self):
            lvldata = None

            try:
                with open(Resources.getInstance().resource_path("assets/state/state.json"), "rb") as state:
                    decryptedData = self.__mCrypt.decrypt(state.read())
                    lvldata = json.loads(decryptedData)

                    try:
                        return lvldata["LVL"]
                    except:
                        raise IOError
            except (IOError):
                with open(Resources.getInstance().resource_path("assets/state/state.json"), "wb+") as state:
                    data = self.__mCrypt.encrypt('{"LVL":"1"}')
                    state.write(data)
                    return 1

class LevelButton(object):

    def __init__(self, text, x, y, size, action, locked):
        self.mLocked = locked
        self.mActive = False
        self.mAction = lambda: action(self.mText) if not locked else lambda: False
        self.mText = text
        self.x, self.y = x, y
        self.size = size
        self.rect = RectF(x, y, size.x, size.y)
