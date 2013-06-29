#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, Box2D
from pygame.locals import * 
from Box2D import b2Vec2, b2Vec2_zero
from libs.BaseInputHandler import *
from model.Direction import *
from model.Camera import *

class Input(BaseInputHandler):
    
    def __init__(self, world, camera):
        self.world = world
        self.player = world.player
        self.camera = camera
        self.gravity = world.gravity
    
    def update(self):  
        event = pygame.event.poll()      
        
        BaseInputHandler.checkEvent(self, event)
        
        if event.type == KEYDOWN:
            if self.player.mOnGround != False:
                if event.key == K_LEFT:
                    self.gravity.set(GravityDirection.LEFT)
                    self.player.flip(MoveDirection.LEFT)
                if event.key == K_RIGHT:
                    self.gravity.set(GravityDirection.RIGHT)
                    self.player.flip(MoveDirection.RIGHT)
                if event.key == K_UP:
                    self.gravity.set(GravityDirection.UP)
                    self.player.flip(MoveDirection.UP)
                if event.key == K_DOWN:
                    self.gravity.set(GravityDirection.DOWN)
                    self.player.flip(MoveDirection.DOWN)
                
            #cameradisplacement
            if event.key == K_KP4:
                self.camera.displacement.Set(self.camera.displacement.x + 1, self.camera.displacement.y)          
            if event.key == K_KP6:
                self.camera.displacement.Set(self.camera.displacement.x - 1, self.camera.displacement.y)       
            if event.key == K_KP8:
                self.camera.displacement.Set(self.camera.displacement.x, self.camera.displacement.y + 1)
            if event.key == K_KP5:
                self.camera.displacement.Set(self.camera.displacement.x, self.camera.displacement.y - 1)
                
        #model mousecoords        
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            cords = self.camera.getModelCoordinats(b2Vec2(x,y))
            print cords

        #zero out the velocity 
        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                self.player.mDirection.Set(0,0)
        
        #check for player movement
        pressed = pygame.key.get_pressed()
        
        if self.gravity.get().x == 0:
            if pressed[pygame.K_a]:
                self.player.move(MoveDirection.LEFT)
            if pressed[pygame.K_d]:
                self.player.move(MoveDirection.RIGHT)
        elif self.gravity.get().y == 0:
            if pressed[pygame.K_s]:
                self.player.move(MoveDirection.DOWN)
            if pressed[pygame.K_w]:
                self.player.move(MoveDirection.UP)

      
        #camerascale           
        if pressed[pygame.K_KP_PLUS]:
            self.camera.scale = b2Vec2(self.camera.scale.x + 1, self.camera.scale.y + 1)
        if pressed[pygame.K_KP_MINUS]:
            self.camera.scale = b2Vec2(self.camera.scale.x - 1, self.camera.scale.y - 1)
            
        
