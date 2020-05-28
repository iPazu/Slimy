from panda3d.core import *
from cuboid import Cuboid
class Module():
    def __init__(self,pos,difficulty):
        self.pos = pos
        self.difficulty = difficulty
        self.models = []
        self.initCollisionBox(pos,(5,6,10))

    def createBox(self,pos,scale):
        c = Cuboid(scale,pos)
        c.hide()
        cnodePath = c.model.attachNewNode(CollisionNode('cnode'))
        box = CollisionBox(pos, scale[0], scale[1], scale[2])
        cnodePath.node().addSolid(box)
        cnodePath.show()

    