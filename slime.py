from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from entity import Entity
from math import log2, sqrt, atan2, degrees
import time

class Slime(Entity):

    def __init__(self, terrain, initialPos, slimeModelPath, floorPos, scale, lifePoint, volumicMass, movingSpeed, dt):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos, slimeModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass)

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
        self.dt = dt

        base.accept('space', self.jump,[self.jumpSpeed])

    def update(self):  # dt = time elapsed between the two updates
        self.checkForMovement()
        self.pos += self.speed*self.dt
        if (self.is_flying == True or self.speed[2] >= 0):
            #self.updateJumpAnimation()  
            self.speed += self.externalg*self.dt
        else:
            self.pos[2] = self.groundHeight
        if self.speed[0] != 0 and self.speed[0] > 0:
            self.speed[0] -= 5
        if self.speed[0] != 0 and self.speed[0] < 0:
            self.speed[0] += 5
        if self.speed[1] != 0 and self.speed[1] > 0:
            self.speed[1] -= 5
        if self.speed[1] != 0 and self.speed[1] < 0:
            self.speed[1] += 5
        self.is_flying = (self.pos[2] > self.groundHeight) # status updating
        self.updatePos()

    def checkForMovement(self):
        isDown = base.mouseWatcherNode.isButtonDown
        self.updateHpr()
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
    
    def updateJumpAnimation(self):
        self.model.setScale(LVecBase3f(2 - 0.5*log2(self.pos[2]- self.groundHeight +4),2 - 0.5*log2(self.pos[2]- self.groundHeight +4),0.5*log2(self.pos[2]- self.groundHeight +4)))

    def updatePos(self):
        self.model.setPos(self.pos)

    def damage(self, damage):
        self.lifePoint -= damage

    def remove(self):
        self.model.removeNode()

    def updateHpr(self):
        mw = base.mouseWatcherNode
        if mw.hasMouse():
            x, y = mw.getMouse()
            angle = degrees(atan2(y, x))
            self.Hpr = (angle+90, 0, 0)
            self.model.setHpr(self.Hpr)

    def setColor(self,r,g,b,a):
        print("Changing color of the slime with colors {} {} {} {}".format(r,g,b,a))
        self.model.setColor(r,g,b,a)

    def teleport(self,posx,posy,posz):
        self.pos = LVecBase3f(posx,posy,posz)
