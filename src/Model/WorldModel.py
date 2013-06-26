from Camera import *
from Controller.Input import *
from Level import *
from Player import *
from View.DebugDraw import *
from Libs.Pgl import *

class WorldModel(object):
    
    physWorld = None
    timeStep = 1.0 / 60
    vel_iters, pos_iters = 6, 2 
    debugRender = None;
    player = None
    body = None
    
    def __init__(self):
        self.main()
    
    def main(self):
        self.physWorld = Box2D.b2World(gravity=(0,0),doSleep=True)
        level = Level(self.physWorld)
        self.player = Player(level.mStartPos, self.physWorld)
     
    def update(self, delta):
        self.physWorld.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.physWorld.ClearForces()
        
        self.player.update(delta)

