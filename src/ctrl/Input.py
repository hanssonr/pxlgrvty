#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Maininput while the game is running for controlling the player

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

import pygame
from pygame.locals import * 
from libs.BaseInputHandler import BaseInputHandler
from model.Direction import GravityDirection, MoveDirection

class Input(BaseInputHandler):
    
    def __init__(self, screen, world, camera):
        self.mCurrentScreen = screen
        self.world = world
        self.player = world.player
        self.camera = camera
        self.gravity = world.gravity
        
        pygame.event.set_blocked(MOUSEMOTION)
    
    def update(self):  
        event = pygame.event.poll()      
        
        BaseInputHandler.checkEvent(self, event)
        
        if self.player.alive:
            #handle gravity
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.world.changeGravity(GravityDirection.LEFT)
                if event.key == K_RIGHT:
                    self.world.changeGravity(GravityDirection.RIGHT)
                if event.key == K_UP:
                    self.world.changeGravity(GravityDirection.UP)
                if event.key == K_DOWN:
                    self.world.changeGravity(GravityDirection.DOWN)
                if event.key == K_SPACE:
                    self.player.jump()
                if event.key == K_ESCAPE:
                    self.mCurrentScreen.goBack()
                if event.key == K_r:
                    self.world.restart()

                    
                #debug
                if event.key == K_F1:
                    self.world.DEBUG = not self.world.DEBUG
    
            #button up
            elif event.type == KEYUP:
                #zero out the velocity 
                if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                    self.player.mDirection.Set(0,0)
                if event.key == K_SPACE:
                    self.player.endJump()
            
            #check for player movement
            pressed = pygame.key.get_pressed()
            
            if self.player.mGravityToUse.x == 0:
                if pressed[pygame.K_a]:
                    self.player.move(MoveDirection.LEFT)
                if pressed[pygame.K_d]:
                    self.player.move(MoveDirection.RIGHT)
            elif self.player.mGravityToUse.y == 0:
                if pressed[pygame.K_s]:
                    self.player.move(MoveDirection.DOWN)
                if pressed[pygame.K_w]:
                    self.player.move(MoveDirection.UP)

        