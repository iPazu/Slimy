from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from monster import Monster, distance
from panda3d.core import *
from terrain import Terrain
from skybox import Skybox
from direct.filter.CommonFilters import CommonFilters
from panda3d.ai import *

monsterList = []

import os
MAINDIR = str(Filename.fromOsSpecific(os.getcwd()))

class Start():
    def __init__(self):
        self.menu = 1
        self.begin()

    def begin(self):
        app = MyApp()
        app.run()

    def end(self):
        a = 1

class MyApp(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)
        self.setFrameRateMeter(True)

        # the dt should depend on the framerate
        self.dt = 0.25
        
        # Load Skybox
        Skybox(self.render)
        
        # AI
        self.setAI()

        # Load terrain
        self.terrain = Terrain(1024)
        
        # Load shaders

        # Load the models.
        self.loadModels()
        
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
    
    def setAI(self):
        #Create AI world
        self.AIworld = AIWorld(render)

    def loadModels(self):
        MODELSDIR = '/assets/models/'
        startingPoint = (100, 0, 3)
        #terrain, initialPos, slimeModelPath, scale, lifePoint, volumicMass, movingSpeed
        self.slime = Slime(self.terrain, startingPoint, MAINDIR+MODELSDIR+"slime.egg", 2, 100, 0.03, 10) 
        
        for i in range(10):
            #terrain, initialPos, ModelPath, movingSpeed, scale, lifePoint, volumicMass, target, AIworld, detectionDistance, name
            monsterList.append(Monster(self.terrain, (i*10,i*10,1), MAINDIR+MODELSDIR+"slime.egg", 100, i+1, 100, 100, self.slime, self.AIworld, 300, str(i)))

    def setLights(self):
        sun = DirectionalLight("sun")
        sun.setColor((1, 1, 0.9, 1))
        sun.setScene(render)
        self.sunNp = render.attachNewNode(sun)
        self.sunNp.setPos(-10, -10, 30)
        self.sunNp.lookAt(0,0,0)
        render.setLight(self.sunNp)
    
        alight = AmbientLight('alight')
        alight.setColor((0.5, 0.5, 0.5, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

    def gameOver(self):
        start().end

    def mainLoop(self,task):
        if self.slime.live == True:
            self.slime.update(self.dt)
            for i in monsterList:
                i.update()
                if distance(self.slime.pos, i.pos) < self.slime.scale:
                    i.dommage(1000, self.AIworld)
            self.AIworld.update()
        else :
            self.gameOver()
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

start = Start()
start.begin()
