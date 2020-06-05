from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from entity import Entity
from panda3d.ai import *
from math import sqrt

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
        self.detectionDistance = detectionDistance
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
            self.music = base.loader.loadSfx("assets/sounds/candy.mp3")
            self.music.play()
            self.music.setVolume(0.1)
        elif self.name[8:] == "kamikaze":
            self.music = base.loader.loadSfx("assets/sounds/hitDamage.mp3")
            self.music.play()
            self.music.setVolume(0.1)
        else:
            self.music = base.loader.loadSfx("assets/sounds/slime.mp3")
            self.music.play()
            self.music.setVolume(0.1)
        self.aiWorld.removeAiChar(self.name)
        self.model.removeNode()
        Monster.score += self.scale
        Monster.monster.remove(self)

    def damage(self, dommagePoint):
        self.lifePoint -= dommagePoint
        if self.lifePoint <= 0:
            if self.name[8:] == "candy":
                self.target.setScale(self.target.scale+self.scale)
            self.remove()

    def generalUpdate(self,):
        self.pos = self.model.getPos()
        self.model.setPos((self.pos[0], self.pos[1], self.scale))

    def update(self,):
        self.generalUpdate()
        self.specificUpdate()
        