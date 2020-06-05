from monster import Monster
from math import atan2, degrees

class Kamikaze(Monster):

    def __init__(self, terrain, initialPos, target, aiWorld, size, name):
        #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name, specificUpdate
        Monster.__init__(self, terrain, initialPos, "assets/models/kamikaze.egg", 175, size, 1, 100, target, aiWorld, 1000, name, self.Hpr)
        self.AIbehaviors.pursue(self.target.model)
        self.dx = 0
        self.dy = 0
        self.posx2, self.posy2 = self.pos[0], self.pos[1]

    def Hpr(self,):
        mw = base.mouseWatcherNode
        self.dx, self.dy = self.pos[0]-self.posx2, self.pos[1]-self.posy2
        self.angle = degrees(atan2(self.dy, self.dx))+90
        self.Hpr = (self.angle, 90, 0)
        self.model.setHpr(self.Hpr)
        self.posx2, self.posy2 = self.pos[0], self.pos[1]
        self.pos[2] = self.scale//2
        self.model.setPos(self.pos)