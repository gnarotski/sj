from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import Vec3
from CollideObjectBase import *
class Celestial(SphereCollideObject,ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,texPath:str):
			self.model=base.loader.loadModel("./Assets/Planets/protoPlanet.x")
			self.model.reparentTo(base.render)
			self.model.setPos(posVec)
			self.model.setScale(scaleVec)
			self.model.setTexture(loader.loadTexture(texPath),1)
			#self.model.setName("")
class Universe(InverseSphereCollideObject,ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float):
		super(Universe,self).__init__(base.loader,"./Assets/Universe/Universe.x",self.model,"universe",Vec3(0,0,0),.9*scaleVec)
		self.model=base.loader.loadModel("./Assets/Universe/Universe.x")
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture("./Assets/Universe/Universe-fors8M4.png"),1)
class Spaceship(SphereCollideObject,ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,modelPath,texturePath):
		if type(modelPath) is str:
			self.model=base.loader.loadModel(modelPath)
		else:
			self.model=modelPath
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture(texturePath),1)
class Player(InverseSphereCollideObject,ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,modelPath,texturePath,s):
		super(Player,self).__init__(base.loader,modelPath,self.model,"psh",posVec,2*scaleVec)
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
	def UpTurn(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyUpTurn,'up-turn')
		else:
			self.s.taskMgr.remove('up-turn')
	def applyUpTurn(self,task):
		rate=.5
		self.model.setP(self.model.getP()+rate)
		return Task.cont
	def DownTurn(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyDownTurn,'down-turn')
		else:
			self.s.taskMgr.remove('down-turn')
	def applyDownTurn(self,task):
		rate=.5
		self.model.setP(self.model.getP()-rate)
		return Task.cont
	def LeftRoll(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyLeftRoll,'left-roll')
		else:
			self.s.taskMgr.remove('left-roll')
	def applyLeftRoll(self,task):
		rate=.5
		self.model.setR(self.model.getR()-rate)
		return Task.cont
	def RightRoll(self,keyDown):
		if keyDown:
			self.s.taskMgr.add(self.applyRightRoll,'right-roll')
		else:
			self.s.taskMgr.remove('right-roll')
	def applyRightRoll(self,task):
		rate=.5
		self.model.setR(self.model.getR()+rate)
		return Task.cont
class SpaceStation(CapsuleCollideObject):
	def __init__(self,posVec:Vec3,scaleVec:float):
		super(SpaceStation,self).__init__(loader,"./Assets/Space Station/SpaceStation1B/spaceStation.x",model,"SpaceStation",1,-1,5,1,-1,-5,100)
		self.model=base.loader.loadModel("./Assets/Space Station/SpaceStation1B/spaceStation.x")
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture("./Assets/Space Station/SpaceStation1B/SpaceStation1_Dif2.png"),1)
class Drone(SphereCollideObject,ShowBase):
	droneCount = 0
	def __init__(self,posVec:Vec3,scaleVec:float):
		self.droneCount+=1
		self.model=base.loader.loadModel("./Assets/Drone Defender/DroneDefender.x")
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture("./Assets/Extra/missing_texture.jpg"),1)