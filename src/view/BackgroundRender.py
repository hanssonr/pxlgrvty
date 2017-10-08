"""
Class that renders the background depending on variable of the level

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

from libs.Sprite import Sprite
from libs.Pgl import *
from Resources import *
import pygame

class BackgroundRender(object):

    mBg = None
    mBgColor = None
    mCamera = None

    def __init__(self, camera, level):
        self.mCamera = camera
        self.levelUpdate(level)

    def render(self, delta):
        Pgl.app.surface.fill(self.mBgColor)
        self.mBg.draw(self.mCamera.getScaledSize(3 - self.mCamera.displacement.x / 6, 2 - self.mCamera.displacement.y / 2.5))

    def levelUpdate(self, level):
        self.mBg = Sprite(pygame.image.load(Resources.getInstance().resource_path("assets/gfx/%s" % level.mBackground)).convert(), self.mCamera.getScaledSize(5,5))
        self.mBgColor = level.mBackgroundcolor
