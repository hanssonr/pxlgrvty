#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.PygameApplication import *
from libs.Pgl import *
from Pxlgrvty import *


class Main(object):
    
    width =  1280
    height = 800
    fps = 60
    
    def __init__(self):
        PygameApplication(Pxlgrvty(), self.width, self.height, self.fps)


if __name__ == "__main__":  
    Main()
