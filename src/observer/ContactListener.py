import Box2D
from Box2D import b2ContactListener
from model.entities.Player import *
from model.Tile import TileType

class ContactListener(b2ContactListener):
    
    def __init__(self):
        super(ContactListener, self).__init__()
    
    def BeginContact(self, contact):
        fixA = contact.fixtureA
        fixB = contact.fixtureB          
        bodyA = fixA.body
        bodyB = fixB.body
        
        #Player onground
        if fixB.userData == Sensor.FOOTSENSOR:
            bodyB.userData.mOnGround += 1
        elif fixA.userData == Sensor.FOOTSENSOR:
            bodyA.userData.mOnGround += 1
        
        #Player entering gravityzone (TODO: change to some baseclass)
        if fixB.userData == Sensor.GRAVITYZONESENSOR:
            if fixA.userData == TileType.GRAVITYZONE:
                bodyB.userData.enterGravityZone()
        elif fixA.userData == Sensor.GRAVITYZONESENSOR:
            if fixB.userData == TileType.GRAVITYZONE:
                bodyA.userData.enterGravityZone()
    
    def EndContact(self, contact):
        fixA = contact.fixtureA
        fixB = contact.fixtureB          
        bodyA = fixA.body
        bodyB = fixB.body
        
        #Player leaving ground
        if fixB.userData == Sensor.FOOTSENSOR:
            bodyB.userData.mOnGround -= 1
            
        #Player leaving gravityzone (TODO: change to some baseclass)
        if fixB.userData == Sensor.GRAVITYZONESENSOR:
            if fixA.userData == TileType.GRAVITYZONE:
                bodyB.userData.exitGravityZone()
        elif fixA.userData == Sensor.GRAVITYZONESENSOR:
            if fixB.userData == TileType.GRAVITYZONE:
                bodyA.userData.exitGravityZone()
    
    
    def PreSolve(self, contact, oldManifold):
        pass
    
    def PostSolve(self, contact, impulse):
        pass
    