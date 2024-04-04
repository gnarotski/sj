from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.interval.LerpInterval import LerpFunc
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import TextureStage
from panda3d.core import CardMaker
from panda3d.core import Vec3

import DefensePaths
import keyboard
import math
import time

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
		"drone": "./models/DroneDefender.x",
		"space station": "./models/spaceStation.x",
	}
	colors = {
		"hot pink": (1,.412,.706)
	}
	settings = {
		"universe size": 15000,
		"universe rotation": .01,
		"max phasers": 3,
		"phasers cooldown": .1,
		"phaser kill distance": 600,
		"phaser speed": 8,
		"spaceship camera": True,
		"spaceship thrust": 5,
		"spaceship rotation rate": .5,
		"spaceship collision buffer": 5,
		"toggle hud": True,
		"display hud": True,
		"cloud drone jump time": .1,
		"drone orbit speed": .05,
	}
	center = (0,0,0)
	drone_cycle=30
	drone_size=3
	def __init__(self):
		ShowBase.__init__(self)
		if Game.settings["spaceship camera"]:
			self.disableMouse()
			if Game.settings["display hud"]:
				self.Hud = OnscreenImage(image= Game.textures["Hud"], pos=(0, 0, 0),scale=.1)
				self.Hud.setTransparency(1)
		self.press_g_to_change_fire_mode = OnscreenText(text='press \'g\' to change fire mode', pos=(-1, .8), fg=(1,1,1,1), scale=0.07)
		self.fire_mode = OnscreenText(text='Fire mode: [3 round burst]', pos=(-1, .9), fg=(1,1,1,1), scale=0.07)
		self.fm=1
		self.phaser_bolts=[]
		self.lastFired = 0
		self.setupHotkeys()
		self.setupBox()
		self.setupPlanets()
		self.setupSpaceStation()
		self.setupDrones()
		self.setupPlayer()
		self.taskMgr.add(self.loop)
		self.taskMgr.add(self.droneOrbitals)
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
	def setupSpaceStation(self):
		self.spaceStation=Item((1000,0,1000), 10, Game.models["space station"], Game.textures["space station"])
	def setupDrones(self):
		self.drones=[]
		self.drawCloudDefense(self.planets[0],Game.drone_cycle)
		self.drawBaseballSeams(self.planets[1],1,30)
		self.drawXY(self.planets[2],Game.drone_cycle)
		self.drawXZ(self.planets[3],Game.drone_cycle)
		self.drawYZ(self.planets[4],Game.drone_cycle)
		self.drawCloudDefense(self.planets[5],Game.drone_cycle)
	def drawCloudDefense(self, celestial,count):
		for j in range(count):
			unitVec = DefensePaths.Cloud()
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.drones.append(Drone(position,Game.drone_size,"cloud",celestial,j))
	def drawBaseballSeams(self,celestial,completion,count,radius=1):
		for step in range(math.floor(completion*count)):
			unitVec = DefensePaths.BaseballSeams(step,count,B=0.4)
			unitVec.normalize()
			position=unitVec*celestial.model.getScale()[0]*2+celestial.model.getPos()
			self.drones.append(Drone(position,Game.drone_size,"baseball",celestial,step))
	def drawXY(self, celestial,count):
		for j in range(count):
			unitVec = DefensePaths.XY(j,count)
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.drones.append(Drone(position,Game.drone_size,"XY",celestial,j))
	def drawXZ(self, celestial,count):
		for j in range(count):
			unitVec = DefensePaths.XZ(j,count)
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.drones.append(Drone(position,Game.drone_size,"XZ",celestial,j))
	def drawYZ(self, celestial,count):
		for j in range(count):
			unitVec = DefensePaths.YZ(j,count)
			unitVec.normalize()
			position = (unitVec*(celestial.model.getScale()[0]*1.5))+celestial.model.getPos()
			self.drones.append(Drone(position,Game.drone_size,"YZ",celestial,j))
	def setupPlayer(self):
		self.player			= Item(Game.center, 1, Game.models["Khan"], Game.textures["Khan"])
		self.player.model.setP(self.player.model.getP()+90)
	def fire(self):
		if (len(self.phaser_bolts)<Game.settings["max phasers"] or Game.settings["max phasers"]<0) and time.time() - self.lastFired >= Game.settings["phasers cooldown"]:
			self.lastFired = time.time()
			self.player.model.setP(self.player.model.getP()-90)
			self.phaser_bolts.append(Phaser(self.player.model.getPos(), self.player.model.getHpr(), self.player.trajectory*Game.settings["phaser speed"]))
			self.player.model.setP(self.player.model.getP()+90)
	def getSpaceshipTrajectory(self):
		self.player.model.setP(self.player.model.getP()-90)
		self.player.trajectory=self.render.getRelativeVector(self.player.model,Vec3.forward())
		self.player.trajectory.normalize()
		self.player.model.setP(self.player.model.getP()+90)
	def loop(self,task):
		self.getSpaceshipTrajectory()
		self.keyActions()
		if Game.settings["spaceship camera"]:
			self.camera.setPos(self.player.model.getPos())
			self.camera.setHpr(self.player.model.getHpr())
			self.camera.setP(self.player.model.getP()+270)
		boom=[]
		if len(self.phaser_bolts)>0:
			for bolt in self.phaser_bolts:
				bolt.model.setFluidPos(bolt.model.getPos()+bolt.trajectory)
				for drone in self.drones:
					if drone.model.getDistance(bolt.model)<Game.drone_size*2.3:
						boom.append((bolt,drone))
				if self.player.model.getDistance(bolt.model)>Game.settings["phaser kill distance"]:
					bolt.kill()
		for target in boom:
			target[0].kill()
			target[1].kaboom()
		self.universe.model.setP(self.universe.model.getP()+Game.settings["universe rotation"])
		self.spaceStation.model.setR(self.spaceStation.model.getR()+.3)
		self.killDeadDestructables()
		return Task.cont
	def droneOrbitals(self,task):
		for drone in self.drones:
			if drone.droneType=="cloud" and time.time() - drone.lastJumped >= Game.settings["cloud drone jump time"]:
				unitVec = DefensePaths.Cloud()
				unitVec.normalize()
				drone.model.setPos((unitVec*(drone.core.model.getScale()[0]*1.5))+drone.core.model.getPos())
				drone.lastJumped = time.time()
			if drone.droneType=="baseball":
				drone.j+=Game.settings["drone orbit speed"]
				unitVec = DefensePaths.BaseballSeams(drone.j,Game.drone_cycle,B=0.4)
				unitVec.normalize()
				drone.model.setFluidPos(unitVec*drone.core.model.getScale()[0]*2+drone.core.model.getPos())
			if drone.droneType=="XY":
				drone.j+=Game.settings["drone orbit speed"]
				unitVec = DefensePaths.XY(drone.j,Game.drone_cycle)
				unitVec.normalize()
				drone.model.setFluidPos((unitVec*(drone.core.model.getScale()[0]*1.5))+drone.core.model.getPos())
			if drone.droneType=="XZ":
				drone.j+=Game.settings["drone orbit speed"]
				unitVec = DefensePaths.XZ(drone.j,Game.drone_cycle)
				unitVec.normalize()
				drone.model.setFluidPos((unitVec*(drone.core.model.getScale()[0]*1.5))+drone.core.model.getPos())
			if drone.droneType=="YZ":
				drone.j+=Game.settings["drone orbit speed"]
				unitVec = DefensePaths.YZ(drone.j,Game.drone_cycle)
				unitVec.normalize()
				drone.model.setFluidPos((unitVec*(drone.core.model.getScale()[0]*1.5))+drone.core.model.getPos())
		return Task.cont
	def killDeadDestructables(self):
		self.phaser_bolts=[bolt for bolt in self.phaser_bolts if bolt.live]
		self.drones=[drone for drone in self.drones if drone.live]
	def setupHotkeys(self):
		if Game.settings["toggle hud"]:
			keyboard.add_hotkey('z', self.toggleHud)
		keyboard.add_hotkey('g', self.nextFire)
	def nextFire(self):
		if self.fm == 1:
			self.fire_mode.removeNode()
			self.fire_mode = OnscreenText(text='Fire mode: [rapid fire]', pos=(-1, .9), fg=(1,1,1,1), scale=0.07)
			Game.settings["max phasers"] = -1
			Game.settings["phasers cooldown"] = .1
			self.fm=2
		elif self.fm == 2:
			self.fire_mode.removeNode()
			self.fire_mode = OnscreenText(text='Fire mode: [single]', pos=(-1, .9), fg=(1,1,1,1), scale=0.07)
			Game.settings["max phasers"] = -1
			Game.settings["phasers cooldown"] = 2
			self.fm=3
		elif self.fm == 3:
			self.fire_mode.removeNode()
			self.fire_mode = OnscreenText(text='Fire mode: [3 round burst]', pos=(-1, .9), fg=(1,1,1,1), scale=0.07)
			Game.settings["max phasers"] = 3
			Game.settings["phasers cooldown"] = .1
			self.fm=1
	def toggleHud(self):
		Game.settings["display hud"] = not Game.settings["display hud"]
		if Game.settings["spaceship camera"]:
			if Game.settings["display hud"]:
				self.Hud = OnscreenImage(image= Game.textures["Hud"], pos=(0, 0, 0),scale=.5)
				self.Hud.setTransparency(1)
			else:
				self.Hud.destroy()
	def pitec(self,item1,item2):
		return (item2.model.getPos()-item1.model.getPos()).length()<item2.model.getScale()+item1.model.getScale()+Game.settings["spaceship collision buffer"]
	def pitem(self,item1,item2):
		return not ((item2.model.getPos()-item1.model.getPos()).length()<item2.model.getScale()+item1.model.getScale()-Game.settings["spaceship collision buffer"])
	def keyActions(self):
		if keyboard.is_pressed("space"):
			self.player.model.setFluidPos(self.player.model.getPos()+self.player.trajectory*Game.settings["spaceship thrust"])
			if ((self.spaceStation.model.getPos()-self.player.model.getPos()).length()) < 150:
				self.player.model.setFluidPos(self.player.model.getPos()+self.player.trajectory*300)
			for planet in self.planets:
				if self.pitec(self.player,planet):
					self.player.model.setFluidPos(self.player.model.getPos()+((planet.model.getPos()-self.player.model.getPos()).normalize()*Game.settings["spaceship thrust"]))
			if self.pitem(self.player,self.universe):
				self.player.model.setFluidPos(Game.center)
		if keyboard.is_pressed("f"):
			self.fire()
		if keyboard.is_pressed("a"):
			self.player.model.setH(self.player.model.getH()+Game.settings["spaceship rotation rate"])
			if(self.player.model.getH()>360):
				self.player.model.setH(self.player.model.getH()-360)
		if keyboard.is_pressed("d"):
			self.player.model.setH(self.player.model.getH()-Game.settings["spaceship rotation rate"])
			if(self.player.model.getH()<0):
				self.player.model.setH(self.player.model.getH()+360)
		if keyboard.is_pressed("w"):
			self.player.model.setP(self.player.model.getP()+Game.settings["spaceship rotation rate"])
			if(self.player.model.getP()>360):
				self.player.model.setP(self.player.model.getP()-360)
		if keyboard.is_pressed("s"):
			self.player.model.setP(self.player.model.getP()-Game.settings["spaceship rotation rate"])
			if(self.player.model.getP()<0):
				self.player.model.setP(self.player.model.getP()+360)
		if keyboard.is_pressed("q"):
			self.player.model.setR(self.player.model.getR()-Game.settings["spaceship rotation rate"])
			if(self.player.model.getR()<0):
				self.player.model.setR(self.player.model.getR()+360)
		if keyboard.is_pressed("e"):
			self.player.model.setR(self.player.model.getR()+Game.settings["spaceship rotation rate"])
			if(self.player.model.getR()>360):
				self.player.model.setR(self.player.model.getR()-360)
