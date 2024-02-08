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
		self.Universe=self.loader.loadModel("./Assets/Universe/Universe.x")
		self.Universe.reparentTo(self.render) #all grey
		self.Universe.setScale(15000) #all white
		self.Universe.setTexture(loader.loadTexture("./Assets/Universe/Universe-fors8M3.png"))
		
		self.Planet1=self.loader.loadModel("./Assets/Planets/protoPlanet.x")
		self.Planet1.reparentTo(self.render)
		self.Planet1.setPos(150,5000,67)
		self.Universe.setScale(350)
		#self.Universe.setTexture(loader.loadTexture("./Assets/Planets/protoPlanet.png"))
		
app = SpaceJam()
app.run()