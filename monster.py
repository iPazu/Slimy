from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from entity import Entity
from panda3d.ai import *
from collision import distance

class Monster(Entity):

    monsters = []

    def __init__(self, terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos , modelPath, 2*scale, movingSpeed, scale, lifePoint, volumicMass)
        self.name = name
        self.updatePos()
        self.detectionDistance = detectionDistance
        self.target = target
        self.status = False
        self.aiWorld = aiWorld
        self.setUpAI()
        Monster.monsters.append(self)
    
    def setUpAI(self):
        #initialise AI stuff
        self.AIchar = AICharacter(self.name, self.model, self.mass, self.movingSpeed, self.movingSpeed)
        self.aiWorld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.pursue(self.target.model, 1)
        self.AIbehaviors.wander(50, 0, 50, 1)
        #self.model.loop("run")
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

    def remove(self, collision):
        Monster.monsters.remove(self)
        collision.entities.remove(self)
        self.model.removeNode()
        self.aiWorld.removeAiChar(self.name)

    def dommage(self, dommagePoint, collision):
        self.lifePoint -= dommagePoint
        if self.lifePoint <= 0:
            self.target.setScale(self.target.scale + self.scale)
            self.remove(collision)
            
    def update(self):
        self.pos = self.model.getPos()
        self.detection()
        self.model.setPos((self.pos[0], self.pos[1], self.scale))
        self.model.setHpr((0, 0, 0))
        

