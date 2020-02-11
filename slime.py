from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from math import log2

class Slime():
    def __init__(self,initialPos, slimeModelPath, floorPos):
        #loading the model
        self.model = loader.loadModel(slimeModelPath)
        self.model.reparentTo(render)
        
        #initialise vectorial stuff
        self.pos = LVecBase3f(initialPos)
        self.pos.set
        self.speed = LVecBase3f(0,0,0) # initialize as static object
        
        #init constants
        self.jumpSpeed = LVecBase3f(0,0,8)
        self.movingSpeed = 15
        
        # environment
        self.groundHeight = floorPos
        self.externalg = LVecBase3f(0,0,-9.81) # const

        # state
        self.is_flying = (self.pos[2] > self.groundHeight)

        #user controls
        self.forward = KeyboardButton.asciiKey("z")
        self.backward = KeyboardButton.asciiKey('s')
        self.left = KeyboardButton.asciiKey('q')
        self.right = KeyboardButton.asciiKey('d')
        self.keymaplist = [self.forward, self.backward, self.left, self.right]

        base.accept('space', self.jump,[self.jumpSpeed])
    
    def update(self,dt):  # dt = time elapsed between the two updates
        self.checkForMovement()
        if (self.pos[2] > self.groundHeight or self.speed[2] >= 0):
            self.updateJumpAnimation()
            self.pos += self.speed*dt
            self.speed += self.externalg*dt
        else:
            self.pos[2] = self.groundHeight
            self.speed = LVecBase3f(0,0,0)

        self.is_flying = (self.pos[2] > self.groundHeight) # status updating
        self.updatePos()

    def checkForMovement(self):
        isDown = base.mouseWatcherNode.isButtonDown
        for x in range(4):
            if(isDown(self.keymaplist[x])):
                if(x < 2): #backward or forward
                    self.speed[1] = self.movingSpeed * (-1)**x
                else:#left or right
                    self.speed[0] = self.movingSpeed * -(-1)**x

    def jump(self, jspeed):
        if not self.is_flying:
            self.speed += jspeed

    def updateJumpAnimation(self):
        self.model.setScale(LVecBase3f(2 - 0.5*log2(self.pos[2]- self.groundHeight +4),2 - 0.5*log2(self.pos[2]- self.groundHeight +4),0.5*log2(self.pos[2]- self.groundHeight +4)))

    
    def updatePos(self):
        self.model.setPos(self.pos)