from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Slime():
    def __init__(self,):
        charPath = "models/"
        self.model = loader.loadModel(charPath+"slime.egg")
        self.model.reparentTo(render)
        
        self.posx = 0
        self.posy = 0
        self.posz = 0

        self.direction = LVecBase3f(0,0,0)
        self.velocity = LVecBase3f(0,0,0)
        self.acceleration = LVecBase3f(-0.1,-0.1,-0.1)

        self.velocityincrementer = 0.1
        self.state = 'ground'
        

        self.forward = KeyboardButton.asciiKey("z")
        self.backward = KeyboardButton.asciiKey('s')
        self.left = KeyboardButton.asciiKey('q')
        self.right = KeyboardButton.asciiKey('d')

        base.accept('space', self.jump)
        
        taskMgr.add(self.moveTask,"MoveTask")
        print('slime loaded')
    
    def moveTask(self,task):
        isDown = base.mouseWatcherNode.isButtonDown
        if(isDown(self.forward)):
            self.velocity.addY(self.velocityincrementer)
            self.direction.setY(1)

        if(isDown(self.backward)):
            self.velocity.addY(self.velocityincrementer)
            self.direction.setY(-1)

        if(isDown(self.left)):
            self.velocity.addX(self.velocityincrementer)
            self.direction.setX(-1)

        if(isDown(self.right)):
            self.velocity.addX(self.velocityincrementer)
            self.direction.setX(1)


        self.posx += self.direction.getX()*self.velocity.getX()
        self.posy += self.direction.getY()*self.velocity.getY()
        self.posz += self.velocity.getZ()

        

        if(self.velocity.getX != 0):
            self.velocity.addX(self.acceleration.getX())
            self.updatePos()
            if(self.velocity.getX() < 0):
                self.velocity.setX(0)

        if(self.velocity.getY != 0):
            self.velocity.addY(self.acceleration.getY())
            self.updatePos()
            if(self.velocity.getY() < 0):
                self.velocity.setY(0)

        if(self.velocity.getZ != 0):
            self.velocity.addZ(self.posz*self.acceleration.getZ())
            self.updatePos()
            if(self.velocity.getZ() < 0 and self.posz <= 0):
                self.velocity.setZ(0)
                self.posz = 0


        return task.cont
    
    def jump(self):
        self.velocity.addZ(1)

        
    def updatePos(self):
        self.model.setPos(self.posx,self.posy,self.posz)