import Box2D
from Box2D import b2ContactListener
from model.entities.Player import *

class ContactListener(b2ContactListener):
    
    def __init__(self):
        super(ContactListener, self).__init__()
    
    def BeginContact(self, contact):        
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        
        #Player onground
        if isinstance(contact.fixtureB.userData, Sensor):
            bodyB.userData.mOnGround += 1
        elif isinstance(contact.fixtureA.userData, Sensor):
            bodyA.userData.mOnGround += 1
    
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        
        #Player leaving ground
        if isinstance(contact.fixtureB.userData, Sensor):
            bodyB.userData.mOnGround -= 1
    
    
    def PreSolve(self, contact, oldManifold):
        pass
    
    def PostSolve(self, contact, impulse):
        pass
    