from monster import Monster

class Candy(Monster):

    def __init__(self, terrain, initialPos, target, aiWorld, size, name):
        #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name
        Monster.__init__(self, terrain, initialPos, "assets/models/candy.egg", 100, size, 1, 100, target, aiWorld, 100000, name, self.none)
        self.AIbehaviors.flee(self.target.model, 300, 600)

    def none(self,):
        pass