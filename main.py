from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from monster import Monster
from entity import Entity
from collision import Collision, distance
from panda3d.core import *
from terrain import Terrain
from skybox import Skybox
from direct.filter.CommonFilters import CommonFilters
from panda3d.ai import *
from gui.menu import Menu
from spawn import Spawn
import sys
from panda3d.core import WindowProperties
from panda3d.physics import *
from cuboid import Cuboid
import pconsole as pc
from gui.classement import Classement
from database import Database
from gui.gameover import Gameover
import os
import getpass
from gui.hud import Hud
from datetime import datetime as date

class MyApp(ShowBase):

    def __init__(self):
        self.debug = False
        ShowBase.__init__(self)

        # the dt should depend on the framerate
        self.dt = 0.25

        self.database = Database()
        self.ranking = self.database.getRankingFromDatabase()

        #initiate game state
        self.state = 'Menu'
        self.terrain = Terrain(1024)
        self.classement = Classement(self.ranking)
        self.classement.hideMenu()

        self.menu = Menu()
        self.loadStartMenu()

        if(self.debug == False):
            self.disableMouse()
        
    def loadStartMenu(self):
        self.accept("Menu-Start-Parkour", self.loadGame)
        self.accept("Menu-Start-World", self.loadGame)
        self.accept("Menu-Start-Ranking", self.loadRankingMenu)

        self.menu.showStartMenu()
        self.show_cursor()

    def exitStartMenu(self):
        self.ignore("Menu-Start-Ranking")
        self.ignore("Menu-Start-World")
        self.ignore("Menu-Start-Parkour")
        self.menu.hideStartMenu()

    def loadGameOverMenu(self,score):
        self.gameover = Gameover(score)
        taskMgr.doMethodLater(5, self.restartGame,'timer')
        self.show_cursor()

    def loadRankingMenu(self):
        self.accept("Menu-Ranking-Return", self.exitRankingMenu)
        self.exitStartMenu()
        self.classement.showMenu()
        
        self.show_cursor()

    def exitRankingMenu(self):
        print("hidding ranking menu")
        self.ignore("Menu-Ranking-Return")
        self.classement.hideMenu()
        self.loadStartMenu()
        
    def loadGame(self):
        self.exitStartMenu()
        print("Loading game")
        self.state = 'Loading'
        
        if(self.debug == False):
            self.hide_cursor
        self.setLights()

        self.terrain.load()
        self.hud = Hud()
        self.hud.show()
        self.loadEntities()

        #positionate the camera
        if(self.debug == False):
            self.camera.lookAt(self.slime.model)
        # Load Skybox
        Skybox(self.render)

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
        #Load music
        self.music = base.loader.loadSfx("assets/sounds/hytale-ost-kweebec-village.mp3")
        self.music.play()
        self.music.setVolume(0.1)

        self.setFrameRateMeter(True)
        self.state = 'Game'
        
        #init console
        """
        self.userConsole = pc.Console()
        commands = {"restart":self.__init__,
                    "teleport": self.slime.teleport,
                    "color": self.slime.setColor,
                    "stop": self.endGame
                    }
        self.userConsole.create(commands,app=self)
        """
        
    def endGame(self):
        self.state = 'Finished'
        print("SCORE : "+str(Monster.score))
        self.loadGameOverMenu(Monster.score)
        today = date.today()
        name = getpass.getuser()
        self.database.insertValues(name.capitalize(),Monster.score,today.strftime("%d/%m/%Y"))

    def restartGame(self,task):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def loadEntities(self):
        startingPoint = (100, 0, 10)
        #AI
        self.AIworld = AIWorld(render)
        self.collision = Collision(Monster.monster)
        #terrain, initialPos, slimeModelPath, floorPos, scale, lifePoint, volumicMass, movingSpeed, dt
        self.slime = Slime(self.terrain, startingPoint, "assets/models/new_slime.egg", 10, 10, 100, 0.01, 10, self.dt, "slime", self.collision) 
        self.spawn = Spawn([self.slime]+Monster.monster, self.terrain, self.AIworld, self.collision)
        self.spawn.spawn()

    def setLights(self):
        sun = DirectionalLight("sun")
        sun.setColor((1, 1, 0.9, 1))
        sun.setScene(render)
        self.sunNp = render.attachNewNode(sun)
        self.sunNp.setPos(-10, -10, 30)
        self.sunNp.lookAt(0,0,0)
        render.setLight(self.sunNp)
    
        alight = AmbientLight('alight')
        alight.setColor((0.35, 0.35, 0.35, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

    def mainLoop(self,task):
        if(self.state == "Finished"):
            return
        if(self.slime.lifePoint <= 0 or self.slime.scale >= 1000):
            self.endGame()
        self.AIworld.update()
        self.spawn.spawn()
        for e in [self.slime]+Monster.monster:
            e.update()
        self.hud.setLifeBarValue(self.slime.lifePoint)
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
        self.win.requestProperties(props)

    def setFullscreen(self):
            base.win.clearRejectedProperties()
            props = WindowProperties()
            props.setFullscreen(True)
            props.setSize(self.dispWidth, self.dispHeight)
            base.win.requestProperties(props)
            winSize = ConfigVariableString("win-size")
            winSize.setValue("{} {}".format(self.dispWidth, self.dispHeight))
            fullscreen = ConfigVariableBool("fullscreen")
            fullscreen.setValue(True)
            self.taskMgr.step()
            aspectRatio = self.dispWidth / self.dispHeight
            self.adjustWindowAspectRatio(aspectRatio)

App = MyApp()
App.run()