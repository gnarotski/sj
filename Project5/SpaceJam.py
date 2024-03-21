from math import pi, sin, cos, floor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3,Vec3,CollisionTraverser,CollisionHandlerPusher
from CollideObjectBase import *
from SpaceJamClasses import *
import DefensePaths
fullCycle=10
droneSize=50
class SpaceJam(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.disableMouse()
		self.camera.setPos(0,0,0)
		self.Drones=[]
		self.SetupScene()
		self.cTrav=CollisionTraverser()
		self.cTrav.traverse(self.render)
		self.pusher=CollisionHandlerPusher()
		self.pusher.addCollider(self.PlayerSpaceship.collisionNode,self.PlayerSpaceship.model)
		
		self.cTrav.addCollider(self.PlayerSpaceship.collisionNode,self.pusher)
		self.cTrav.showCollisions(self.render)
		self.keys = {"space":0, "left":0, "right":0, "up":0, "down":0, "A":0, "D":0, "W":0, "S":0, "Q":0, "E":0}
		self.acceptKeys()
		self.taskMgr.add(self.loop,"loop")
	def SetupScene(self):
		self.Universe=Universe((0,0,0),15000)
		self.Planet1=Celestial((1000,5000,0),200,"./Assets/Planets/textures/2k_neptune.jpg")
		self.Planet2=Celestial((700,5500,200),300,"./Assets/Planets/textures/2k_jupiter.jpg")
		self.Planet3=Celestial((500,6000,300),30,"./Assets/Planets/textures/2k_mars.jpg")
		self.Planet4=Celestial((400,6500,600),40,"./Assets/Planets/textures/2k_mercury.jpg")
		self.Planet5=Celestial((200,7000,800),110,"./Assets/Planets/textures/2k_saturn.jpg")
		self.Planet6=Celestial((150,7500,900),106,"./Assets/Planets/textures/2k_uranus.jpg")
		self.Sun=Celestial((0,0,0),1000,"./Assets/Extra/2k_sun.jpg")
		self.PlayerSpaceship=Player((0,0,5000),10,"./Assets/Spaceships/theBorg/theBorg.x","./Assets/Spaceships/theBorg/theBorg.jpg",self)
		self.Spacestation=SpaceStation((5000,0,0),100)
		self.drawCloudDefense(self.Planet1,fullCycle)
		self.drawBaseballSeams(self.Planet2,1,30)
		self.drawXY(self.Sun,fullCycle)
		self.drawXZ(self.Sun,fullCycle)
		self.drawYZ(self.Sun,fullCycle)
		self.Hud = OnscreenImage(image='./Assets/Hud/ReticleIV.gif', pos=(0, 0, 0),scale=.5)
		self.Hud.setTransparency(1)
		self.SetupCam()
		
	def drawCloudDefense(self, celestial:Celestial,count):
		for j in range(fullCycle):
			unitVec = DefensePaths.Cloud()
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def drawBaseballSeams(self,celestial:Celestial,completion,count,radius=1):
		for step in range(floor(completion*count)):
			unitVec = DefensePaths.BaseballSeams(step,count,B=0.4)
			unitVec.normalize()
			position=unitVec*celestial.model.getScale()[0]*2+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def drawXY(self, celestial:Celestial,count):
		for j in range(fullCycle):
			unitVec = DefensePaths.XY(j,fullCycle)
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def drawXZ(self, celestial:Celestial,count):
		for j in range(fullCycle):
			unitVec = DefensePaths.XZ(j,fullCycle)
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def drawYZ(self, celestial:Celestial,count):
		for j in range(fullCycle):
			unitVec = DefensePaths.YZ(j,fullCycle)
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def SetupCam(self):
		#self.trackball.node().set_pos(0,10000,0)
		self.camera.setPos(self.PlayerSpaceship.model.getPos())
		self.camera.setHpr(self.PlayerSpaceship.model.getHpr())
	def SetCam(self):
		self.camera.setPos(self.PlayerSpaceship.model.getPos())
		self.camera.setHpr(self.PlayerSpaceship.model.getHpr())
	def acceptKeys(self):
		self.accept('escape',self.quit)
		self.accept('space',self.PlayerSpaceship.Thrust,[1])
		self.accept('a',self.PlayerSpaceship.LeftTurn,[1])
		self.accept('d',self.PlayerSpaceship.RightTurn,[1])
		self.accept('w',self.PlayerSpaceship.UpTurn,[1])
		self.accept('s',self.PlayerSpaceship.DownTurn,[1])
		self.accept('q',self.PlayerSpaceship.LeftRoll,[1])
		self.accept('e',self.PlayerSpaceship.RightRoll,[1])
		self.accept('f',self.PlayerSpaceship.fire)
		self.accept('space-up',self.PlayerSpaceship.Thrust,[0])
		self.accept('a-up',self.PlayerSpaceship.LeftTurn,[0])
		self.accept('d-up',self.PlayerSpaceship.RightTurn,[0])
		self.accept('w-up',self.PlayerSpaceship.UpTurn,[0])
		self.accept('s-up',self.PlayerSpaceship.DownTurn,[0])
		self.accept('q-up',self.PlayerSpaceship.LeftRoll,[0])
		self.accept('e-up',self.PlayerSpaceship.RightRoll,[0])
	def quit(self):
		sys.exit()
	def setKey(self,key,state):
		self.keys[key] = state
	def loop(self,task):
		self.SetCam()
		return Task.cont
app = SpaceJam()
app.run()