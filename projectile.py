#Panda3d import
from panda3d.core import *

#Util import
import platform
from math import cos, sin
import random


class Projectile():

    projectile = []
    count = 0

    def __init__(self, angle, initialPos, scale, damage):
        # Load model
        if random.randint(0, 100) != 0:
            self.model = loader.loadModel("assets/models/projectile2.egg")
        else:
            self.model = loader.loadModel("assets/models/alien.egg")
        self.model.reparentTo(render)
        # Size
        self.size = damage//5
        if self.size < 5:
            self.size = 5
        if self.size > 30:
            self.size = 30
        self.model.setScale(self.size)
        # Pos
        self.pos = LVecBase3f(initialPos)
        self.pos[2] = 3/4*scale
        self.angle = angle*3.14/180
        self.Xincrement = cos(self.angle)*6
        self.Yincrement = sin(self.angle)*6
        self.pos[0] += cos(self.angle)*scale
        self.pos[1] += sin(self.angle)*scale
        self.model.setPos(self.pos)
        # Name
        self.name = "projectile"
        # Damage
        self.damage = damage
        # Add to list
        Projectile.projectile.append(self)
        # Music lauch
        self.playSound("bubble.ogg",0.2)
    def destroy(self):
        self.model.removeNode()
        Projectile.projectile.remove(self)

    def update(self):
        self.pos[0] += self.Xincrement
        self.pos[1] += self.Yincrement
        self.model.setPos(self.pos)
        if self.pos[0] > 1024 or self.pos[0] < -1024 or self.pos[1] > 1024 or self.pos[1] < -1024:
            self.destroy()
    
    def playSound(self,name,volume):
        sound = base.loader.loadSfx("assets/sounds/"+name)
        sound.play()
        sound.setVolume(volume)
