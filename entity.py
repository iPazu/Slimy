from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Entity():
        def __init__(self,initialPos, ModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass):

            #loading the model
            self.model = loader.loadModel(ModelPath)
            self.model.reparentTo(render)

            #initialise vectorial stuff
            self.pos = LVecBase3f(initialPos)
            self.pos.set 
            self.speed = LVecBase3f(0,0,0) # initialize as static object
        
            #init constants
            self.movingSpeed = movingSpeed
            self.scale = scale
            self.lifePoint = lifePoint
            self.volumicMass = volumicMass
            self.mass = scale * volumicMass
        
<<<<<<< Updated upstream
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
=======
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
>>>>>>> Stashed changes
