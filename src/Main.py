#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Libs.PygameApplication import *
from Libs.Pgl import *
from Pxlgrvty import *


class Main(object):
    
    #initialize windowsize and fps
    width = 1280
    height = 800
    fps = 60
    
    def __init__(self):
        PygameApplication(Pxlgrvty(), self.width, self.height, self.fps)


if __name__ == "__main__":  
    Main()
