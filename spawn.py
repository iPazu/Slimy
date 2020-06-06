from direct.showbase.DirectObject import DirectObject
from monster import Monster
from entity import Entity
from monsters.evilSlime import EvilSlime
from monsters.candy import Candy
from monsters.kamikaze import Kamikaze
from collision import Collision
import random
import time
import sys

class Spawn(DirectObject):

    def __init__(self, entities, terrain, AIworld, collision):
        self.t0 = int(round(time.time() * 1000))
        self.terrain = terrain
        self.AIworld = AIworld
        self.entities = entities
        self.slime = self.entities[0]
        self.collision = collision

    def spawn(self):
        self.entities = [self.slime]+Monster.monster
        self.entitiesNumber = len(self.entities)
        while self.entitiesNumber <= 12:
            self.entitiesNumber = len(self.entities)
            x, y = random.randint(-500, 500), random.randint(-500, 500)
            i = self.slime.scale
            rand = random.randint(0, 100)
            if int(round(time.time() * 1000))-self.t0 < 5:
                if rand > 70:
                    result = "evilSlime"
                else:
                    result = "candy"
            elif self.slime.scale < 200:
                if rand > 45:
                    result = "evilSlime"
                elif rand < 30:
                    result = "kamikaze"
                else:
                    result = "candy"
            else:
                if rand > 30:
                    result = result = "evilSlime"
                else:
                    result = "kamikaze"
            if result == "evilSlime":
                size = random.randint(int(i-9), int(9+i))
                EvilSlime(self.terrain, (x, y, 3), self.slime, self.AIworld, size, "evilSlime")
            elif result == "candy":
                #self, terrain, initialPos, target, aiWorld, size, name
                size = random.randint(int(i-9), int(-1+i))
                Candy(self.terrain, (x, y, 3), self.slime, self.AIworld, size, "candy")
            else:
                size = int(i//2)
                Kamikaze(self.terrain, (x, y, 3), self.slime, self.AIworld, size, "kamikaze")
            self.entities = [self.slime]+Monster.monster
            self.collision.addColliderObject(self.entities[self.entitiesNumber])
