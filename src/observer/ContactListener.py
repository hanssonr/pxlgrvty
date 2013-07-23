"""
Callback class for Box2D collision detection
Makes me able to alter things pre, post, and under collision
"""

from Box2D import b2ContactListener
from model.Tile import TileType, Tile
from model.entities.Box import Box
from model.Sensor import Sensor
from model.entities.Enemy import Enemy
from model.entities.SpikeBox import SpikeBox
from model.entities.Entity import Entity
from model.entities.Player import Player
from model.entities.PickableObject import PickableObject

class ContactListener(b2ContactListener):
    
    def __init__(self):
        super(ContactListener, self).__init__()
    
    def BeginContact(self, contact):
        fixA = contact.fixtureA
        fixB = contact.fixtureB          
        bodyA = fixA.body
        bodyB = fixB.body
        
        #Player onground/box
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
        """
        #Player collides Enemy
        if isinstance(bodyA.userData, Player):
            if isinstance(bodyB.userData, Enemy):
                bodyA.userData.alive = False
        elif isinstance(bodyB.userData, Player):
            if isinstance(bodyA.userData, Enemy):
                bodyB.userData.alive = False
        """
        if fixA.userData == Sensor.PLAYER_DEATHSENSOR:
            if isinstance(bodyB.userData, Enemy):
                bodyA.userData.alive = False
        elif fixB.userData == Sensor.PLAYER_DEATHSENSOR:
            if isinstance(bodyA.userData, Enemy):
                bodyB.userData.alive = False
        
        
        #Player collides pickupable
        if isinstance(bodyA.userData, Player):
            if isinstance(bodyB.userData, PickableObject):
                bodyB.userData.alive = False
        if isinstance(bodyB.userData, Player):
            if isinstance(bodyA.userData, PickableObject):
                bodyA.userData.alive = False
        
        #Entity enters gravityzone
        if fixA.userData == Sensor.GRAVITYZONESENSOR:
            if fixB.userData == TileType.GRAVITYZONE:
                bodyA.userData.enterGravityZone()
        elif fixB.userData == Sensor.GRAVITYZONESENSOR:
            if fixA.userData == TileType.GRAVITYZONE:
                bodyB.userData.enterGravityZone()
                
        #Spikebox collides with Tile/other entity
        if isinstance(bodyA.userData, SpikeBox):
            if isinstance(bodyB.userData, Tile) or isinstance(bodyB.userData, Box) or isinstance(bodyB.userData, SpikeBox):
                bodyA.userData.touch()
        if isinstance(bodyB.userData, SpikeBox):
            if isinstance(bodyA.userData, Tile) or isinstance(bodyA.userData, Box) or isinstance(bodyA.userData, SpikeBox):
                bodyB.userData.touch()
    
    def EndContact(self, contact):
        fixA = contact.fixtureA
        fixB = contact.fixtureB          
        bodyA = fixA.body
        bodyB = fixB.body
        
        #Player leaving ground/box
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
                
        #Spikebox leaving Tile/other entity
        if isinstance(bodyA.userData, SpikeBox):
            if isinstance(bodyB.userData, Tile) or isinstance(bodyB.userData, Box) or isinstance(bodyB.userData, SpikeBox):
                bodyA.userData.endtouch()
        if isinstance(bodyB.userData, SpikeBox):
            if isinstance(bodyA.userData, Tile) or isinstance(bodyA.userData, Box) or isinstance(bodyA.userData, SpikeBox):
                bodyB.userData.endtouch()
    
    
    def PreSolve(self, contact, oldManifold):
        pass
    
    def PostSolve(self, contact, impulse):
        pass
    