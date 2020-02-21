from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from math import sqrt
from entity import Entity
from panda3d.ai import *

def distance(A, B):
    return sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 )

class Monster(Entity):
    def __init__(self, terrain, initialPos, ModelPath, movingSpeed, scale, lifePoint, volumicMass, target, AIworld, detectionDistance, name):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos , ModelPath, 2*scale, movingSpeed, scale, lifePoint, volumicMass)
        self.updatePos()
        self.detectionDistance = detectionDistance
        self.target = target
        self.status = False
        self.name = name

        #initialise AI stuff
        self.AIchar = AICharacter(self.name, self.model, self.mass, self.movingSpeed, self.movingSpeed)
        AIworld.addAiChar(self.AIchar)
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

    def dommage(self, dommagePoint, AIworld):
        self.lifePoint -= dommagePoint
        if self.lifePoint <= 0:
            self.target.setScale(self.target.scale + self.scale)
            self.model.removeNode()
            AIworld.removeAiChar(self.name)
            #monsterList.remove()
            
    def update(self):
        self.pos = self.model.getPos()
        self.detection()
        self.model.setPos((self.pos[0], self.pos[1], self.scale))

