#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.PygameApplication import *
from libs.Pgl import *
from Pxlgrvty import *
import crypter


class Main(object):
    
    fps = 45
    
    def __init__(self):
        PygameApplication(Pxlgrvty(), self.fps)


if __name__ == "__main__":  
    Main()
