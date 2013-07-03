from Camera import *
from controller.Input import *
from Level import *
from entities.Player import *
from view.DebugDraw import *
from libs.Pgl import *
from model.Gravity import *
from observer.ContactListener import *
from model.entities.Box import *

class WorldModel(object):
    
    DEBUG = False
    
    physWorld = None
    timeStep = 1.0 / 60
    vel_iters, pos_iters = 6, 2 
    debugRender = None;
    player = None
    body = None
    dynamic_enities = []
    mFirstUpdate = True
    
    def __init__(self):
        self.main()
    
    def main(self):
        self.contactListener = ContactListener()
        self.gravity = Gravity()
        self.physWorld = Box2D.b2World(gravity=(0,0),doSleep=True, contactListener=self.contactListener)
        self.level = Level(self.physWorld, self.gravity)
        self.player = Player(self.level.mStartPos, self.physWorld, self.gravity)
     
    def update(self, delta):
        #set oldposition for boxes
        for box in self.level.mObjects:
            if isinstance(box, Box):
                box.mOldPos = box.mBody.position.copy()
        
        #step the physicsworld
        self.physWorld.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.physWorld.ClearForces()
        
        for body in self.physWorld.bodies:
            #dynamic body
            if body.type == Box2D.b2_dynamicBody:
                if self.mFirstUpdate:
                    self.dynamic_enities.append(body)
                
                #playerobject
                if isinstance(body.userData, Player):
                    body.userData.update(delta)
                #box
                elif isinstance(body.userData, Box):
                    body.userData.update(delta)
                    
        self.mFirstUpdate = False
        
        
    
    
    def changeGravity(self, gravitydirection):
        if self.player.isOnGround() == True:
            self.gravity.set(gravitydirection)
            
            for body in self.dynamic_enities:
                if not body.userData.isInGravityZone():
                    body.userData.flip(gravitydirection)
            
            #if not self.player.isInGravityZone():
                #self.player.flip(gravitydirection)

