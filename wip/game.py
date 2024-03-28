from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import CardMaker
from panda3d.core import Vec3

import keyboard

class Game(ShowBase):
	textures = {
		"universe": "./textures/Universe-fors8M4.png",
		"ceres": "./textures/ceres.jpg",
		"earth": "./textures/earth.jpg",
		"eris": "./textures/eris.jpg",
		"haumea": "./textures/haumea.jpg",
		"jupiter": "./textures/jupiter.jpg",
		"makemake": "./textures/makemake.jpg",
		"mars": "./textures/mars.jpg",
		"mercury": "./textures/mercury.jpg",
		"missing texture": "./textures/missing_texture.jpg",
		"moon": "./textures/moon.jpg",
		"neptune": "./textures/neptune.jpg",
		"saturn": "./textures/saturn.jpg",
		"sun": "./textures/sun.jpg",
		"uranus": "./textures/uranus.jpg",
		"venus atmosphere": "./textures/venus_atmosphere.jpg",
		"venus surface": "./textures/venus_surface.jpg",
		"the Borg": "./textures/theBorg.jpg",
		"Khan": "./textures/Khan.jpg",
		"phaser": "./textures/phaser.jpg",
		"Hud": "./textures/ReticleIV.gif",
		"space station": "./textures/SpaceStation.png",
		"sparkle": "./textures/sparkle.png",
	}
	models = {
		"inner sphere": "./models/innerSphere.x",
		"outer sphere": "./models/outerSphere.x",
		"the Borg": "./models/theBorg.x",
		"Khan": "./models/Khan.x",
		"phaser": "./models/phaser.x",
		"space station": "./models/spaceStation.x",
	}
	colors = {
		"hot pink": (1,.412,.706)
	}
	settings = {
		"universe size": 15000,
		"max phasers": 3,
		"phaser kill distance": 300,
		"spaceship camera": True,
		"spaceship thrust": 5,
		"toggle hud": True,
		"display hud": True,
	}
	center = (0,0,0)
	def __init__(self):
		ShowBase.__init__(self)
		if(Game.settings["spaceship camera"]):
			self.disableMouse()
			if(Game.settings["display hud"]):
				self.Hud = OnscreenImage(image= Game.textures["Hud"], pos=(0, 0, 0),scale=.5)
				self.Hud.setTransparency(1)
		self.phaser_bolts=[]
		self.drones=[]
		self.setupHotkeys()
		self.setupBox()
		self.setupPlanets()
		self.setupPlayer()
		self.taskMgr.add(self.loop,"loop")
	def setupBox(self):
		self.setBackgroundColor(Game.colors["hot pink"])
		self.universe		= Item(Game.center, Game.settings["universe size"], Game.models["inner sphere"], Game.textures["universe"])
		self.universe_outer	= Item(Game.center, Game.settings["universe size"], Game.models["outer sphere"], Game.textures["universe"])
	def setupPlanets(self):
		self.planets=[]
		self.planets.append(Item((1000,0,0), 100, Game.models["outer sphere"], Game.textures["ceres"]))
		self.planets.append(Item((-1000,0,0), 100, Game.models["outer sphere"], Game.textures["eris"]))
		self.planets.append(Item((0,1000,0), 100, Game.models["outer sphere"], Game.textures["haumea"]))
		self.planets.append(Item((0,-1000,0), 100, Game.models["outer sphere"], Game.textures["jupiter"]))
		self.planets.append(Item((0,0,1000), 100, Game.models["outer sphere"], Game.textures["neptune"]))
		self.planets.append(Item((0,0,-1000), 100, Game.models["outer sphere"], Game.textures["makemake"]))
	def setupPlayer(self):
		self.player			= Item(Game.center, 1, Game.models["Khan"], Game.textures["Khan"])
		self.player.model.setP(self.player.model.getP()+90)
	def fire(self):
		if(len(self.phaser_bolts)<=Game.settings["max phasers"]):
			self.player.model.setP(self.player.model.getP()-90)
			self.phaser_bolts.append(Phaser(self.player.model.getPos(), self.player.model.getHpr(), self.player.trajectory*Game.settings["spaceship thrust"]))
			self.player.model.setP(self.player.model.getP()+90)
	def getSpaceshipTrajectory(self):
		self.player.model.setP(self.player.model.getP()-90)
		self.player.trajectory=self.render.getRelativeVector(self.player.model,Vec3.forward())
		self.player.trajectory.normalize()
		self.player.model.setP(self.player.model.getP()+90)
	def loop(self,task):
		self.getSpaceshipTrajectory()
		self.keyActions()
		if(Game.settings["spaceship camera"]):
			self.camera.setPos(self.player.model.getPos())
			self.camera.setHpr(self.player.model.getHpr())
			self.camera.setP(self.player.model.getP()+270)
		if(len(self.phaser_bolts)>0):
			for bolt in self.phaser_bolts:
				bolt.model.setFluidPos(bolt.model.getPos()+bolt.trajectory)
				if(self.player.model.getDistance(bolt.model)>Game.settings["phaser kill distance"]):
					bolt.kill()
			self.phaser_bolts=[bolt for bolt in self.phaser_bolts if bolt.live]
		return Task.cont
	def setupHotkeys(self):
		keyboard.add_hotkey('f', self.fire)
		if(Game.settings["toggle hud"]):
			keyboard.add_hotkey('z', self.toggleHud)
	def toggleHud(self):
		Game.settings["display hud"] = not Game.settings["display hud"]
		if(Game.settings["spaceship camera"]):
			if(Game.settings["display hud"]):
				self.Hud = OnscreenImage(image= Game.textures["Hud"], pos=(0, 0, 0),scale=.5)
				self.Hud.setTransparency(1)
			else:
				self.Hud.destroy()
	def keyActions(self):
		if keyboard.is_pressed("space"):
			self.player.model.setFluidPos(self.player.model.getPos()+self.player.trajectory*Game.settings["spaceship thrust"])
		rate=.5
		if keyboard.is_pressed("a"):
			self.player.model.setH(self.player.model.getH()+rate)
		if keyboard.is_pressed("d"):
			self.player.model.setH(self.player.model.getH()-rate)
		if keyboard.is_pressed("w"):
			self.player.model.setP(self.player.model.getP()+rate)
		if keyboard.is_pressed("s"):
			self.player.model.setP(self.player.model.getP()-rate)
		if keyboard.is_pressed("q"):
			self.player.model.setR(self.player.model.getR()-rate)
		if keyboard.is_pressed("e"):
			self.player.model.setR(self.player.model.getR()+rate)
class Item(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,modelPath:str,texPath:str):
		self.model=base.loader.loadModel(modelPath)
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture(texPath),1)
class Card(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,texPath:str):
		self.model = render.attachNewNode(CardMaker('card').generate())
		tex = loader.loadTexture(texPath)
		self.model.setTexture( tex )
		self.model.reparentTo( base.render )
		self.model.setPos([posVec])
		self.model.setLightOff()
		self.model.setTransparency(True)
		self.model.setBillboardPointEye()
class Phaser(Item):
	def __init__(self,posVec:Vec3,hpr,trajVec:Vec3):
		super(Phaser,self).__init__(posVec,1,Game.models["phaser"], Game.textures["phaser"])
		self.model.setHpr(hpr)
		self.trajectory=trajVec
		self.live = True
	def kill(self):
		self.explode()
		self.model.removeNode()
		self.live=False
	def explode(self):
		#Card(self.model.getPos,10,Game.textures["sparkle"])
		pass
app = Game()
app.run()