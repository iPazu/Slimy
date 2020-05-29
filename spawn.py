from direct.showbase.DirectObject import DirectObject
from monster import Monster
from entity import Entity
from collision import Collision
import random

class Spawn(DirectObject):

    def __init__(self, entities, terrain, AIworld, collision):
        self.terrain = terrain
        self.AIworld = AIworld
        self.entities = entities
        self.slime = self.entities[0]
        self.collision = collision
        self.entitiesNumber = 1
        self.count = 0

    def spawn(self):
        self.entities = [self.slime]+Monster.monster
        self.entitiesNumber = len(self.entities)
        while self.entitiesNumber <= 13:
            self.entitiesNumber = len(self.entities)
            print("An entity have spawned")
            x, y = random.randint(-500, 500), random.randint(-500, 500)
            i = self.slime.scale
            size = random.randint(int(i-9), int(9+i))
            #self, terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, mass, target, aiWorld, detectionDistance, name
            Monster(self.terrain, (x, y, 3), "assets/models/evil_slime.egg", 150, size, 10, 10, self.slime, self.AIworld, 150, str(self.count))
            self.entities = [self.slime]+Monster.monster
            self.collision.addColliderObject(self.entities[self.entitiesNumber], self.count)
            self.count += 1

