#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basklass för alla rörliga objekt
"""

class Entity(object):
    
    mPosition = None
    mBody = None
    
    def __init__(self, pos, physbody):
        self.mPosition = pos
        self.mBody = physbody
    
    def __getPosition(self):
        return self.mBody.position
    
    def __setPosition(self, pos, angle):
        self.mBody.transform(pos, angle)
    
    position = property(__getPosition, __setPosition)