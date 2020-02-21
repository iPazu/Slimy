from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Entity():
    def __init__(self, terrain, initialPos, modelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass):

        self.spawn(modelPath,initialPos)
        self.speed = LVecBase3f(0, 0, 0) # initialize as static object
        
        #init constants
        self.movingSpeed = movingSpeed
        self.scale = scale
        self.lifePoint = lifePoint
        self.volumicMass = volumicMass
        self.mass = scale * volumicMass
        self.terrain = terrain
        
        # environment
        self.groundHeight = floorPos
        self.externalg = LVecBase3f(0,0,-9.81*self.mass) # const

        # init
        self.setScale(scale)

        # state
        self.is_flying = (self.pos[2] > self.groundHeight)

    def spawn(self,modelPath,initialPos):
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.pos = LVecBase3f(initialPos)

    def remove(self):
        self.removeNode()
        

    def updatePos(self):
        self.model.setPos(self.pos)

    def updateMass(self):
        self.mass = self.scale * self.volumicMass

    def setScale(self,scale):
        self.model.setScale(scale)
        self.updateMass()

    def getPos(self):
        return self.pos

    def setLifePoint(self,lifePoint):
        self.lifePoint = lifePoint

