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

    def getImage(self):
        return self.image