from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectWaitBar, DGG
from panda3d.core import TextNode

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

        self.accept("hud_setLifeBarValue", self.setLifeBarValue)
        self.hide()

    def show(self):
        self.lifeBar["value"] = 100
        self.lifeBar.show()

    def hide(self):
        self.lifeBar.hide()

    def setLifeBarValue(self, newValue):
        self.lifeBar["value"] = newValue