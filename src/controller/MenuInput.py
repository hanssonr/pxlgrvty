"""
Inputhandler for menus

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

import pygame
from pygame.locals import *
from libs.BaseInputHandler import BaseInputHandler

class MenuInput(BaseInputHandler):

    def __init__(self, screen):
        self.mMenuScreen = screen

        self.joysticks = []
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                self.joysticks.append(joystick)

    def update(self):
        for e in pygame.event.get():
            BaseInputHandler.checkEvent(self, e)

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.mMenuScreen.mouseClick(e.pos)

            if e.type == KEYDOWN:
                self.mMenuScreen.keyInput(e.key)

    def getMousePosition(self):
        return pygame.mouse.get_pos()
