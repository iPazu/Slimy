from panda3d.core import *
from math import sqrt
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.showbase.DirectObject import DirectObject
from monster import Monster
from slime import Slime
from projectile import Projectile
import platform
def standardization(number):
    number = str(number)
    n = len(number)
    return (8-n)*'0'+number

def distance(A, B):
    return round(sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ))

class Collision(DirectObject):

    def __init__(self,entities):
        #Initialisation of collision related objet
        global pusher, lifter
        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()
        lifter = CollisionHandlerFloor()
        pusher.addInPattern('%fn-into-%in')

        self.count = -1

        # Initialisation of list
        self.entitiesNode = []
        self.entitiesC = []
    
    def addColliderObject(self, entity):
        self.count += 1
        name = str(standardization(self.count))+entity.name
        entity.name = name
        number = self.count
        self.entities = [Slime.slime[0]]+Monster.monster
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
        if number != 0:
            self.accept('00000000slime-into-'+name, self.collide1)
        for p in Projectile.projectile:
            self.accept(p.name+'-into-'+name, self.projectileHandler)
        
    def projectileInit(self, p):
        self.count += 1
        name = str(standardization(self.count))+p.name
        p.name = name
        number = self.count
        self.entitiesNode.append(CollisionNode(name))
        # Add solid to the node
        self.entitiesNode[number].addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
        # Add the nood to collider list
        self.entitiesC.append(p.model.attachNewNode(self.entitiesNode[number]))
        # Initialise Collision
        base.cTrav.addCollider(self.entitiesC[number], pusher)
        pusher.addCollider(self.entitiesC[number], p.model, base.drive.node())
        lifter.addCollider(self.entitiesC[number], p.model)
        for m in Monster.monster:
            self.accept(p.name+'-into-'+m.name, self.projectileHandler)

    def projectileHandler(self, collEntry):
        projectile = collEntry.getFromNodePath().getParent()
        monster = collEntry.getIntoNodePath().getParent()
        i = 0
        while projectile != Projectile.projectile[i].model:
            i+=1
        projectile = Projectile.projectile[i]
        i = 0
        while monster != Monster.monster[i].model:
            i+=1
        monster = Monster.monster[i]
        if monster.name[8:] != "candy":
            if monster.name[8:] == "kamikaze" and monster.lifePoint <= projectile.damage:
                monster.playSound("slime.mp3",0.5)
            monster.damage(projectile.damage)
        projectile.model.setPos(10000, 10000, 0)
        projectile.destroy()

    def collide1(self, collEntry):
        self.entities = [self.entities[0]]+Monster.monster
        slime = self.entities[0]
        collInto = collEntry.getIntoNodePath().getParent()
        nodePath = [self.entities[i].model for i in range(len(self.entities))]
        i = 0
        while collInto != nodePath[i]:
            i += 1
        monster = self.entities[i]
        if monster.name[8:] == "kamikaze":
            monster.damage(80)
            slime.damage(25)
        elif slime.scale > monster.scale:
            monster.damage(monster.lifePoint)
        else:
            slime.playSound("hitDamage.mp3",0.1)
            slime.damage(20)
        """
        Sequence(
            Func(collParent.setColor, (1, 0, 0, 1)),
            Wait(0.2),
            Func(collParent.setColor, (0, 1, 0, 1)),
            Wait(0.2),
            Func(collParent.setColor, (1, 1, 1, 1)),
        ).start()
        """
