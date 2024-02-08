from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from shapeGenerator import Sphere #https://discourse.panda3d.org/t/generating-primitives/6630/8

class SpaceJam(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.SetupScene()
	def SetupScene(self):
		self.SetupCam()
		self.Universe=Celestial("./Assets/Universe/Universe.x",0,0,0,15000,"./Assets/Universe/Universe-fors8M3.png",self)
		self.Planet1=Celestial(Sphere(1),150,5000,67,100,"./Assets/Planets/textures/2k_neptune.jpg",self)
		self.Sun=Celestial(Sphere(1),0,0,0,1000,"./Assets/Extra/2k_sun.jpg",self)
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
app = SpaceJam()
app.run()