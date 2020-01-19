from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from panda3d.core import *

import os
MAINDIR=Filename.fromOsSpecific(os.getcwd())
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # the dt should depend on the framerate
        self.dt = 0.05
        
        # Load the models.
        MODELSDIR = '/models/'
        self.ground = self.loader.loadModel("models/plan")
        startingPoint = (0,0,1)
        self.slime = Slime(startingPoint, str(MAINDIR)+MODELSDIR+"slime.egg", 1)

        # Apply scale and position transforms on the models.
        self.ground.setPos(0,0,0)
        self.ground.setScale(50, 50, 50)

        # Reparent the models to render.
        self.ground.reparentTo(self.render)

        #setting the lights
        self.setLights()
        
        #positionate the camera
        self.cam.setHpr(0,-20,0)
        self.cam.setPos(0,-120,40)

        self.task_mgr.add(self.mainLoop, "MainTask")

    def setLights(self):
        directionalLight = DirectionalLight('directionalLight')
        directionalLightNP = render.attachNewNode(directionalLight)
        directionalLightNP.setHpr(45, -45, 0)
        directionalLight.setColor((2, 2, 2, 1))
        render.setLight(directionalLightNP)

    def mainLoop(self,task):
        self.slime.update(self.dt)
        return task.cont



app = MyApp()
app.run()