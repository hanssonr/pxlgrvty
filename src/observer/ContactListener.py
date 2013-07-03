import Box2D
from Box2D import b2ContactListener
from model.entities.Player import *
from model.Tile import *
from model.Sensor import *
from model.entities.Box import *

class ContactListener(b2ContactListener):
    
    def __init__(self):
        super(ContactListener, self).__init__()
    
    def BeginContact(self, contact):
        fixA = contact.fixtureA
        fixB = contact.fixtureB          
        bodyA = fixA.body
        bodyB = fixB.body
        
        #Player onground
        if fixB.userData == Sensor.PLAYER_FOOTSENSOR:
            if isinstance(bodyA.userData, Tile):
                bodyB.userData.mOnGround += 1
            elif isinstance(bodyA.userData, Box):
                if bodyA.userData.isMoving():
                    bodyB.userData.mOnGround -= 1
                else:
                    bodyB.userData.mOnGround += 1
                
        elif fixA.userData == Sensor.PLAYER_FOOTSENSOR:
            if isinstance(bodyB.userData, Tile):
                bodyA.userData.mOnGround += 1
            elif isinstance(bodyB.userData, Box):
                if bodyB.userData.isMoving():
                    bodyA.userData.mOnGround -= 1
                else:
                    bodyA.userData.mOnGround += 1
        
        #Entity enters gravityzone
        if fixA.userData == Sensor.GRAVITYZONESENSOR:
            print fixA.body
            if fixB.userData == TileType.GRAVITYZONE:
                bodyA.userData.enterGravityZone()
        elif fixB.userData == Sensor.GRAVITYZONESENSOR:
            if fixA.userData == TileType.GRAVITYZONE:
                bodyB.userData.enterGravityZone()
    
    def EndContact(self, contact):
        fixA = contact.fixtureA
        fixB = contact.fixtureB          
        bodyA = fixA.body
        bodyB = fixB.body
        
        #Player leaving ground
        if fixB.userData == Sensor.PLAYER_FOOTSENSOR:
            if isinstance(bodyA.userData, Tile):
                bodyB.userData.mOnGround -= 1
            elif isinstance(bodyA.userData, Box):
                bodyB.userData.mOnGround -= 1
                    
        elif fixA.userData == Sensor.PLAYER_FOOTSENSOR:
            if isinstance(bodyB.userData, Tile):
                bodyA.userData.mOnGround -= 1
            elif isinstance(bodyB.userData, Box):
                bodyA.userData.mOnGround -= 1
        
        
        #Entity leaving gravityzone
        if fixA.userData == Sensor.GRAVITYZONESENSOR:
            if fixB.userData == TileType.GRAVITYZONE:
                bodyA.userData.exitGravityZone()
        elif fixB.userData == Sensor.GRAVITYZONESENSOR:
            if fixA.userData == TileType.GRAVITYZONE:
                bodyB.userData.exitGravityZone()
    
    
    def PreSolve(self, contact, oldManifold):
        pass
    
    def PostSolve(self, contact, impulse):
        pass
    