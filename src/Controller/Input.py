#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, Box2D
from pygame.locals import * 
from Box2D import b2Vec2, b2Vec2_zero
from Libs.BaseInputHandler import *
from Model.Direction import *

class Input(BaseInputHandler):
    
    def __init__(self, world, camera):
        self.world = world
        self.player = world.player
        self.camera = camera
    
    def update(self):
        
        event = pygame.event.poll()      
        
        BaseInputHandler.checkEvent(self, event)
        
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.camera.displacement.Set(self.camera.displacement.x + 1, self.camera.displacement.y)
            if event.key == K_RIGHT:
                self.camera.displacement.Set(self.camera.displacement.x - 1, self.camera.displacement.y)
            if event.key == K_UP:
                self.camera.displacement.Set(self.camera.displacement.x, self.camera.displacement.y + 1)
            if event.key == K_DOWN:
                self.camera.displacement.Set(self.camera.displacement.x, self.camera.displacement.y - 1)
            if event.key == K_SPACE:
                self.player.mGravity *= -1

        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                self.player.mDirection.Set(self.player.mGravity.x, self.player.mGravity.y)
            elif event.key == K_w or event.key == K_s:
                self.player.mDirection.Set(self.player.mGravity.x, self.player.mGravity.y)
        
        pressed = pygame.key.get_pressed()
        
        if self.player.mGravityDirection == GravityDirection.DOWN or self.player.mGravityDirection == GravityDirection.DOWN:
            if pressed[pygame.K_a]:
                self.player.goLeft()
            if pressed[pygame.K_d]:
                self.player.goRight()
        else:
            if pressed[pygame.K_s]:
                self.player.goRight()
            if pressed[pygame.K_w]:
                self.player.goLeft()

        
           
        if pressed[pygame.K_KP_PLUS]:
            self.camera.scale = b2Vec2(self.camera.scale.x + 1, self.camera.scale.y + 1)
        if pressed[pygame.K_KP_MINUS]:
            self.camera.scale = b2Vec2(self.camera.scale.x - 1, self.camera.scale.y - 1)
