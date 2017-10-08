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

        self.joysticks = []
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                self.joysticks.append(joystick)

        pygame.event.set_blocked(MOUSEMOTION)

    def deadZoneAdjustment(self, value, deadzone = 0.15):
        if value > deadzone:
            return (value - deadzone) / (1 -deadzone)
        elif value < -deadzone:
            return (value + deadzone) / (1 - deadzone)
        else:
            return 0

    def update(self):
        for event in pygame.event.get():

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

                #gamepad
                if event.type == JOYBUTTONDOWN:
                    if event.button == 0:
                        self.player.jump()
                    if event.button == 7:
                        self.world.restart()
                    if event.button == 6:
                        self.mCurrentScreen.goBack()
                elif event.type == JOYBUTTONUP:
                    if event.button == 0:
                        self.player.endJump()

                leftStickX = 0
                leftStickY = 0
                rightStickX = 0
                rightStickY = 0
                if event.type == JOYAXISMOTION:
                    leftStickX = self.deadZoneAdjustment(self.joysticks[0].get_axis(0), 0.4)
                    leftStickY = self.deadZoneAdjustment(self.joysticks[0].get_axis(1), 0.4)

                    rightStickY = self.deadZoneAdjustment(self.joysticks[0].get_axis(3), 0.7)
                    rightStickX = self.deadZoneAdjustment(self.joysticks[0].get_axis(4), 0.7)

                    if leftStickX == 0 or leftStickY == 0:
                        self.player.mDirection.Set(0,0)

                    if rightStickX < 0:
                        self.world.changeGravity(GravityDirection.LEFT)
                    if rightStickX > 0:
                        self.world.changeGravity(GravityDirection.RIGHT)
                    if rightStickY < 0:
                        self.world.changeGravity(GravityDirection.UP)
                    if rightStickY > 0:
                        self.world.changeGravity(GravityDirection.DOWN)

                #check for player movement
                pressed = pygame.key.get_pressed()

                if self.player.mGravityToUse.x == 0:
                    if pressed[pygame.K_a] or leftStickX < 0:
                        self.player.move(MoveDirection.LEFT)
                    if pressed[pygame.K_d] or leftStickX > 0:
                        self.player.move(MoveDirection.RIGHT)
                elif self.player.mGravityToUse.y == 0:
                    if pressed[pygame.K_s] or leftStickY > 0:
                        self.player.move(MoveDirection.DOWN)
                    if pressed[pygame.K_w] or leftStickY < 0:
                        self.player.move(MoveDirection.UP)
