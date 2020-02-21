from panda3d.core import *
from math import sqrt

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class Collision():

    def __init__(self,entities):
        self.entities = entities

    def collisionDetection(self):
        self.isCollided = [[(distance(self.entities[a].pos, self.entities[b].pos) <= max(self.entities[a].scale, self.entities[b].scale), self.entities[b], self.entities[a]) for b in range(a)] for a in range(len(self.entities))]
        # Conversion du tableau en liste
        isCollidedCopy = []
        for i in range (len(self.isCollided)):
            isCollidedCopy += self.isCollided[i]
        self.isCollided = isCollidedCopy

    def consequences(self):
        for i in range(len(self.isCollided)):
            if self.isCollided[i][0] == True :
                if self.isCollided[i][1] == self.entities[0] and self.entities[0].scale > self.isCollided[i][2].scale:
                    self.isCollided[i][2].dommage(1000, self)  
                """else:
                    self.isCollided[i][1].model.setHpr(0, 0, -180)
                    self.isCollided[i][2].model.setHpr(0, 0, 0)"""

    def update(self):
        self.collisionDetection()
        self.consequences()


