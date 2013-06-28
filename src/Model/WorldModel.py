from Camera import *
from controller.Input import *
from Level import *
from entities.Player import *
from view.DebugDraw import *
from libs.Pgl import *
from model.Gravity import *
from observer.ContactListener import *

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
        self.contactListener = ContactListener()
        self.gravity = Gravity()
        self.physWorld = Box2D.b2World(gravity=(0,0),doSleep=True, contactListener=self.contactListener)
        self.level = Level(self.physWorld)
        self.player = Player(self.level.mStartPos, self.physWorld, self.gravity)
     
    def update(self, delta):
        self.physWorld.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.physWorld.ClearForces()
        
        self.player.update(delta)

