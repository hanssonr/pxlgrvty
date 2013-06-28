#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.Game import *
from libs.BaseInputHandler import * 
from screen.LoadingScreen import LoadingScreen

class Pxlgrvty(Game):  
    
    def __init__(self):
        super(Pxlgrvty, self).__init__(self)
        self.input = BaseInputHandler()
        
  
    def create(self):
        #self.setScreen(GameScreen(self))
        self.setScreen(LoadingScreen(self))
    
    def update(self, delta):
        Game.update(self, delta)
    
    def render(self, delta):
        Game.render(self, delta)
    
    def setInput(self, a_input):
        self.input = a_input

        
