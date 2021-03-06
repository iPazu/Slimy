#Panda3d import
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

#Util import
from math import sqrt
import platform

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class Entity():

    def __init__(self, terrain, initialPos, ModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass, name):

        self.speed = LVecBase3f(0, 0, 0) # initialize as static object
        
        self.spawn(ModelPath,initialPos)
        
        #init constants
        self.name = name
        self.movingSpeed = movingSpeed
        self.scale = scale
        self.lifePoint = lifePoint
        self.maxLifePoint = lifePoint
        self.volumicMass = volumicMass
        self.mass = scale * volumicMass
        self.terrain = terrain
        
        # environment
        self.groundHeight = floorPos
        self.externalg = LVecBase3f(0,0,-9.81*self.mass) # const

        # init
        self.setScale(self.scale)

        # state
        self.is_flying = (self.pos[2] > self.groundHeight)
    
    def spawn(self,modelPath,initialPos):
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.pos = LVecBase3f(initialPos)

    def updatePos(self):
        self.model.setPos(self.pos)

    def updateMass(self):
        self.mass = self.scale * self.volumicMass

    def setScale(self, scale):
        self.scale, self.groundHeight = scale, scale
        self.model.setScale(self.scale)
        self.updateMass()

    def getPos(self):
        return self.pos

    def getHpr(self):
        return self.model.getHpr()

    """
    #if you want to test if an entithy is properly remove
    def __del__(self):
        print("Instance of Custom Class Alpha Removed")
    """

    def playSound(self,name,volume):
        self.sound = base.loader.loadSfx("assets/sounds/"+name)
        self.sound.play()
        self.sound.setVolume(volume)

        
