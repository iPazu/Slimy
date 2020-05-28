from panda3d.core import TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)
from direct.gui.OnscreenImage import OnscreenImage
import os
from panda3d.core import Filename
MAINDIR = Filename.from_os_specific(os.getcwd())
class Menu:
    def __init__(self):
        self.loadStartMenu()

    def loadStartMenu(self):
        base.setBackgroundColor(0,0.25,0.4)
        self.title=OnscreenImage(image=str(MAINDIR)+'/assets/gui/title.png',pos=(0,0,0.20),scale=(0.5,0.5,0.125))
        self.title.setTransparency(1)
        
        mapsparkour = loader.loadModel("assets/gui/parkour_maps")
        mapsworld = loader.loadModel("assets/gui/world_maps")
        mapsranking = loader.loadModel("assets/gui/classement_maps")
        
        self.parkour_button = DirectButton(
            geom = (mapsparkour.find("**/parkour_ready"),mapsparkour.find("**/parkour_over")),
            frameColor = (0,0,0,0),
            pos = (-0.70,0,-0.40),
            command = base.messenger.send,
            scale = 0.35,
            extraArgs = ["Menu-Start-Parkour"])
        self.world_button = DirectButton(
            geom = (mapsworld.find("**/world_ready"),mapsworld.find("**/world_over")),
            frameColor = (0,0,0,0),
            pos = (0.70,0,-0.40),
            command = base.messenger.send,
            scale = 0.35,
            extraArgs = ["Menu-Start-World"])
        self.ranking_button = DirectButton(
            geom = (mapsranking.find("**/classement_ready"),mapsranking.find("**/classement_over")),
            frameColor = (0,0,0,0),
            pos = (0,0,-0.80),
            command = base.messenger.send,
            scale = 0.25,
            extraArgs = ["Menu-Start-Ranking"])
        
    def hideStartMenu(self):
        self.world_button.hide()
        self.ranking_button.hide()
        self.parkour_button.hide()        
        self.title.hide()