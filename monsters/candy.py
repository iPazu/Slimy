from monster import Monster
from panda3d.core import *

class Candy(Monster):

    def __init__(self, terrain, initialPos, target, aiWorld, size, name):
        #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name
        Monster.__init__(self, terrain, initialPos, "assets/models/candy.egg", 100, size, 1, 10, target, aiWorld, 100000, name, self.Hpr)
        self.AIbehaviors.flee(self.target.model, 300, 600)

    def Hpr(self,):
        self.model.setHpr((0, 0, 0))
        self.pos = LVecBase3f(self.pos[0], self.pos[1], 0)
        self.model.setPos(self.pos)