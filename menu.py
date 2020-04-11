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
        maps = loader.loadModel("assets/gui/button_play")
        self.title=OnscreenImage(image=str(MAINDIR)+'/assets/gui/title.png',pos=(0,0,0.20),scale=(0.5,0.5,0.125))
        self.title.setTransparency(1)
        self.play_button = DirectButton(
            geom = (maps.find("**/button_ready"),maps.find("**/button_over")),
            frameColor = (0,0,0,0),
            pos = (0,0,-0.40),
            command = base.messenger.send,
            scale = 0.3,
            extraArgs = ["Menu-Start"])
        
    def hideStartMenu(self):
        self.play_button.hide()
        self.title.hide()