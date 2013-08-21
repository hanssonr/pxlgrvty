#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Start the game by initializing a new pygameapplication and inject the game into it

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.PygameApplication import PygameApplication
from Pxlgrvty import Pxlgrvty


class Main(object):
    
    def __init__(self):
        PygameApplication(Pxlgrvty())


if __name__ == "__main__":  
    Main()