class Item(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,modelPath:str,texPath:str):
		self.model=base.loader.loadModel(modelPath)
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setTexture(loader.loadTexture(texPath),1)
class Card(ShowBase):
	def __init__(self,posVec:Vec3,scaleVec:float,texPath:str):
		cm=CardMaker('card')
		cm.setFrame(-.5,.5,-.5,.5)
		self.model = render.attachNewNode(cm.generate())
		self.model.setTexture(loader.loadTexture(texPath))
		self.model.reparentTo(base.render)
		self.model.setPos(posVec)
		self.model.setScale(scaleVec)
		self.model.setLightOff()
		self.model.setTransparency(True)
		self.model.setBillboardPointWorld()
class Destructable:
	live = True
	def kill(self):
		self.model.removeNode()
		self.live=False
	def kaboom(self):
		self.explode()
		self.kill()
	def explode(self):
		Explosion(self.model.getPos())
class Phaser(Item,Destructable):
	def __init__(self,posVec:Vec3,hpr,trajVec:Vec3):
		super(Phaser,self).__init__(posVec,1,Game.models["phaser"], Game.textures["phaser"])
		self.model.setHpr(hpr)
		self.trajectory=trajVec
class Drone(Item,Destructable):
	def __init__(self,posVec:Vec3,size:float,droneType:str,core:Item,j:float):
		super(Drone,self).__init__(posVec,size,Game.models["drone"], Game.textures["missing texture"])
		self.droneType=droneType
		self.core=core
		self.j=j
		self.lastJumped=0
		self.model.setBillboardPointWorld()
class Explosion():
	def __init__(self,posVec:Vec3):
		self.card=Card(posVec,10,Game.textures["sparkle"])
		LerpFunc(self.explode, 5.0, 0, 1).start()
	def explode(self,completion):
		self.card.model.setScale(self.card.model.getScale()*.9)
		if math.floor(completion):
			self.card.model.removeNode()
	
app = Game()
app.run()