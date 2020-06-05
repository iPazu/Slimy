from math import cos, sin
from panda3d.core import *

class Projectile():

    projectile = []
    count = 0

    def __init__(self, angle, initialPos, scale, damage):
        self.model = loader.loadModel("assets/models/projectile.egg")
        self.model.reparentTo(render)
        size = damage//5
        if size < 5:
            size = 5
        if size > 30:
            size = 30
        self.model.setScale(size)
        self.pos = LVecBase3f(initialPos)
        self.pos[2] -= scale//2
        self.angle = angle*3.14/180
        self.Xincrement = cos(self.angle)*6
        self.Yincrement = sin(self.angle)*6
        self.model.setHpr(angle, 0, 90)
        self.name = "projectile"
        #self.pos[0], self.pos[1] = self.pos[0]+scale*cos(self.angle)//5, self.pos[1]*sin(self.angle)//5
        self.model.setPos(self.pos)
        self.damage = damage
        Projectile.projectile.append(self)
        self.music = base.loader.loadSfx("assets/sounds/bubble.mp3")
        self.music.play()
        self.music.setVolume(0.05)

    def destroy(self,):
        self.model.removeNode()
        Projectile.projectile.remove(self)

    def update(self,):
        self.pos[0] += self.Xincrement
        self.pos[1] += self.Yincrement
        self.model.setPos(self.pos)
        if self.pos[0] > 1024 or self.pos[0] < -1024 or self.pos[1] > 1024 or self.pos[1] < -1024:
            self.destroy()
