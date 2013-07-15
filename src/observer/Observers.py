from abc import ABCMeta, abstractmethod

class LevelupdateListener(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def levelChanged(self, level):
        pass
        

class LevelupdateObserver(object):
    
    __mListeners = None
    
    def __init__(self):
        self.__mListeners = []
    
    def addListener(self, listener):
        self.__mListeners.append(listener)
    
    def levelChanged(self, level):
        for listener in self.__mListeners:
            listener.levelChanged(level)