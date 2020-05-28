from panda3d.core import *
class Cuboid():
    def __init__(self,pos,scale):
        self.parts =  [] 
        self.pos = LVecBase3f(pos)
        self.scale = scale
        self.createCuboid()
        self.initCollisions()


    def createCuboid(self):
        for i in range(6):
            m = loader.loadModel("assets/models/plan.egg")
            if(i == 0):
                self.model = m
            if(i < 2):
                m.setScale((self.scale[0],self.scale[1],1))
            elif(i < 4):
                m.reparentTo(self.model)   
                m.setScale((self.scale[2],self.scale[1],1))
                m.setHpr(0,0,90)
            else:
                m.reparentTo(self.model)   
                m.setScale((self.scale[0],self.scale[2],1))
                m.setHpr(0,90,0)

            m.reparentTo(render)
            self.parts.append(m)
        print(self.pos)
        self.parts[0].setPos(self.getCoordIncremented(self.pos,self.scale[2],2)) #top
        self.parts[0].setColor(160,0,0)
        self.parts[1].setPos(self.getCoordIncremented(self.pos,-self.scale[2],2))#bottom
        self.parts[1].setColor(160,0,0)

        self.parts[2].setPos(self.getCoordIncremented(self.pos,self.scale[0],0)) #left
        self.parts[2].setColor(0,160,0)
        self.parts[3].setPos(self.getCoordIncremented(self.pos,-self.scale[0],0)) #right
        self.parts[3].setColor(0,160,0)

        self.parts[4].setPos(self.getCoordIncremented(self.pos,self.scale[1],1)) #front
        self.parts[4].setColor(0,0,160)
        self.parts[5].setPos(self.getCoordIncremented(self.pos,-self.scale[1],1)) #behind
        self.parts[5].setColor(0,0,160)


    def show(self):
        for m in self.parts:
            m.show()
    
    def hide(self):
        for m in self.parts:
            m.hide()
   
    def initCollisions(self):
        # Initialize the collision traverser.
        base.cTrav = CollisionTraverser()

        # Initialize the Pusher collision handler.
        self.pusher = CollisionHandlerPusher()
        # Create a collision node for this object.
        self.cNode = CollisionNode('box')
        # Attach a collision sphere solid to the collision node.
        self.cNode.addSolid(CollisionBox((0,0,-self.scale[2]), 1,1,self.scale[2]))
        # Attach the collision node to the object's model.
        self.boxC = self.model.attachNewNode(self.cNode)
        # Set the object's collision node to render as visible.
        self.boxC.show()     

        print("WERT")

    def addCollisionTo(self,modelC,model):
        # Add the Pusher collision handler to the collision traverser.
        base.cTrav.addCollider(modelC, self.pusher)
        # Add the 'frowney' collision node to the Pusher collision handler.
        self.pusher.addCollider(modelC, model, base.drive.node())

    def collide(self, collEntry):
        print("Collided")

    def getCoordIncremented(self,c,eps,v):
        cout = LVecBase3f(c)
        if(v == 0):
            cout.addX(eps)
        elif(v == 1):
            cout.addY(eps)
        else:
            cout.addZ(eps)
        print(cout)
        return cout