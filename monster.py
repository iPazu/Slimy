from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from math import sqrt
from entity import Entity

from panda3d.ai import *

class Monster(Entity):
    def __init__(self, terrain, initialPos, ModelPath, movingSpeed, scale, lifePoint, volumicMass, target, AIworld, detectionDistance):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos , ModelPath, 2*scale, movingSpeed, scale, lifePoint, volumicMass)
        self.updatePos()
        self.detectionDistance = detectionDistance
        self.target = target
        self.status = False

        #initialise AI stuff
        self.AIchar = AICharacter("seeker", self.model, self.mass, self.movingSpeed, self.movingSpeed)
        AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.pursue(self.target.model, 1)
        self.AIbehaviors.wander(50, 0, 50, 1)
        self.AIbehaviors.obstacleAvoidance(1)
        #self.model.loop("run")
        self.AIbehaviors.pauseAi("pursue")

    def detection(self):
        targetPos = self.target.getPos()
        targetDistance = sqrt( (self.pos[0]-targetPos[0])**2 + (self.pos[1]-targetPos[1])**2 + (self.pos[2]-targetPos[2])**2)
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

    def update(self):
        self.pos = self.model.getPos()
        self.detection()
        self.model.setPos((self.pos[0], self.pos[1], 0))
