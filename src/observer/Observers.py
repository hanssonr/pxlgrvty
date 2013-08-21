"""
Observers and listeners

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from abc import ABCMeta, abstractmethod

class LevelupdateListener(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def levelChanged(self, level):
        raise Exception("Override this")
        

class LevelupdateObserver(object):
    
    __mListeners = None
    
    def __init__(self):
        self.__mListeners = []
    
    def addListener(self, listener):
        self.__mListeners.append(listener)
    
    def levelChanged(self, level):
        for listener in self.__mListeners:
            listener.levelChanged(level)
            
class FXListener(object):
    __metaclass_ = ABCMeta
    
    @abstractmethod
    def addFx(self, fx):
        raise Exception("Override this")
    

class FXObserver(object):
    
    __mListeners = None
    
    def __init__(self):
        self.__mListeners = []
        
    def addListener(self, listener):
        self.__mListeners.append(listener)
    
    def addFx(self, fx):
        for listener in self.__mListeners:
            listener.addFx(fx)
