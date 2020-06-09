#Panda3d import
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from panda3d.ai import *

#Util import
from math import sqrt

#Class import
from entity import Entity

#Utilities fonction
def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))


class Monster(Entity):

    monster = []
    score = 0

    def __init__(self, terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, mass, target, aiWorld, detectionDistance, name, specificUpdate):
        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos , modelPath, 2*scale, movingSpeed, scale, lifePoint, mass, name)
        self.specificUpdate = specificUpdate
        #initconstant
        self.updatePos()
        self.detectionDistance = detectionDistance+scale
        self.target = target
        self.mass = mass
        #AIstuff
        self.aiWorld = aiWorld
        self.AIchar = AICharacter(self.name, self.model, self.mass, self.movingSpeed, self.movingSpeed)
        self.aiWorld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        #Add to the list
        Monster.monster.append(self)

    def remove(self):
        if self.name[8:] == "candy":
            self.playSound("candy.ogg",0.5)
        elif self.name[8:] == "kamikaze":
            self.playSound("hitDamage.ogg",0.5)
        else:
            self.playSound("slime.ogg",0.5)
        self.aiWorld.removeAiChar(self.name)
        self.model.removeNode()
        Monster.monster.remove(self)

    def damage(self, dommagePoint, killer):
        self.lifePoint -= dommagePoint
        if self.lifePoint <= 0:
            if self.name[8:] == "candy":
                if self.target.scale < 75:
                    self.target.setScale(self.target.scale+self.scale)
                elif self.target.scale > 75:
                    self.target.scale = 75
            if killer != "projectile":
                Monster.score += self.scale
            self.remove()

    def generalUpdate(self,):
        self.pos = self.model.getPos()
        self.model.setPos((self.pos[0], self.pos[1], self.scale))

    def update(self,):
        self.generalUpdate()
        self.specificUpdate()
        
