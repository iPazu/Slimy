#Panda3d import
from panda3d.core import *

#Util import
import os,sys


# these routines are trivial and won't be commented
MAINDIR=Filename.from_os_specific(os.getcwd())
class Skybox:
    def __init__(self,RenderTemplate):
        try:
            self.pic_path=str(MAINDIR)+"/assets/skybox/sky_#.bmp"
            self.mesh_path=str(MAINDIR)+"/assets/models/invertedSphere.egg"
            self.isphere=loader.loadModel(self.mesh_path) #loading skybox structure
            self.isphere.setTwoSided(True)
            self.tex=loader.loadCubeMap(self.pic_path)

            self.isphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)
            self.isphere.setTexProjector(TextureStage.getDefault(), render, self.isphere)
            self.isphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
            self.isphere.setTexScale(TextureStage.getDefault(), .5)
            self.isphere.setTexture(self.tex)
            self.isphere.setLightOff()
            self.isphere.setScale(10000)
            self.isphere.reparentTo(RenderTemplate)
            print("[SKYBOX LOADER]: Setup completed, skybox ready\nFiles used: \n"+str(self.pic_path)+"\n"+str(self.mesh_path))
        except:
            print("[SKYBOX LOADER]: Failed to load skybox, either the sphere mesh or the textures have caused the issue")
        return None
