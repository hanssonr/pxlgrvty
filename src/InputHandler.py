#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, Box2D
from pygame.locals import * 
from Box2D import b2Vec2, b2Vec2_zero

class InputHandler(object):
    
    def __init__(self, world, player, camera):
        self.world = world
        self.player = player
        self.camera = camera
    
    def update(self):
        event = pygame.event.poll()
        
        if event.type == pygame.QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.camera.displacement = b2Vec2(self.camera.displacement.x + 1, self.camera.displacement.y)
            if event.key == K_RIGHT:
                self.camera.displacement = b2Vec2(self.camera.displacement.x - 1, self.camera.displacement.y)
            if event.key == K_UP:
                self.camera.displacement = b2Vec2(self.camera.displacement.x, self.camera.displacement.y + 1)
            if event.key == K_DOWN:
                self.camera.displacement = b2Vec2(self.camera.displacement.x, self.camera.displacement.y - 1)
            if event.key == K_SPACE:
                self.world.gravity = b2Vec2(0, self.world.gravity.y * -1)
        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                self.player.velocity = b2Vec2(0,0)
        
        pressed = pygame.key.get_pressed()
         
        if pressed[pygame.K_a]:
            self.player.velocity = b2Vec2(-3,0)
        if pressed[pygame.K_d]:
            self.player.velocity = b2Vec2(3,0)
        if pressed[pygame.K_s]:
            self.player.velocity = b2Vec2(0,-3)
        if pressed[pygame.K_w]:
            self.player.velocity = b2Vec2(0,3)
        
           
        if pressed[pygame.K_KP_PLUS]:
            self.camera.scale = b2Vec2(self.camera.scale.x + 1, self.camera.scale.y + 1)
        if pressed[pygame.K_KP_MINUS]:
            self.camera.scale = b2Vec2(self.camera.scale.x - 1, self.camera.scale.y - 1)
        
        return True
