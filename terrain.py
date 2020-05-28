from panda3d.core import *
import random
from worldimage import ProceduralImage

class Terrain():
    def __init__(self,size):
        self.grassbushes = 0
        self.treenumber = 500
        self.grass = {}
        self.trees = {}
        self.biomes = {
            (0,0.4,0):Biome('dark forest',True,100,["assets/models/basic_tree"]),
            (0, 0.6, 0.1):Biome('forest',True,80,["assets/models/basic_tree"]),
            (0, 0.8, 0.3):Biome('prairies',True,50,["assets/models/basic_tree"]),
            (0.5,1,0.2):Biome('lush lands',True,20,["assets/models/basic_tree"]),
            (0.9,1,0.5):Biome('beach',False,0,[""]),
            (0.9, 1, 0.7):Biome('desert',False,0,[""])}
        self.size = size
        self.terrain = CardMaker("myTerrain")

    def load(self):
        self.world = World(self.terrain,self.size)
        self.world.load()
        #self.addWorldTrees()

    def addWorldTrees(self):
        for i in range(self.treenumber):
            biome = ""
            while(True):
                p = random.randint(1,100)
                x = random.randint(-self.size+1,self.size-1)
                y = random.randint(-self.size+1,self.size-1)
                biome = self.getBiome(x,y)
                if(biome.hasTrees()):
                    if(p <= biome.getTreeRate()):
                        break
            model = loader.loadModel(str(biome.getTreeModelPath()))
            scale = random.randint(5,10)
            model.setScale(scale,scale,scale)
            model.setColorScale(0.9, 0.9, 0.9, 1.0)
            model.setPos(x,y,0.1)
            self.trees[(x,y,0)] = model
            model.reparentTo(render)
    

    """ Biome system"""
    def getBiome(self,x,y):
        xel = self.getPixelFromPos(x,y)
        return self.biomes[self.roundNumber(xel[0]),self.roundNumber(xel[1]),self.roundNumber(xel[2])]

    def roundNumber(self,n):
        return float("{0:.2f}".format(n))

    def getPixelFromPos(self,x,y):
        posx = int((x+self.size)/2)
        posy = int((self.size-y)/2)
        try:
            return self.world.pimage.getImage().getXel(posx,posy)
        except AssertionError:
            print("AssertionError, can't find that pixel: ("+str(posx)+","+str(posy)+") with those coords: ("+str(x)+","+str(y)+")")
       
class World():
    def __init__(self,terrain,size):
        self.image = None
        self.terrain = terrain
        self.size = size
        self.pimage = ProceduralImage(size)

    def load(self):
        # Set up the GeoMipTerrain
        self.terrain.setFrame(-self.size,self.size,-self.size,self.size)

        # Store the root NodePath for convenience
        root = NodePath(self.terrain.generate())
        root.reparentTo(render)
        root.setHpr(0,-90,0)
        try:
            root.setShader(Shader.load(Shader.SL_GLSL, "assets/shaders/shader.vert", "assets/shaders/shader.frag"))
        except IOError:
            print("World image not found, create new image.")
            self.pimage.createImage()
            root.setShader(Shader.load(Shader.SL_GLSL, "assets/shaders/shader.vert", "assets/shaders/shader.frag"))

        root.setShaderInput("texInput", loader.loadTexture("assets/texture/perlin.png"))

        # Generate it.
        self.terrain.generate()

class Biome():
    def __init__(self,name, havetrees,treesrate,treesmodelspaths):
        self.name = name
        self.haveTrees = havetrees
        self.treesrate = treesrate
        self.treesmodelpaths = treesmodelspaths

    def hasTrees(self):
        return self.haveTrees

    def getName(self):
        return self.name

    #Between 1 and 100
    def getTreeRate(self):
        return self.treesrate

    def getTreeModelPath(self):
        r = random.randint(0,len(self.treesmodelpaths)-1)
        return self.treesmodelpaths[r]
