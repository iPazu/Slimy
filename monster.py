from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from entity import Entity
from panda3d.ai import *
from math import sqrt

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class Monster(Entity):

    monster = []

    def __init__(self, terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, mass, target, aiWorld, detectionDistance, name):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos , modelPath, 2*scale, movingSpeed, scale, lifePoint, mass)
        self.name = name
        self.updatePos()
        self.detectionDistance = detectionDistance
        self.target = target
        self.status = False
        self.aiWorld = aiWorld
        self.setUpAI()
        self.mass = mass
        Monster.monster.append(self)
    
    def setUpAI(self):
        #initialise AI stuff
        self.AIchar = AICharacter(self.name, self.model, self.mass, self.movingSpeed, self.movingSpeed)
        self.aiWorld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.pursue(self.target.model, 1)
        self.AIbehaviors.wander(50, 0, 50, 1)
        
        self.AIbehaviors.pauseAi("pursue")

    def detection(self):
        targetDistance = distance(self.pos, self.target.pos)
        status = targetDistance < self.detectionDistance
        if status != self.status:
            if status == True:
                self.status = True
                self.AIbehaviors.pauseAi("wander")
                self.AIbehaviors.resumeAi("pursue")
            else :
                self.status = False
                self.AIbehaviors.pauseAi("pursue")
                self.AIbehaviors.resumeAi("wander")

    def remove(self):
        Monster.monster.remove(self)
        self.model.removeNode()
        self.aiWorld.removeAiChar(self.name)

    def damage(self, dommagePoint):
        self.lifePoint -= dommagePoint
        if self.lifePoint < self.maxLifePoint*0.8:
            self.model.setColor(1,0,0,1)
        if self.lifePoint <= 0:
            self.target.setScale(self.target.scale + self.scale)
            self.remove()

    def update(self):
        self.pos = self.model.getPos()
        self.detection()
        self.model.setPos((self.pos[0], self.pos[1], self.scale))
        self.model.setHpr((0, 0, 0))
        