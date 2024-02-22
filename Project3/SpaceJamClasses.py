from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import Vec3

class Celestial(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,texPath:str):
			self.model=base.loader.loadModel("./Assets/Planets/protoPlanet.x")
			self.model.reparentTo(base.render)
			self.model.setPos(posVec)
			self.model.setScale(scaleVec)
			self.model.setTexture(loader.loadTexture(texPath),1)
			#self.model.setName("")
class Universe(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float):
			self.model=base.loader.loadModel("./Assets/Universe/Universe.x")
			self.model.reparentTo(base.render)
			self.model.setPos(posVec)
			self.model.setScale(scaleVec)
			self.model.setTexture(loader.loadTexture("./Assets/Universe/Universe-fors8M4.png"),1)
class Spaceship(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,modelPath,texturePath):
		if type(modelPath) is str:
			self.model=base.loader.loadModel(modelPath)
		else:
			self.model=modelPath
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture(texturePath),1)
class Player(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,modelPath,texturePath,s):
		if type(modelPath) is str:
			self.model=base.loader.loadModel(modelPath)
		else:
			self.model=modelPath
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture(texturePath),1)
		self.s=s
	def Thrust(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyThrust,'forward-thrust')
		else:
			self.s.taskMgr.remove('forward-thrust')
	def applyThrust(self,task):
		rate=5
		trajectory=self.s.render.getRelativeVector(self.model,Vec3.forward())
		trajectory.normalize()
		self.model.setFluidPos(self.model.getPos()+trajectory*rate)
		return Task.cont
	def LeftTurn(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyLeftTurn,'left-turn')
		else:
			self.s.taskMgr.remove('left-turn')
	def applyLeftTurn(self,task):
		rate=.5
		self.model.setH(self.model.getH()+rate)
		return Task.cont
	def RightTurn(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyRightTurn,'right-turn')
		else:
			self.s.taskMgr.remove('right-turn')
	def applyRightTurn(self,task):
		rate=.5
		self.model.setH(self.model.getH()-rate)
		return Task.cont
class SpaceStation(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float):
		self.model=base.loader.loadModel("./Assets/Space Station/SpaceStation1B/spaceStation.x")
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture("./Assets/Space Station/SpaceStation1B/SpaceStation1_Dif2.png"),1)
class Drone(ShowBase):
	droneCount = 0
	def __init__(self,posVec:Vec3,scaleVec:float):
		self.droneCount+=1
		self.model=base.loader.loadModel("./Assets/Drone Defender/DroneDefender.x")
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture("./Assets/Extra/missing_texture.jpg"),1)