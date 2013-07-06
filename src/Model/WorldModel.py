from controller.Input import Input
from Level import Level
from entities.Player import Player
from libs.Pgl import Pgl
from model.Gravity import Gravity
from observer.ContactListener import ContactListener
from model.entities.Box import Box
from Box2D import b2World, b2_dynamicBody, b2Vec2

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
    mEntityToFollow = None
    
    def __init__(self, camera):
        self.mCamera = camera
        self.main()
        
    
    def main(self):
        self.contactListener = ContactListener()
        self.gravity = Gravity()
        self.physWorld = b2World(gravity=(0,0),doSleep=True, contactListener=self.contactListener)
        self.level = Level(self.physWorld, self.gravity)
        self.player = Player(self.level.mStartPos, self.physWorld, self.gravity)
        self.mEntityToFollow = self.player
     
    def update(self, delta):
        #set oldposition for boxes
        for box in self.level.mObjects:
            if isinstance(box, Box):
                box.mOldPos = box.mBody.position.copy()
        
        #step the physicsworld
        self.physWorld.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.physWorld.ClearForces()
        
        self.level.update(self.player.position)
        
        #print len(self.physWorld.bodies)
        for body in self.physWorld.bodies:
            #dynamic body
            if body.type == b2_dynamicBody:
                if self.mFirstUpdate:
                    self.dynamic_enities.append(body)
                
                #playerobject
                if isinstance(body.userData, Player):
                    body.userData.update(delta)
                #box
                elif isinstance(body.userData, Box):
                    if self.level.isInActiveChunks(body.userData.position):
                        body.userData.update(delta)
                    else:
                        body.userData.stopMovement()
                    
        self.mFirstUpdate = False
        
        
    
    
    def changeGravity(self, gravitydirection):
        #if self.player.isOnGround() == True:
        self.gravity.set(gravitydirection)
        
        for body in self.dynamic_enities:
            if not body.userData.isInGravityZone():
                body.userData.flip(gravitydirection)
        
            #if not self.player.isInGravityZone():
                #self.player.flip(gravitydirection)

        

