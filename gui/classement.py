from panda3d.core import TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
import os
from panda3d.core import Filename
MAINDIR = Filename.from_os_specific(os.getcwd())

class Classement:
    def __init__(self,ranking):
        self.ranking = ranking
        self.loadMenu()

    def loadMenu(self):
        base.setBackgroundColor(0,0.25,0.4)

        self.font = loader.loadFont(str(MAINDIR)+'/assets/fonts/allerdisplay.ttf')
        self.font.setPixelsPerUnit(150)
        self.title = OnscreenText(text="Classement", pos=(0,0.75),scale=0.25, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font)

        mapsparkour = loader.loadModel("assets/gui/retour_maps")
        self.retour_button = DirectButton(
            geom = (mapsparkour.find("**/retour_ready"),mapsparkour.find("**/retour_ready")),
            frameColor = (0,0,0,0),
            pos = (-1.5,-1,-0.90),
            command = base.messenger.send,
            scale = 0.25,
            extraArgs = ["Menu-Ranking-Return"])

        self.createPlayerRankingDisplay()

        

    def createPlayerRankingDisplay(self):
        self.ranking_plates = []
        z = 0.70
        for r in self.ranking:
            z-=0.32
            ranking=OnscreenImage(image=str(MAINDIR)+'/assets/gui/classement_template.png',pos=(0,0,z),scale=(1.5,1,0.15))
            ranking.setTransparency(1)
            nametext = OnscreenText(text=r[0], pos=(-1.15,z-0.035),scale=0.1, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font)
            scoretext = OnscreenText(text="Score: {}".format(r[1]), pos=(-0.1,z-0.035),scale=0.1, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font)
            datetext = OnscreenText(text=''.join(r[2]), pos=(1,z-0.035),scale=0.1, fg=(1, 1, 1, 1), align=TextNode.ACenter,font= self.font)
            self.ranking_plates.append([ranking,nametext,scoretext,datetext])

    def hideMenu(self):
        self.title.hide()
        self.retour_button.hide()
        for r in self.ranking_plates:
            for i in r:
                i.hide()
    def showMenu(self):
        self.title.show()
        self.retour_button.show()
        for r in self.ranking_plates:
            for i in r:
                i.show()