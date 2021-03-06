"""
The games worldmodel, initialize all the enitites of the game and its levels

Author: Rickard Hansson, rkh.hansson@gmail.com
"""
from model.Level import Level
from model.entities.Player import Player
from model.Gravity import Gravity
from observer.ContactListener import ContactListener
from model.entities.Box import Box
from Box2D import b2World, b2_dynamicBody, b2Vec2
from model.entities.Enemy import Enemy
from model.entities.PickableObject import PickableObject
from effects.Particle import Particle
from effects.BloodSplatter import BloodSplatter
from libs.SoundManager import SoundManager, SoundID

class WorldModel(object):

    DEBUG = False

    physWorld = None
    vel_iters, pos_iters = 6, 2
    debugRender = None;
    player = None
    body = None
    dynamic_enities = []
    mFirstUpdate = True
    mEntityToFollow = None
    mTimer = None
    mDeathTimer = 1.0

    mSwitch = None


    def __init__(self, camera, luObserver, fxObserver, lvl):
        self.mSwitch = True
        self.mTimer = 0.0
        self.mLevelDone = False
        self.mCamera = camera
        self.mLuObs = luObserver
        self.mFxObs = fxObserver
        self.contactListener = ContactListener()
        self.gravity = Gravity()
        self.physWorld = b2World(gravity=(0,0),doSleep=True, contactListener=self.contactListener)
        self.level = Level(self.physWorld, self.gravity, lvl)
        self.player = Player(self.level.mStartPos, self.physWorld, self.gravity)
        self.mEntityToFollow = self.player

    def __resetWorld(self):
        self.mSwitch = True
        self.mDeathTimer = 1.0
        self.mTimer = 0.0
        self.dynamic_enities = []
        self.mFirstUpdate = True
        self.gravity.reset()
        self.player.reset(b2Vec2(self.level.mStartPos.x + self.player.size.x/3, self.level.mStartPos.y + self.player.size.y/2))
        self.mLuObs.levelChanged(self.level)

    def restart(self):
        self.mFxObs.addFx(BloodSplatter(self.physWorld, self.gravity.get(), self.player.position))
        self.level.retryLevel()
        self.__resetWorld()

    def update(self, delta):
        self.mTimer += delta

        #step the physicsworld
        self.physWorld.Step(delta, self.vel_iters, self.pos_iters)
        self.physWorld.ClearForces()

        for body in self.physWorld.bodies:
            #dynamic body
            if body.type == b2_dynamicBody:
                if self.mFirstUpdate:
                    if isinstance(body.userData, Player):
                        self.dynamic_enities.append(body)

                    # body.userData.update(delta)
                if isinstance(body.userData, Player):
                    body.userData.update(delta)
                elif isinstance(body.userData, Enemy):
                    body.userData.update(delta)
                elif isinstance(body.userData, PickableObject):
                    body.userData.update(delta)
                elif isinstance(body.userData, Particle):
                    body.userData.update(delta)


        if self.mFirstUpdate == True:
            self.mFirstUpdate = False

        #update level, if level is done, returns true
        if self.level.update(delta, self.player.position):
            self.mLevelDone = True

        #is player dead?
        if not self.player.alive:

            if self.mSwitch:
                SoundManager.getInstance().playSound(SoundID.FLESHEXPLOSION)
                self.mFxObs.addFx(BloodSplatter(self.physWorld, self.gravity.get(), self.player.position))
                self.mSwitch = False

            self.player.stopMovement()
            self.mDeathTimer -= delta

            if self.mDeathTimer < 0:
                self.level.retryLevel()
                self.__resetWorld()


    def changeGravity(self, gravitydirection):
        if self.player.isOnGround() == True:
            self.gravity.set(gravitydirection)

            for body in self.dynamic_enities:
                if not body.userData.isInGravityZone():
                    body.userData.flip(gravitydirection)
