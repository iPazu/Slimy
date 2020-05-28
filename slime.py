from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from entity import Entity
from math import log2
import time
class Slime(Entity):

    def __init__(self, terrain, initialPos, slimeModelPath, scale, lifePoint, volumicMass, movingSpeed):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos, slimeModelPath, scale, movingSpeed, scale, lifePoint, volumicMass)


        #init constants
        self.jumpSpeed = LVecBase3f(0, 0, 8)
        self.dashSpeed = 15

        #user controls
        self.forward = KeyboardButton.asciiKey("z")
        self.backward = KeyboardButton.asciiKey('s')
        self.left = KeyboardButton.asciiKey('q')
        self.right = KeyboardButton.asciiKey('d')
        self.e = KeyboardButton.asciiKey('e')
        self.keymaplist = [self.forward, self.backward, self.right, self.left]
        self.t0 = 0
        self.dashDelay = 5
        self.initCollisionBox()

        base.accept('space', self.jump,[self.jumpSpeed])

    def update(self, dt):  # dt = time elapsed between the two updates
        self.checkForMovement()
        if (self.is_flying == True or self.speed[2] >= 0):
            #self.updateJumpAnimation()   
            self.pos += self.speed*dt
            self.speed += self.externalg*dt
            self.speed[0] = 0
            self.speed[1] = 0
        else:
            self.pos[2] = self.groundHeight
            self.speed = LVecBase3f(0, 0, 0)

        self.is_flying = (self.pos[2] > self.groundHeight) # status updating
        self.updatePos()

    def checkForMovement(self):
        isDown = base.mouseWatcherNode.isButtonDown
        for x in range(4):
            if(isDown(self.keymaplist[x])):
                movingIncrementer = self.movingSpeed
                if(isDown(self.e)):
                    if int(round(time.time() * 1000)) - self.t0 > self.dashDelay*1000:
                        movingIncrementer = self.dashSpeed*8
                        self.t0 = int(round(time.time() * 1000))
                if(x < 2): #backward or forward
                    self.speed[1] = movingIncrementer * (-1)**x
                else: #left or right
                    self.speed[0] = movingIncrementer * (-1)**x
    
    def jump(self, jspeed):
        if not self.is_flying:
            self.speed += jspeed
    def setColor(self,r,g,b,a):
        print("Changing color of the slime with colors {} {} {} {}".format(r,g,b,a))
        self.model.setColor(r,g,b,a)

    def updateJumpAnimation(self):
        self.model.setScale(LVecBase3f(2 - 0.5*log2(self.pos[2]- self.groundHeight +4),2 - 0.5*log2(self.pos[2]- self.groundHeight +4),0.5*log2(self.pos[2]- self.groundHeight +4)))

    def updatePos(self):
        self.model.setPos(self.pos)
    def teleport(self,posx,posy,posz):
        self.pos = LVecBase3f(posx,posy,posz)
    
    def initCollisionBox(self):
        # Create a collsion node for this object.
        self.cNode = CollisionNode('slime')
        # Attach a collision sphere solid to the collision node.
        self.cNode.addSolid(CollisionSphere(0,0,0,1))
        # Attach the collision node to the object's model.
        self.slimeC = self.model.attachNewNode(self.cNode)
        # Set the object's collision node to render as visible.
        #self.slimeC.show()


