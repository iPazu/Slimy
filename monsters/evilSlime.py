from monster import Monster
from math import sqrt

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class EvilSlime(Monster):

    def __init__(self, terrain, initialPos, target, aiWorld, size, name):
        #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name, specificUpdate
        Monster.__init__(self, terrain, initialPos, "assets/models/evil_slime.egg", 10, size, 50+size//2, 10, target, aiWorld, 500, name, self.detection)
        #initialise AI stuff related to this object
        targetDistance = distance(self.pos, self.target.pos)
        self.statusD = (targetDistance < self.detectionDistance)
        self.statusS = (self.target.scale < self.scale)
        self.AIbehaviors.pursue(self.target.model, 1)
        self.AIbehaviors.flee(self.target.model, 500, 500)
        self.AIbehaviors.wander(50, 0, 50, 1)
        self.AIbehaviors.pauseAi("pursue")
        self.AIbehaviors.pauseAi("flee")

    def detection(self):
        targetDistance = distance(self.pos, self.target.pos)
        statusD = (targetDistance < self.detectionDistance)
        statusS = (self.target.scale < self.scale)
        if statusS != self.statusS or statusD != self.statusD:
            if statusD == False:
                self.AIbehaviors.pauseAi("pursue")
                self.AIbehaviors.pauseAi("flee")
                self.AIbehaviors.resumeAi("wander")
            else:
                if statusS == True:
                    self.AIbehaviors.pauseAi("wander")
                    self.AIbehaviors.pauseAi("flee")
                    self.AIbehaviors.resumeAi("pursue")
                else:
                    self.AIbehaviors.pauseAi("pursue")
                    self.AIbehaviors.pauseAi("wander")
                    self.AIbehaviors.resumeAi("flee")
        self.statusS = statusS
        self.statusD = statusD
        self.model.setHpr((0, 0, 0))
