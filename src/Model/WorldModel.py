from controller.Input import Input
from Level import Level
from entities.Player import Player
from libs.Pgl import Pgl
from model.Gravity import Gravity
from observer.ContactListener import ContactListener
from model.entities.Box import Box
from Box2D import b2World, b2_dynamicBody, b2Vec2
from Direction import GravityDirection
from entities.Enemy import Enemy

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
    
    def __init__(self, camera, luObserver):
        self.mCamera = camera
        self.mLuObs = luObserver
        self.contactListener = ContactListener()
        self.gravity = Gravity()
        self.physWorld = b2World(gravity=(0,0),doSleep=True, contactListener=self.contactListener)
        self.level = Level(self.physWorld, self.gravity)
        self.player = Player(self.level.mStartPos, self.physWorld, self.gravity)
        self.mEntityToFollow = self.player
        
    def resetWorld(self):
        self.dynamic_enities = []
        self.mFirstUpdate = True
        self.gravity.set(GravityDirection.DOWN)
        self.player.alive = True
        self.player.position = b2Vec2(self.level.mStartPos.x + self.player.size.x/3, self.level.mStartPos.y + self.player.size.y/2), 0
        self.player.mBodyDirection = GravityDirection.DOWN
        self.mLuObs.levelChanged(self.level)
        
     
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
            if body.type == b2_dynamicBody:
                if self.mFirstUpdate:
                    if not isinstance(body.userData, Enemy):
                        self.dynamic_enities.append(body)
                
                #playerobject
                if isinstance(body.userData, Player):
                    body.userData.update(delta)
                #box
                elif isinstance(body.userData, Box):
                    #if self.level.isInActiveChunks(body.userData.position):
                    body.userData.update(delta)
                    #else:
                        #body.userData.stopMovement()
                elif isinstance(body.userData, Enemy):
                    body.userData.update(delta)
        
        if self.mFirstUpdate == True:          
            self.mFirstUpdate = False
            
        #is level done, reset and start next level
        if self.level.update(self.player.position):
            self.resetWorld()
            
        #is player dead?
        if not self.player.alive:
            self.level.retryLevel()
            self.resetWorld()
        
    
    def changeGravity(self, gravitydirection):
        if self.player.isOnGround() == True:
            self.gravity.set(gravitydirection)
            
            for body in self.dynamic_enities:
                if not body.userData.isInGravityZone():
                    body.userData.flip(gravitydirection)
        
            #if not self.player.isInGravityZone():
                #self.player.flip(gravitydirection)

        

