from panda3d.core import *
from math import sqrt
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.showbase.DirectObject import DirectObject
from monster import Monster

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class Collision(DirectObject):

    def __init__(self,entities):
        self.entities = entities
        #Initialisation of collision related objet
        global pusher, lifter
        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()
        lifter = CollisionHandlerFloor()
        pusher.addInPattern('%fn-into-%in')

        # Initialisation of list
        self.entitiesNode = []
        self.entitiesC = []

        self.addColliderObject(self.entities[0])
    
    def addColliderObject(self, entity):
        name = entity.name
        number = int(entity.name[:8])
        self.entities = [self.entities[0]]+Monster.monster
        # Create the node
        self.entitiesNode.append(CollisionNode(name))
        # Add solid to the node
        self.entitiesNode[number].addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
        # Add the nood to collider list
        self.entitiesC.append(entity.model.attachNewNode(self.entitiesNode[number]))
        # Initialise Collision
        base.cTrav.addCollider(self.entitiesC[number], pusher)
        pusher.addCollider(self.entitiesC[number], entity.model, base.drive.node())
        lifter.addCollider(self.entitiesC[number], entity.model)
        self.accept('00000000slime-into-'+name, self.collide1)

    def collide1(self, collEntry):
        self.entities = [self.entities[0]]+Monster.monster
        if (self.entities[0].model == collEntry.getFromNodePath().getParent()):
            slime = self.entities[0]
            collInto = collEntry.getIntoNodePath().getParent()
            nodePath = [self.entities[i].model for i in range(len(self.entities))]
            i = 0
            while collInto != nodePath[i]:
                i += 1
            monster = self.entities[i]
            if slime.scale > monster.scale:
                monster.damage(50)
            else:
                slime.damage(25)
        else:
            print("AVOID")
        """
        Sequence(
            Func(collParent.setColor, (1, 0, 0, 1)),
            Wait(0.2),
            Func(collParent.setColor, (0, 1, 0, 1)),
            Wait(0.2),
            Func(collParent.setColor, (1, 1, 1, 1)),
        ).start()
        """
