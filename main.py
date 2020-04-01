from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from monster import Monster
from panda3d.core import *
from terrain import Terrain
from skybox import Skybox
from direct.filter.CommonFilters import CommonFilters
from panda3d.ai import *
from direct.showbase.DirectObject import DirectObject

class MyApp(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        self.setFrameRateMeter(True)

        # the dt should depend on the framerate
        self.dt = 0.25
        
        # Load Skybox
        Skybox(self.render)
        
        # AI
        self.AIworld = AIWorld(render)

        # Load terrain
        self.terrain = Terrain(1024)
        
        # Load shaders

        # Load the models.
        self.loadEntities()
        self.entities = [self.slime]+Monster.monsters
        self.collision()
        
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

    def loadEntities(self):
        startingPoint = (100, 0, 3)
        #terrain, initialPos, slimeModelPath, scale, lifePoint, volumicMass, movingSpeed
        self.slime = Slime(self.terrain, startingPoint, "assets/models/slime.egg", 2, 100, 0.03, 10) 
        
        for i in range(3, 10):
            #terrain, initialPos, modelPath, movingSpeed, scale, lifePoint, volumicMass, target, aiWorld, detectionDistance, name)
            Monster(self.terrain, (i*10,i*10,1), "assets/models/slime.egg", 100, i+2, (i+1)*100, 100, self.slime, self.AIworld, 300, str(i))

    def collision(self):
        #Initialisation of collision related objet
        base.cTrav = CollisionTraverser()
        #self.collHandEvent = CollisionHandlerEvent()
        #self.collHandEvent.addInPattern('into-%in')
        pusher = CollisionHandlerPusher()
        lifter = CollisionHandlerFloor()

        # Initialisation of list
        self.entitiesNode = []
        self.entitiesFloor = []
        self.entitiesC = []
        """self.collCount = 0"""

        # For all entities
        for i in range(len(self.entities)):
            # Create the node
            self.entitiesNode.append(CollisionNode(str(i)+" entities"))
            # Add solid to the node
            self.entitiesNode[i].addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
            self.entitiesNode[i].addSolid(CollisionRay((0, 0, 0), (0, 0, -1)))
            #
            """
            nodeStr = 'CollisionHull{0}_{1}'.format(self.collCount, self.entitiesNode[i].name)
            self.collCount += 1
            self.accept('into-' + nodeStr, self.collide)
            """
            # Add the nood to collider list
            self.entitiesC.append(self.entities[i].model.attachNewNode(self.entitiesNode[i]))
            # Initialise Collision
            base.cTrav.addCollider(self.entitiesC[i], pusher)
            #base.cTrav.addCollider(self.entitiesC[i], self.collHandEvent)
            pusher.addCollider(self.entitiesC[i], self.entities[i].model, base.drive.node())
            lifter.addCollider(self.entitiesC[i], self.entities[i].model)
    
    def collide():
        print("content")

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
        self.AIworld.update()
        self.slime.update(self.dt)
        for m in Monster.monsters:
            m.update()
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

App = MyApp()
App.run()
