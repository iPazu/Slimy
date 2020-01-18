from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from slime import Slime
from panda3d.core import *

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the models.
        self.scene = self.loader.loadModel("models/plan")
        self.slime = Slime()

        self.scene.setPos(0,0,-1)

        # Reparent the models to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the models.
        self.scene.setScale(10, 10, 10)

        #setting the lights
        directionalLight = DirectionalLight('directionalLight')
        directionalLightNP = render.attachNewNode(directionalLight)
        directionalLightNP.setHpr(45, -45, 0)
        directionalLight.setColor((2, 2, 2, 1))
        render.setLight(directionalLightNP)


app = MyApp()
app.run()