import Box2D
from Box2D import b2ContactListener

class ContactListener(b2ContactListener):
    
    def __init__(self):
        super(ContactListener, self).__init__()
    
    def BeginContact(self, contact):        
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
    
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
    
    
    def PreSolve(self, contact, oldManifold):
        pass
    
    def PostSolve(self, contact, impulse):
        pass
    