from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from monster import Monster
from panda3d.core import *
from terrain import Terrain
from skybox import Skybox
from direct.filter.CommonFilters import CommonFilters
from panda3d.ai import *
from panda3d.physics import *
from menu import Menu
import sys
import time
from cuboid import Cuboid
from module import Module
import pconsole as pc
class MyApp(ShowBase):
    def __init__(self):
        self.debug = True
        ShowBase.__init__(self)

        # the dt should depend on the framerate
        self.dt = 0.25

        #initiate game state
        self.state = 'Menu'
        self.terrain = Terrain(1024)
        self.loadMenu()

        if(self.debug == False):
            self.disableMouse()
        
    def loadMenu(self):
        self.accept("Menu-Start-Parkour", self.loadGame,['parkour'])
        self.accept("Menu-Start-World", self.loadGame,['world'])
        self.menu = Menu()
        self.show_cursor()
    def exitMenu(self):
        self.ignore("Menu-Start")
        self.ignore("Menu-World")
        self.ignore("Menu-Quit")
        self.menu.hideStartMenu()
        
    def loadGame(self,gamemode):
        self.exitMenu()
        self.gamemode = gamemode
        print("Loading game")
        self.state = 'Loading'
        
        if(self.debug == False):
            self.hide_cursor
        self.setLights()

        self.terrain.load()
            
        
        self.loadEntities()

        #positionate the camera
        if(self.debug == False):
            self.camera.lookAt(self.slime.model)
        # Load Skybox
        Skybox(self.render)

        # AI
        self.AIworld = AIWorld(render)

        #register events
        self.ydelta = 100
        self.zdelta = 20
        self.accept("wheel_up", self.camzoom,[True])
        self.accept("wheel_down", self.camzoom,[False])

        #register tasks
        self.task_mgr.add(self.mainLoop, "MainTask")
        if(self.debug == False):
            self.task_mgr.add(self.updateCamera, "CameraTask")
        self.startGame()

    def startGame(self):
        print("Starting game")
        self.setFrameRateMeter(True)
        self.state = 'Game'
        
        #init console
        self.userConsole = pc.Console()
        commands = {"restart":self.__init__,
                    "teleport": self.slime.teleport,
                    "color": self.slime.setColor
                    }
        self.userConsole.create(commands,app=self)

    def loadEntities(self):
        startingPoint = (100, 0, 3)
        c = Cuboid((0,0,20),(20,120,20))
        c.show()
        #terrain, initialPos, slimeModelPath, scale, lifePoint, volumicMass, movingSpeed
        self.slime = Slime(self.terrain, startingPoint, "assets/models/new_slime.egg", 2, 100, 0.03, 10) 
        c.addCollisionTo(self.slime.slimeC,self.slime.model)
        #for i in range(10):
            #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name)
            #Monster(self.terrain, (i*10,i*10,1), "assets/models/slime.egg", 100, i+1, (i+1)*100, 100, self.slime, self.AIworld, 300, str(i))

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
        if(self.state != 'Game'):
            return
        self.AIworld.update()
        self.slime.update(self.dt)
        for m in Monster.monsters:
            m.update()
        #self.collision.update()
        return task.cont

    def camzoom(self,decrease):
        if(decrease):
            self.ydelta-=5
            self.zdelta-=1
        else:
            self.ydelta+=5
            self.zdelta+=1

    def updateCamera(self,task):
        if(self.state != 'Game'):
            return
        self.cam.setPos(self.slime.pos.getX(),self.slime.pos.getY()-self.ydelta,self.slime.pos.getZ()+self.zdelta)
        #print("x:"+str(self.camera.getX()-self.slime.pos.getX())+" y:"+str(self.camera.getY()-self.slime.pos.getY())+" z:"+str(self.camera.getZ()))
        #print(self.cam.getHpr())
        self.cam.lookAt(self.slime.model)
        return task.cont
    
    def hide_cursor(self):
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
    def show_cursor(self):
        """set the Cursor visible again"""
        props = WindowProperties()
        props.setCursorHidden(False)
        x11 = "assets/gui/Cursor.x11"
        win = "assets/gui/Cursor.ico"
        if sys.platform.startswith("linux"):
            props.setCursorFilename(x11)
        else:
            props.setCursorFilename(win)
        self.win.requestProperties(props)

    
App = MyApp()
App.run()
