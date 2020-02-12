from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from monster import Monster
from creature import Creature
from panda3d.core import *
from terrain import Terrain

import os
MAINDIR=Filename.fromOsSpecific(os.getcwd())
class MyApp(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)
        self.setFrameRateMeter(True)

        # the dt should depend on the framerate
        self.dt = 0.25
        
        # Load the models.
        MODELSDIR = '/models/'
        startingPoint = (0,0,1)
        self.slime = Slime(startingPoint, str(MAINDIR)+MODELSDIR+"slime.egg", 1, 5, 100, 0.02)
        
        #Load terrain
        self.terrain = Terrain(1024)

        #setting the lights
        self.setLights()
        self.disableMouse()
        #positionate the camera
        self.camera.lookAt(self.slime.model)
        
        self.ydelta = 100
        self.zdelta = 20
        self.accept("wheel_up", self.camzoom,[True])
        self.accept("wheel_down", self.camzoom,[False])


        self.task_mgr.add(self.mainLoop, "MainTask")
        self.task_mgr.add(self.updateCamera, "CameraTask")



    def setLights(self):
        sun = DirectionalLight("sun")
        sun.setColor((1, 1, 1, 1))
        sun.setScene(render)
        self.sunNp = render.attachNewNode(sun)
        self.sunNp.setPos(-10, -10, 30)
        self.sunNp.lookAt(0,0,0)
        render.setLight(self.sunNp)
    
        alight = AmbientLight('alight')
        alight.setColor((0.5, 0.5, 0.5, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

    def mainLoop(self,task):
        self.slime.update(self.dt)
        #self.terrain.getBiome(int(self.slime.getPos()[0]),int(self.slime.getPos()[1]))
        for t in self.terrain.trees.keys():
            if(self.terrain.distance(t,self.slime.getPos()) < 50):
                self.terrain.trees[t].removeNode()
        return task.cont
    def camzoom(self,decrease):
        if(decrease):
            self.ydelta-=5
            self.zdelta-=1
        else:
            self.ydelta+=5
            self.zdelta+=1
    def updateCamera(self,task):
        self.cam.setPos(self.slime.pos.getX(),self.slime.pos.getY()-self.ydelta,self.slime.pos.getZ()+self.zdelta)
        #print("x:"+str(self.camera.getX()-self.slime.pos.getX())+" y:"+str(self.camera.getY()-self.slime.pos.getY())+" z:"+str(self.camera.getZ()))
        #print(self.cam.getHpr())
        self.cam.lookAt(self.slime.model)
        return task.cont

app = MyApp()
app.run()