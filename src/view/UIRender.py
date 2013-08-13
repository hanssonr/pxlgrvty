from libs.Sprite import Sprite
from Resources import Resources
from model.Camera import Camera
from model.Time import Time
from libs.Pgl import *

class UIRender(object):
    
    mCamera = None
    mWorld = None
    mUI = None
    mTimeFont = None
    
    def __init__(self, camera, world):
        self.mCamera = camera
        self.mWorld = world
        
        self.mUI = Sprite(Resources.getInstance().mUI, self.mCamera.getScaledSize(4,1))

        self.timefont = Resources.getInstance().getScaledFont(self.mCamera.scale.x)
        self.timesize = self.timefont.size("00:00:00")
        
    def render(self, delta):
        uipos =  self.mCamera.getScaledSize(Camera.CAMERA_WIDTH / 2.0 - 2, Camera.CAMERA_HEIGHT - 1)
        self.mUI.draw(uipos)
        
        self.time = self.timefont.render(Time.convertToTimeString(self.mWorld.mTimer), 0, (255, 255, 255))
        Pgl.app.surface.blit(self.time,
                             (self.mCamera.getScaledSize(Camera.CAMERA_WIDTH / 2.0 - (self.timesize[0] / 2.0) / self.mCamera.scale.x, 
                                                         Camera.CAMERA_HEIGHT - ((Camera.CAMERA_HEIGHT +self.timesize[1]) / self.mCamera.scale.y))))