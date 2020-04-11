from panda3d.core import *
from math import sqrt

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class Collision():

    def __init__(self,entities):
        self.entities = entities

    def start(self):
        #Initialisation of collision related objet
        base.cTrav = CollisionTraverser()
        #self.collHandEvent = CollisionHandlerEvent()
        #self.collHandEvent.addInPattern('into-%in')
        pusher = CollisionHandlerPusher()
        lifter = CollisionHandlerFloor()

        # Initialisation of list
        self.entitiesNode = []
        self.entitiesFloor = []
        self.entitiesC = []
        """self.collCount = 0"""

        # For all entities
        for i in range(len(self.entities)):
            # Create the node
            self.entitiesNode.append(CollisionNode(str(i)+" entities"))
            # Add solid to the node
            self.entitiesNode[i].addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
            self.entitiesNode[i].addSolid(CollisionRay((0, 0, 0), (0, 0, -1)))
            #
            """
            nodeStr = 'CollisionHull{0}_{1}'.format(self.collCount, self.entitiesNode[i].name)
            self.collCount += 1
            self.accept('into-' + nodeStr, self.collide)
            """
            # Add the nood to collider list
            self.entitiesC.append(self.entities[i].model.attachNewNode(self.entitiesNode[i]))
            # Initialise Collision
            base.cTrav.addCollider(self.entitiesC[i], pusher)
            #base.cTrav.addCollider(self.entitiesC[i], self.collHandEvent)
            pusher.addCollider(self.entitiesC[i], self.entities[i].model, base.drive.node())
            lifter.addCollider(self.entitiesC[i], self.entities[i].model)


