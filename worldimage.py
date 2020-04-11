from panda3d.core import *
from math import *
class ProceduralImage():
    def __init__(self,size):
        self.sizex = size
        self.sizey = size
        self.image = PNMImage(size,size)
        try:
            print("reading image")
            self.image.read("assets/texture/perlin.png")
        except IOError:
            print("creating image")
            self.createImage()
        self.applyMasks()
    def createImage(self):
        self.perlinNoise = StackedPerlinNoise2()
        self.addFrequency(0.32)
        self.addFrequency(0.16)
        self.addFrequency(0.08)
        
        self.image.perlinNoiseFill(self.perlinNoise)
        #save image
        self.image.write("assets/texture/perlin.png")

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


