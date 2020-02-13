from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Entity():
        def __init__(self,terrain,initialPos, ModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass):

            #loading the model
            self.model = loader.loadModel(ModelPath)
            self.model.reparentTo(render)

            #initialise vectorial stuff
            self.pos = LVecBase3f(initialPos)
            self.speed = LVecBase3f(0,0,0) # initialize as static object
        
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

            # state
            self.is_flying = (self.pos[2] > self.groundHeight)

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
