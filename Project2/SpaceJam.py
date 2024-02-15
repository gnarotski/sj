from math import pi, sin, cos, floor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from SpaceJamClasses import *
from panda3d.core import Vec3
import DefensePaths
fullCycle=10
droneSize=100
class SpaceJam(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.Drones=[]
		self.SetupScene()
	def SetupScene(self):
		self.SetupCam()
		self.Universe=Universe((0,0,0),15000)
		self.Planet1=Celestial((1000,5000,0),200,"./Assets/Planets/textures/2k_neptune.jpg")
		self.Planet2=Celestial((700,5500,200),300,"./Assets/Planets/textures/2k_jupiter.jpg")
		self.Planet3=Celestial((500,6000,300),30,"./Assets/Planets/textures/2k_mars.jpg")
		self.Planet4=Celestial((400,6500,600),40,"./Assets/Planets/textures/2k_mercury.jpg")
		self.Planet5=Celestial((200,7000,800),110,"./Assets/Planets/textures/2k_saturn.jpg")
		self.Planet6=Celestial((150,7500,900),106,"./Assets/Planets/textures/2k_uranus.jpg")
		self.Sun=Celestial((0,0,0),1000,"./Assets/Extra/2k_sun.jpg")
		self.PlayerSpaceship=Spaceship((0,0,5000),100,"./Assets/Spaceships/theBorg/theBorg.x","./Assets/Spaceships/theBorg/theBorg.jpg")
		self.Spacestation=SpaceStation((5000,0,0),100)
		#self.drawCloudDefense(self.Sun,fullCycle)
		#self.drawBaseballSeams(self.Sun,1,30)
		self.drawXY(self.Sun,fullCycle)
		self.drawXZ(self.Sun,fullCycle)
		self.drawYZ(self.Sun,fullCycle)
		
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
			unitVec = DefensePaths.XY()
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def drawXZ(self, celestial:Celestial,count):
		for j in range(fullCycle):
			unitVec = DefensePaths.XZ()
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def drawYZ(self, celestial:Celestial,count):
		for j in range(fullCycle):
			unitVec = DefensePaths.YZ()
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.Drones.append(Drone(position,droneSize))
	def SetupCam(self):
		self.trackball.node().set_pos(0,10000,0)
app = SpaceJam()
app.run()