from panda3d.core import CardMaker
from panda3d.core import StackedPerlinNoise2
from panda3d.core import PerlinNoise2
from panda3d.core import PNMImage
from panda3d.core import Filename
from panda3d.core import Shader
from panda3d.core import NodePath
import time
from math import sqrt

class Terrain():
    def __init__(self,size):
        self.procedural = ProceduralImage(1024)
        # Set up the GeoMipTerrain
        self.terrain = CardMaker("myTerrain")
        self.terrain.setFrame(-size,size,-size,size)

        # Store the root NodePath for convenience
        root = NodePath(self.terrain.generate())
        root.reparentTo(render)

        root.setHpr(0,-90,0)
        root.setShader(Shader.load(Shader.SL_GLSL, "shaders/shader.vert", "shaders/shader.frag"))
        root.setShaderInput("texInput", loader.loadTexture("texture/map.png"))

        # Generate it.
        self.terrain.generate()

class ProceduralImage():
    def __init__(self,size):
        self.image = PNMImage(size,size)
        #self.image.read("texture/noise_simplexe")
        self.sizex = size
        self.sizey = size
        self.perlinNoise = StackedPerlinNoise2()

        self.addFrequency(0.48)
        self.addFrequency(0.22)
        self.addFrequency(0.14)
        self.addFrequency(0.18)

        self.image.perlinNoiseFill(self.perlinNoise)
        #self.applyMasks()

        # Smooth out minor imperfections
        self.image.gaussianFilter(10.0)

        #save image
        self.image.write("texture/map.png")
        print("image generated")

    def addFrequency(self,scale):
        perlin = PerlinNoise2()
        perlin.setScale(scale)
        self.perlinNoise.addLevel(perlin)

    def applyMasks(self):
        # This method is obsolete, I've moved this math into the shader.
        for x in range(self.sizex):
            for y in range(self.sizey):
                distance_x = x - self.sizex * 0.5;
                distance_y = y - self.sizey * 0.5;
                distance = sqrt(distance_x**2 + distance_y**2);
                max_width = sqrt(self.sizex**2+self.sizey**2) * 0.5 - 5.0;
                delta = distance / max_width;
                gradient = delta * delta;
                self.image.setXel(x,y,self.image.getXel(x,y)-gradient**2)

    def getImage(self):
        return self.image