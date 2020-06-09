#Util import
from math import atan2, degrees

#Class import
from monster import Monster


class Kamikaze(Monster):

    def __init__(self, terrain, initialPos, target, aiWorld, size, name):
        #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name, specificUpdate
        Monster.__init__(self, terrain, initialPos, "assets/models/kamikaze2.egg", 175, size, 1, 100, target, aiWorld, 1000, name, self.Hpr)
        self.AIbehaviors.pursue(self.target.model)
        self.dx = 0
        self.dy = 0
        self.posx2, self.posy2 = self.pos[0], self.pos[1]

    def Hpr(self):
        self.dx, self.dy = self.pos[0]-self.posx2, self.pos[1]-self.posy2
        self.angle = degrees(atan2(self.dy, self.dx))+90
        self.Hpr = (self.angle, 90, 0)
        self.model.setHpr(self.Hpr)
        self.posx2, self.posy2 = self.pos[0], self.pos[1]
        self.pos[2] = 4/3*self.scale
        self.model.setPos(self.pos)