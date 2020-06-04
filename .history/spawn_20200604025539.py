from direct.showbase.DirectObject import DirectObject
from monster import Monster
from entity import Entity
from Monster.evilSlime import EvilSlime
from Monster.candy import Candy
from collision import Collision
import random
import sys

def standardization(number):
    number = str(number)
    n = len(number)
    if n <= 8:
        return (8-n)*'0'+number
    else:
        print("Max number of this entity have been reach")
        sys.exit()

class Spawn(DirectObject):

    def __init__(self, entities, terrain, AIworld, collision):
        self.terrain = terrain
        self.AIworld = AIworld
        self.entities = entities
        self.slime = self.entities[0]
        self.collision = collision
        self.entitiesNumber = 1
        self.count = 1

    def spawn(self):
        self.entities = [self.slime]+Monster.monster
        self.entitiesNumber = len(self.entities)
        while self.entitiesNumber <= 10:
            self.entitiesNumber = len(self.entities)
            x, y = random.randint(-500, 500), random.randint(-500, 500)
            i = self.slime.scale
            rand = random.randint(0, 100)
            if rand > 30:
                size = random.randint(int(i-9), int(9+i))
                EvilSlime(self.terrain, (x, y, 3), self.slime, self.AIworld, size, standardization(self.count)+"evilSlime")
            else:
                #self, terrain, initialPos, target, aiWorld, size, name
                size = random.randint(int(i-9), int(i-1))
                Candy(self.terrain, (x, y, 3), self.slime, self.AIworld, size, standardization(self.count)+"candy")
            self.entities = [self.slime]+Monster.monster
            self.collision.addColliderObject(self.entities[self.entitiesNumber])
            self.count += 1

