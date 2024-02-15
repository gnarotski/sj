from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class SpaceJam(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.SetupScene()
	def SetupScene(self):
		self.SetupCam()
		self.Universe=Universe("./Assets/Universe/Universe.x",0,0,0,15000,"./Assets/Universe/Universe-fors8M3.png",self)
		self.Planet1=Celestial("./Assets/Planets/protoPlanet.x",1000,5000,0,200,"./Assets/Planets/textures/2k_neptune.jpg",self)
		self.Planet2=Celestial("./Assets/Planets/protoPlanet.x",700,5500,200,300,"./Assets/Planets/textures/2k_jupiter.jpg",self)
		self.Planet3=Celestial("./Assets/Planets/protoPlanet.x",500,6000,300,30,"./Assets/Planets/textures/2k_mars.jpg",self)
		self.Planet4=Celestial("./Assets/Planets/protoPlanet.x",400,6500,600,40,"./Assets/Planets/textures/2k_mercury.jpg",self)
		self.Planet5=Celestial("./Assets/Planets/protoPlanet.x",200,7000,800,110,"./Assets/Planets/textures/2k_saturn.jpg",self)
		self.Planet6=Celestial("./Assets/Planets/protoPlanet.x",150,7500,900,106,"./Assets/Planets/textures/2k_uranus.jpg",self)
		self.Sun=Celestial("./Assets/Planets/protoPlanet.x",0,0,0,1000,"./Assets/Extra/2k_sun.jpg",self)
		self.PlayerSpaceship=Spaceship("./Assets/Spaceships/theBorg/theBorg.x",0,0,5000,100,"./Assets/Spaceships/theBorg/theBorg.jpg",self)
		self.Spacestation=SpaceStation(5000,0,0,100,self)
		
	def SetupCam(self):
		self.trackball.node().set_pos(0,10000,0)
class Celestial:
	def __init__(self,modelPath,x,y,z,scale,texturePath,main):
		if type(modelPath) is str:
			self.model=main.loader.loadModel(modelPath)
		else:
			self.model=modelPath
		self.model.reparentTo(main.render)
		self.model.setPos(x,y,z)
		self.model.setScale(scale)
		self.model.setTexture(loader.loadTexture(texturePath))
class Universe:
	def __init__(self,modelPath,x,y,z,scale,texturePath,main):
		if type(modelPath) is str:
			self.model=main.loader.loadModel(modelPath)
		else:
			self.model=modelPath
		self.model.reparentTo(main.render)
		self.model.setPos(x,y,z)
		self.model.setScale(scale)
		self.model.setTexture(loader.loadTexture(texturePath))
class Spaceship:
	def __init__(self,modelPath,x,y,z,scale,texturePath,main):
		if type(modelPath) is str:
			self.model=main.loader.loadModel(modelPath)
		else:
			self.model=modelPath
		self.model.reparentTo(main.render)
		self.model.setPos(x,y,z)
		self.model.setScale(scale)
		self.model.setTexture(loader.loadTexture(texturePath))
class SpaceStation:
	def __init__(self,x,y,z,scale,main):
		self.model=main.loader.loadModel("./Assets/Space Station/SpaceStation1B/spaceStation.x")
		self.model.reparentTo(main.render)
		self.model.setPos(x,y,z)
		self.model.setScale(scale)
		self.model.setTexture(loader.loadTexture("./Assets/Space Station/SpaceStation1B/SpaceStation1_Dif2.png"))
app = SpaceJam()
app.run()