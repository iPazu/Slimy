from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from entity import Entity

class Creature(Entity):
    def __init__(self,initialPos, monsterModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass):

        #initialise parent stuff
        Entity.__init__(self,initialPos, monsterModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass)