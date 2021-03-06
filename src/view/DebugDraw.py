"""
class that draws debuginfo for Box2D

https://github.com/jameydeorio/GGJ/blob/master/debugdraw.py (modified)
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, Box2D
from Box2D import *
from pygame.locals import *
from model.Camera import *
from libs.Pgl import *


class DebugDraw(b2Draw):
    """
    This debug draw class accepts callbacks from Box2D (which specifies what to draw)
    and handles all of the rendering.

    If you are writing your own game, you likely will not want to use debug drawing.
    Debug drawing, as its name implies, is for debugging.
    """
    circle_segments = 16
    surface = None
    camera = None
    height = 600
    lines = None
    
    def __init__(self, camera): 
        super(DebugDraw, self).__init__()
        self.camera = camera
        self.surface = Pgl.app.surface
        self.lines = []

    def convertColor(self, color):
        """
        Take a floating point color in range (0..1,0..1,0..1) and convert it to (255,255,255)
        """
        if isinstance(color, b2Color):
            return (int(255*color.r), int(255*color.g), int(255*color.b))
        return (int(255*color[0]), int(255*color[1]), int(255*color[2]))

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size/self.camera.scale().x, color, drawwidth=0)
        
    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        points = [self.toScreen(p) for p in [
                    (aabb.lowerBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.upperBound.y ),
                    (aabb.lowerBound.x, aabb.upperBound.y ),
                    ] ]

        pygame.draw.aalines(self.surface, color, True, points)

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        """if len(self.lines) > 7:
            self.DrawSolidPolygon(self.lines, color)
            self.lines = []
        
        self.lines.append(p1)
        self.lines.append(p2)"""
        color = self.convertColor(color)
        if self.camera.isInFrustum(p1[0], p1[1]) or self.camera.isInFrustum(p2[0], p2[1]):
            pygame.draw.line(self.surface, color, self.toScreen(p1), self.toScreen(p2))

    def DrawXForm(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        k_axisScale = 0.4
        p2 = self.toScreen(p1 + k_axisScale * xf.R.col1)
        p3 = self.toScreen(p1 + k_axisScale * xf.R.col2)
        p1 = self.toScreen(p1)

        color = (255,0,0)
        pygame.draw.aaline(self.surface, color, p1, p2)

        color = (0,255,0)
        pygame.draw.aaline(self.surface, color, p1, p3)

    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a wireframe circle given the b2Vec2 center_v, radius, axis of orientation and color.
        """
        color = self.convertColor(color)
        radius *= self.camera.scale.x
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.toScreen(center)
        #if self.camera.isInFrustum(center-radius, center+radius):
        #pygame.draw.circle(self.surface, color, center, radius, drawwidth)

    def DrawSolidCircle(self, center_v, radius, axis, color):
        """
        Draw a solid circle given the b2Vec2 center_v, radius, axis of orientation and color.
        """
        color = self.convertColor(color)
        radius *= self.camera.scale.x
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.toScreen(center_v)
        pygame.draw.circle(self.surface, color, center, radius, 1)  

    def DrawPolygon(self, in_vertices, color):
        """
        Draw a wireframe polygon given the world vertices in_vertices (tuples) with the specified color.
        """
        color = self.convertColor(color)
        vertices = [self.toScreen(v) for v in in_vertices]
        pygame.draw.polygon(self.surface, color, vertices, 1)
        
    def DrawSolidPolygon(self, in_vertices, color):
        """
        Draw a filled polygon given the world vertices in_vertices (tuples) with the specified color.
        """
        color = self.convertColor(color)
        vertices = [self.toScreen(v) for v in in_vertices]
        pygame.draw.polygon(self.surface, color, vertices, 1)

    def toScreen(self, pt):
        """
        Input:  (x, y) - a tuple in world coordinates
        Output: (x, y) - a tuple in screen coordinates
        """   
        pt = b2Vec2(pt[0], pt[1])
        pt = self.camera.getViewCoords(pt)
        return (int(pt.x), int(pt.y))
                 
