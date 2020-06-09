#Panda3d import
from direct.showbase.DirectObject import DirectObject

#Util import
import random
import time
import sys

#Class import
from monster import Monster
from entity import Entity
from monsters.evilSlime import EvilSlime
from monsters.candy import Candy
from monsters.kamikaze import Kamikaze
from collision import Collision


class Spawn(DirectObject):

    def __init__(self, entities, terrain, AIworld, collision):
        # Get time 0
        self.t0 = int(round(time.time()))
        # Get object
        self.terrain = terrain
        self.AIworld = AIworld
        self.entities = entities
        self.collision = collision
        # Get slime
        self.slime = self.entities[0]

    def spawn(self):
        self.entities = [self.slime]+Monster.monster
        self.entitiesNumber = len(self.entities)
        while self.entitiesNumber <= 12:
            self.entitiesNumber = len(self.entities)
            x, y = random.randint(-500, 500), random.randint(-500, 500)
            i = self.slime.scale
            rand = random.randint(0, 100)
            # Set probability
            if int(round(time.time()))-self.t0 < 5:
                if rand > 70:
                    result = "evilSlime"
                else:
                    result = "candy"
            elif self.slime.scale < 75:
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
            # Create monster
            if result == "evilSlime":
                size = random.randint(int(i*0.8-4), 3+i)
                #self, terrain, initialPos, target, aiWorld, size, name
                EvilSlime(self.terrain, (x, y, 3), self.slime, self.AIworld, size, "evilSlime")
            elif result == "candy":
                size = random.randint(i-9, -1+i)
                #self, terrain, initialPos, target, aiWorld, size, name
                Candy(self.terrain, (x, y, 3), self.slime, self.AIworld, size, "candy")
            else:
                size = i//3
                #self, terrain, initialPos, target, aiWorld, size, name
                Kamikaze(self.terrain, (x, y, 3), self.slime, self.AIworld, size, "kamikaze")
            # Update
            self.entities = [self.slime]+Monster.monster
            self.collision.addColliderObject(self.entities[self.entitiesNumber])
