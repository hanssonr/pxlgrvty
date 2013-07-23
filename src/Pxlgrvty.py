#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.Game import *
from libs.BaseInputHandler import * 
from screen.LoadingScreen import LoadingScreen

class Pxlgrvty(Game):  
    
    def __init__(self):
        super(Pxlgrvty, self).__init__(self)
        self.mInput = BaseInputHandler()
        
  
    def create(self):
        #self.setScreen(GameScreen(self))
        self.setScreen(LoadingScreen(self))
    
    def update(self, delta):
        Game.update(self, delta)
    
    def render(self, delta):
        Game.render(self, delta)
    
    def __setInput(self, a_input):
        self.mInput = a_input
        
    def __getInput(self):
        return self.mInput
    
    input = property(__getInput, __setInput)

        
