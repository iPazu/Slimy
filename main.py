from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from terrain import Terrain
from skybox import Skybox
from direct.filter.CommonFilters import CommonFilters
from monster import Monster
from slime import Slime
from panda3d.ai import *
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
        self.terrain = Terrain(1024, self.AIworld)
        
        # Load shaders

        # Monster list
        self.monsterList = []

        # Load the models.
        self.loadEntities()
        
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

    def loadEntities(self):
        #terrain, initialPos, slimeModelPath, scale, lifePoint, volumicMass, movingSpeed
        self.slime = Slime(self.terrain, (0,0,1), "assets/models/slime.egg", 5, 1, 0.02, 10)
        #terrain, initialPos, ModelPath, movingSpeed, scale, lifePoint, volumicMass, target, AIworld
        for i in range(10):
            Monster(self.terrain, (i*10,i*10,1), "assets/models/slime.egg", 100, 2, 0.02, 100, self.slime, self.AIworld, 100)
        
        #If you want to loop through the monsters list you can do that (don't forget to import monster class)
        for m in Monster.monsters:
            print(m)


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

    def mainLoop(self,task):
        self.slime.update(self.dt)
        for i in self.monsterList:
            i.update()
        self.AIworld.update()
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

def getMyApp():
    return app
