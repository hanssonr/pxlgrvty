#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, Box2D
from Box2D import *
from pygame.locals import *
from DebugDraw import DebugDraw
from Camera import Camera
from Player import Player
from InputHandler import InputHandler
from Level import Level

class Game(object):
    
    world = None
    width = 1280
    height = 800
    clock = None 
    fps = 60
    screen = None 
    timeStep = 1.0 / 60
    vel_iters, pos_iters = 6, 2    
    camera = Camera(width, height)
    debugRender = None;
    player = None
    body = None
    
    def __init__(self):
        self.main()
    
    def main(self):
        pygame.init()
        self.world = Box2D.b2World(gravity=(0,0),doSleep=False)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        Level(self.world)
        
        self.debugRender = DebugDraw(self.camera, self.screen)
        self.world.renderer = self.debugRender
        self.debugRender.AppendFlags(self.debugRender.e_shapeBit)
        self.body = self.world.CreateDynamicBody(position=(8,3))
        self.player = Player((1,1), self.world)
        #self.createDemoWorld()
        
        inputhandler = InputHandler(self.world, self.player, self.camera)
           
        while True:
            delta = self.clock.tick(self.fps)
            
            #close game if input returns false
            if not inputhandler.update():
                break
                
            self.update(delta)
            self.render(delta)
                
        pygame.quit()
        
    def update(self, delta):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.world.ClearForces()
        
        self.player.update(delta)
    
    def render(self, delta):
        self.screen.fill((0,0,0))
        self.world.DrawDebugData()
        #self.draw_world()
        pygame.display.flip()
    
    def createDemoWorld(self):
        boxesX = 0
        while boxesX < self.camera.CAMERA_WIDTH:
            self.world.CreateStaticBody(position=(boxesX,0), shapes=b2PolygonShape(box=(0.5,0.5)))
            self.world.CreateStaticBody(position=(boxesX,self.camera.CAMERA_HEIGHT -1), shapes=b2PolygonShape(box=(0.5,0.5)))
            boxesX += 1
        
        self.world.CreateStaticBody(position=(5,4), shapes=b2PolygonShape(box=(0.5,0.5)))
        self.world.CreateStaticBody(position=(6,4), shapes=b2PolygonShape(box=(0.5,0.5)))
    
game = Game()
