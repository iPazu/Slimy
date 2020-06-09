#Panda3d import
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectWaitBar, DGG
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from panda3d.core import Filename
import os
MAINDIR = Filename.from_os_specific(os.getcwd())


class Hud(DirectObject):
    def __init__(self):
        self.lifeBar = DirectWaitBar(
            value = 100,
            barColor = (0, 1, 0.20, 1),
            barRelief = DGG.RAISED,
            relief = DGG.RIDGE,
            frameColor = (0.8,0.05,0.10,1),
            frameSize = (-1.2, 0, 0, -0.1),
            pos = (-0.2,0,base.a2dTop))
        self.lifeBar.setTransparency(1)        
        
        self.font = loader.loadFont(str(MAINDIR)+'/assets/fonts/allerdisplay.ttf')

        self.score_text = OnscreenText(text="Score:", pos=(-1.6,0.93),scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font,mayChange= False)
        self.score = OnscreenText(text="0", pos=(-1.6,0.83),scale=0.07, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font,mayChange= True)

        self.accept("hud_setLifeBarValue", self.setLifeBarValue)
        self.hide()

    def show(self):
        self.lifeBar["value"] = 100
        self.lifeBar.show()

    def hide(self):
        self.lifeBar.hide()

    def setScore(self,score):
        self.score.setText(str(score))

    def setLifeBarValue(self, newValue):
        self.lifeBar["value"] = newValue