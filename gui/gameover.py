#Panda3d import
from panda3d.core import TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.task.Timer import Timer
from panda3d.core import Filename

#Util import
import os

#Class import
import slime

MAINDIR = Filename.from_os_specific(os.getcwd())


class Gameover:
    def __init__(self,score):
        self.loadMenu(score)

    def loadMenu(self,score):

        mapsparkour = loader.loadModel("assets/gui/retour_maps")
        self.screen=OnscreenImage(image=str(MAINDIR)+'/assets/gui/gameover_screen.png',pos=(0,0,0),scale=(0.65,0.65,0.65))
        self.screen.setTransparency(1)

        self.font = loader.loadFont(str(MAINDIR)+'/assets/fonts/allerdisplay.ttf')
        self.score = OnscreenText(text="{}".format(score), pos=(0,-0.2),scale=0.15, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font)
    

    def hideMenu(self):
        self.gameover_button.hide()
        self.screen.hide()
        self.score.hide()

    def showMenu(self):
        self.screen.show()
        self.gameover_button.show()
        self.score.show()
