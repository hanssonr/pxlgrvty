#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pxlgrvty is the games that runs, inherits from superclass Game

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.Game import *
from libs.BaseInputHandler import BaseInputHandler
from screen.LoadingScreen import LoadingScreen

class Pxlgrvty(Game):
    
    __mInput = None
    
    def __init__(self):
        super(Pxlgrvty, self).__init__(self)
        self.__mInput = BaseInputHandler()
         
    def create(self):
        self.setScreen(LoadingScreen(self))
    
    def update(self, delta):
        Game.update(self, delta)
    
    def render(self, delta):
        Game.render(self, delta)
    
    def __setInput(self, a_input):
        self.__mInput = a_input
        
    def __getInput(self):
        return self.__mInput
    
    input = property(__getInput, __setInput)

        
