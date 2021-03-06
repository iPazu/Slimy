#Panda3d import
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

#Util import
from math import log2, sqrt, atan2, degrees
import time

#Class import
from entity import Entity
from projectile import Projectile


class Slime(Entity):

    slime = []

    def __init__(self, terrain, initialPos, slimeModelPath, floorPos, scale, lifePoint, volumicMass, movingSpeed, dt, name, collision):

        #initialise parent stuff
        Entity.__init__(self, terrain, initialPos, slimeModelPath, floorPos, movingSpeed, scale, lifePoint, volumicMass, name)

        #init constants
        self.jumpSpeed = LVecBase3f(0, 0, 11)
        self.dashSpeed = 15
        self.collision = collision

        #user controls
        self.forward = KeyboardButton.asciiKey("z")
        self.backward = KeyboardButton.asciiKey('s')
        self.left = KeyboardButton.asciiKey('q')
        self.right = KeyboardButton.asciiKey('d')
        self.e = KeyboardButton.asciiKey('e')
        self.a = KeyboardButton.asciiKey('a')

        base.accept("mouse1",self.loadshoot)
        base.accept("mouse1-up",self.shoot)

        self.keymaplist = [self.forward, self.backward, self.right, self.left]
        self.dashT0 = 0
        self.projectileT0 = 0
        self.dashDelay = 5
        self.projectileDelay = 0.5
        self.dt = dt
        self.angle = 0

        
        self.shooting_charge_time = 0
        self.loading_shoot = False


        base.accept('space', self.jump, [self.jumpSpeed])
        Slime.slime.append(self)
        self.collision.addColliderObject(self)

    def update(self):  # dt = time elapsed between the two updates
        self.checkForMovement()
        self.pos += self.speed*self.dt
        if (self.is_flying == True or self.speed[2] >= 0):
            #self.updateJumpAnimation()  
            self.speed += self.externalg*self.dt
        else:
            self.pos[2] = self.groundHeight

        sign = lambda x: (1, -1)[x < 0]
        for i in range(2):
            if self.speed[i] != 0:
                self.speed[i] = self.speed[i] - sign(self.speed[i])*5 if (self.speed[i] > 5) else  0

        self.is_flying = (self.pos[2] > self.groundHeight) # status updating
        for p in Projectile.projectile:
            p.update()
        self.updatePos()

    def checkForMovement(self):
        isDown = base.mouseWatcherNode.isButtonDown
        self.updateHpr()
        for x in range(4):
            if(isDown(self.keymaplist[x])):
                movingIncrementer = self.movingSpeed
                if(isDown(self.e)):
                    if int(round(time.time())) - self.dashT0 > self.dashDelay:
                        movingIncrementer = self.dashSpeed*50
                        self.dashT0 = int(round(time.time()))
                if(x < 2): #backward or forward
                    self.speed[1] = movingIncrementer * (-1)**x
                else: #left or right
                    self.speed[0] = movingIncrementer * (-1)**x


    def loadshoot(self):
        t = int(round(time.time() * 20)) - self.projectileT0
        if(self.projectileDelay < t):
            self.shooting_charge_time = int(round(time.time() * 20))
            self.movingSpeed = 2.5
            self.loading_shoot = True

    def shoot(self):
        if(self.loading_shoot == True):
            damage = int(round(time.time() * 20))-self.shooting_charge_time
            Projectile(self.angle-90, self.pos, self.scale, damage)
            self.collision.projectileInit(Projectile.projectile[len(Projectile.projectile)-1])
            self.projectileT0 = int(round(time.time() * 20))
            self.status = False
            self.movingSpeed = 10
        
        
    
    def jump(self, jspeed):
        if not self.is_flying:
            self.playSound("jump.ogg",0.5)
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
            self.angle = degrees(atan2(y, x))+90
            self.Hpr = (self.angle, 0, 0)
            self.model.setHpr(self.Hpr)

    def teleport(self,posx,posy,posz):
        self.pos = LVecBase3f(posx,posy,posz)

    def setColor(self,r,g,b,a):
        print("Changing color of the slime with colors {} {} {} {}".format(r,g,b,a))
        self.model.setColor(r,g,b,a)

