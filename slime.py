from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Slime():
    def __init__(self,):
        charPath = "models/"
        self.model = loader.loadModel(charPath+"slime.egg")
        self.model.reparentTo(render)

        self.pos = LVecBase3f(0,0,0)
        self.velocity = LVecBase3f(0,0,0)
        self.acceleration = LVecBase3f(0,0,-0.981)

        self.movingspeed = 0.1
        self.jumpingspeed = 0.5
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
            self.posy+=self.movingspeed
            self.updatePos()

        if(isDown(self.backward)):
            self.posy-=self.movingspeed
            self.updatePos()

        if(isDown(self.left)):
            self.posx-=self.movingspeed
            self.updatePos()

        if(isDown(self.right)):
            self.posx+=self.movingspeed
            self.updatePos()
        return task.cont
    
    def jump(self):
        if(self.state == 'ground'):
            self.state = 'jumping'
            taskMgr.add(self.jumpTask,'JumpTask')

    def jumpTask(self,task):
        animationspeed = 10
        if(task.frame == 2*animationspeed):
            self.state = 'ground'
            return task.done
        if(task.frame == animationspeed):
            self.state = 'falling'
        
        if(self.state == 'jumping'):
            self.posz+=self.jumpingspeed
        elif(self.state == 'falling'):
            self.posz-=self.jumpingspeed
        self.updatePos()
        return task.cont
        
    def updatePos(self):
        self.model.setPos(self.pos.x,self.posy,self.posz)