from panda3d.core import *
from math import sqrt
import random
from itertools import product
from panda3d.ai import *

class Terrain():
    def __init__(self,size, AIworld):
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
        self.pimage = ProceduralImage(1024)

        # Set up the GeoMipTerrain
        self.terrain = CardMaker("myTerrain")
        self.terrain.setFrame(-size,size,-size,size)

        # Store the root NodePath for convenience
        root = NodePath(self.terrain.generate())
        root.reparentTo(render)
        #AIworld.addObstacle(root)
        root.setHpr(0,-90,0)
        root.setShader(Shader.load(Shader.SL_GLSL, "assets/shaders/shader.vert", "assets/shaders/shader.frag"))
        root.setShaderInput("texInput", loader.loadTexture("assets/texture/perlin.png"))

        # Generate it.
        self.terrain.generate()
        self.addWorldGrass()
        self.addWorldTrees(AIworld)

    def addWorldTrees(self, AIworld):
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
            AIworld.addObstacle(model)

    def addWorldGrass(self):
        for i in range(self.grassbushes):
            self.addBushesOfGrass()

    def addBushesOfGrass(self):
        radius = random.randint(1,3)
        bushgap = 8
        initx = random.randint(-self.size,self.size)
        inity = random.randint(-self.size,self.size)
        locs = list(self.points_in_circle(radius))
        for l in locs:
            self.addGrassModel(initx+l[0]*bushgap,inity+l[1]*bushgap)
        
    def points_in_circle(self,radius):
        for x, y in product(range(int(radius) + 1), repeat=2):
            if x**2 + y**2 <= radius**2:
                yield from set(((x, y), (x, -y), (-x, y), (-x, -y),))
                
    def addGrassModel(self,x,y):
        model = loader.loadModel("assets/models/grass")
        greentex = loader.loadTexture('assets/texture/green.png')
        model.setTexture(greentex, 1)
        model.setScale(5,5,1.5)
        model.setPos(x,y,0.1)
        self.grass[(x,y,0)] = model
        model.reparentTo(render)

    def distance(self,ip,cp):
        x = abs(ip[0]-cp[0])
        y = abs(ip[1]-cp[1])
        z = abs(ip[2]-cp[2])
        return sqrt(x**2+y**2+z**2)
    
    def getBiome(self,x,y):
        xel = self.getPixelFromPos(x,y)
        return self.biomes[self.roundNumber(xel[0]),self.roundNumber(xel[1]),self.roundNumber(xel[2])]

    def roundNumber(self,n):
        return float("{0:.2f}".format(n))
    def getPixelFromPos(self,x,y):
        posx = int((x+self.size)/2)
        posy = int((self.size-y)/2)
        try:
            return self.pimage.getImage().getXel(posx,posy)
        except AssertionError:
            print("AssertionError, can't find that pixel: ("+str(posx)+","+str(posy)+") with those coords: ("+str(x)+","+str(y)+")")
       

    
class ProceduralImage():
    def __init__(self,size):
        self.image = PNMImage(size,size)
        #self.image.read("texture/noise_simplexe")
        self.sizex = size
        self.sizey = size
        self.perlinNoise = StackedPerlinNoise2()

        self.addFrequency(0.32)
        self.addFrequency(0.16)
        self.addFrequency(0.08)
        

        self.image.perlinNoiseFill(self.perlinNoise)
        #save image
        self.image.write("assets/texture/perlin.png")

        self.applyMasks()

        # Smooth out minor imperfections
        #self.image.gaussianFilter(10.0)

        #save image
        self.image.write("assets/texture/mapisland.png")
        print("map image generated, size: "+str(size)+"x"+str(size))

    def addFrequency(self,scale):
        perlin = PerlinNoise2()
        perlin.setScale(scale)
        self.perlinNoise.addLevel(perlin)

    def applyMasks(self):
            # This method is obsolete, Used just for the map preview
            for x in range(self.sizex):
                for y in range(self.sizey):
                    distance_x = x - self.sizex * 0.5;
                    distance_y = y - self.sizey * 0.5;
                    distance = sqrt(distance_x**2 + distance_y**2);
                    max_width = sqrt(self.sizex**2+self.sizey**2) * 0.5 - 5.0;
                    delta = distance / max_width;
                    gradient = delta*delta;
                    self.image.setXel(x,y,self.image.getXel(x,y)-gradient)
                    value = self.image.getXel(x,y)
                    if (value > 0.75):
                        self.image.setXel(x,y,0,0.4,0)
                    elif(value > 0.50):
                        self.image.setXel(x,y,0, 0.6, 0.1)
                    elif (value > 0.30):
                        self.image.setXel(x,y,0, 0.8, 0.3)
                    elif(value > 0.15): 
                        self.image.setXel(x,y,0.5,1,0.2)
                    elif (value > 0.05): 
                        self.image.setXel(x,y,0.9,1,0.5)
                    else:
                        self.image.setXel(x,y,0.9, 1, 0.7)
                

    def getImage(self):
        return self.image

    def getPixel(self,x,y):
        return self.image.getXel(x,y)

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