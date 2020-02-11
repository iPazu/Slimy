from panda3d.core import *
from math import *
import random


class Terrain():
    def __init__(self,size):
        self.grass = {}
        self.trees = {}
        self.size = size
        self.procedural = ProceduralImage(1024)
        # Set up the GeoMipTerrain
        self.terrain = CardMaker("myTerrain")
        self.terrain.setFrame(-size,size,-size,size)

        # Store the root NodePath for convenience
        root = NodePath(self.terrain.generate())
        root.reparentTo(render)

        root.setHpr(0,-90,0)
        root.setShader(Shader.load(Shader.SL_GLSL, "assets/shaders/shader.vert", "assets/shaders/shader.frag"))
        root.setShaderInput("texInput", loader.loadTexture("assets/texture/map.png"))

        # Generate it.
        self.terrain.generate()
        self.addWorldGrass()
        self.addWorldTrees()

    def addWorldTrees(self):
        for i in range(50):
            x = random.randint(-self.size,self.size)
            y = random.randint(-self.size,self.size)
            model = loader.loadModel("assets/models/tree1")
            model.setScale(5,5,5)
            model.setPos(x,y,0.1)
            self.trees[(x,y,0)] = model
            model.reparentTo(render)

    def addWorldGrass(self):
        for i in range(50):
            self.addBushesOfGrass()

    def addBushesOfGrass(self):
        initx = random.randint(-self.size,self.size)
        inity = random.randint(-self.size,self.size)
        radius = 100.0
        gap = 10
        p= 1
        delta = 0
        x = initx
        y= inity
        while p > 0:
            if(p > 0.5):
                x+= (-1)**(round(p*100))*gap
            else:
                y+= (-1)**(round(p*100))*gap
            distance = self.distance((initx,inity,0),(x,y,0))
            self.addGrassModel(x,y)
            delta = distance/round(random.uniform(1, radius),2)
            p-= delta
            p = float("{0:.2f}".format(p))
    
    def addGrassModel(self,x,y):
        model = loader.loadModel("assets/models/grass")
        greentex = loader.loadTexture('assets/texture/green.jpg')
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
        #self.applyMasks()

        # Smooth out minor imperfections
        self.image.gaussianFilter(10.0)

        #save image
        self.image.write("assets/texture/map.png")
        self.applyMasks()
        self.image.write("assets/texture/mapisland.png")
        print("image generated")

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
                    gradient = delta;
                    self.image.setXel(x,y,self.image.getXel(x,y)-gradient)


    def getImage(self):
        return self.image