from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from panda3d.core import *
from terrain import Terrain

import os
MAINDIR=Filename.fromOsSpecific(os.getcwd())
class MyApp(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)

        # the dt should depend on the framerate
        self.dt = 0.05
        
        # Load the models.
        self.slime = Slime((0,0,1),"models\slime.egg", 1)

        #Load terrain
        terrain = Terrain(500)

        #setting the lights
        self.setLights()
        
        #positionate the camera

        self.task_mgr.add(self.mainLoop, "MainTask")


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
        return task.cont

    def updateCamera(self,task):
    
        self.cam.setPos(self.slime.pos.getX(),self.slime.pos.getY()-30,self.slime.pos.getZ()+85)
        self.cam.lookAt(self.slime.model)
        return task.cont



app = MyApp()
app.run()