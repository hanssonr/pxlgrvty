#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, Box2D
from pygame.locals import * 
from Box2D import b2Vec2, b2Vec2_zero
from Libs.BaseInputHandler import *
from Model.Direction import *
from Model.Camera import *

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
                self.player.mGravityDirection = GravityDirection.LEFT
                self.player.flipGravityX()
            if event.key == K_RIGHT:
                self.player.mGravityDirection = GravityDirection.RIGHT
                self.player.flipGravityX()
            if event.key == K_UP:
                self.player.mGravityDirection = GravityDirection.UP
                self.player.flipGravityY()
            if event.key == K_DOWN:
                self.player.mGravityDirection = GravityDirection.DOWN
                self.player.flipGravityY()
            if event.key == K_SPACE:
                pass
            if event.key == K_KP4:
                self.camera.displacement.Set(self.camera.displacement.x + 1, self.camera.displacement.y)
            if event.key == K_KP6:
                self.camera.displacement.Set(self.camera.displacement.x - 1, self.camera.displacement.y)
            if event.key == K_KP8:
                self.camera.displacement.Set(self.camera.displacement.x, self.camera.displacement.y + 1)
            if event.key == K_KP5:
                self.camera.displacement.Set(self.camera.displacement.x, self.camera.displacement.y - 1)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            cords = self.camera.getModelCoordinats(b2Vec2(x,y))
            print cords

        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                self.player.mDirection.Set(self.player.mGravity.x, self.player.mGravity.y)
            elif event.key == K_w or event.key == K_s:
                self.player.mDirection.Set(self.player.mGravity.x, self.player.mGravity.y)
        
        pressed = pygame.key.get_pressed()
        
        if self.player.mGravityDirection == GravityDirection.DOWN or self.player.mGravityDirection == GravityDirection.UP:
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
            
        
