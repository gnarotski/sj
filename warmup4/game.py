from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from direct.interval.LerpInterval import LerpFunc
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import KeyboardButton
from panda3d.core import TextureStage
from panda3d.core import InputDevice
from panda3d.core import CardMaker
from panda3d.core import Point3
from panda3d.core import Vec3

import DefensePaths
import keyboard
import random
import math
import time
import sys

import socket
import threading
sType="idk"
gamedata=""
newgamedata="|||"
def group(lst, n):
	if len(lst)%n != 0:
		raise ValueError("{} is not a multiple of {}".format(len(lst),n))
	return list(zip(*[iter(lst)]*n))
def getRandomPoint():
	return (random.uniform(-2000, 2000),random.uniform(-2000, 2000),random.uniform(-2000, 2000))
def getDistance(model,point):
	[x,y,z]=model.getPos()
	return math.sqrt(((x-point[0])**2)+((y-point[1])**2)+((z-point[2])**2))
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
		self.press_g_to_change_fire_mode = OnscreenText(text='press \'g\' to change fire mode', pos=(-1, .8), fg=(1,1,1,1), scale=0.07,mayChange=1)
		self.fire_mode = OnscreenText(text='Fire mode: [3 round burst]', pos=(-1, .9), fg=(1,1,1,1), scale=0.07)
		self.phaser_bolts=[]
		self.wanderers=[Wanderer(10),Wanderer(10),Wanderer(10),Wanderer(10),Wanderer(10),Wanderer(10),Wanderer(10),Wanderer(10),Wanderer(10)]
		self.lastFired = 0
		self.setupHotkeys()
		self.setupBox()
		self.quickplanets([
			((1000,0,0),"ceres"),
			((-1000,0,0),"eris"),
			((0,1000,0),"haumea"),
			((0,-1000,0),"jupiter"),
			((0,0,1000),"neptune"),
			((0,0,-1000),"makemake")
		])
		self.setupSpaceStation()
		self.setupDrones()
		self.setupPlayer()
		self.taskMgr.add(self.loop)
		self.taskMgr.add(self.droneOrbitals)
	def setupBox(self):
		self.setBackgroundColor(Game.colors["hot pink"])
		self.universe		= Item(Game.center, Game.settings["universe size"], Game.models["inner sphere"], Game.textures["universe"])
		self.universe_outer	= Item(Game.center, Game.settings["universe size"], Game.models["outer sphere"], Game.textures["universe"])
	def quickplanets(self,pdat):
		self.planets=[]
		for data in pdat:
			self.planets.append([Item(data[0], 100, Game.models["outer sphere"], Game.textures[data[1]]),100])
	def setupSpaceStation(self):
		self.spaceStation=Item((1000,0,1000), 10, Game.models["space station"], Game.textures["space station"])
	def setupDrones(self):
		self.drones=[]
		self.drawCloudDefense(self.planets[0][0],Game.drone_cycle)
		self.drawBaseballSeams(self.planets[1][0],1,30)
		self.drawXY(self.planets[2][0],Game.drone_cycle)
		self.drawXZ(self.planets[3][0],Game.drone_cycle)
		self.drawYZ(self.planets[4][0],Game.drone_cycle)
		self.drawCloudDefense(self.planets[5][0],Game.drone_cycle)
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
		self.player2		= Item(Game.center, 1, Game.models["Khan"], Game.textures["Khan"])
		self.player.model.setP(self.player.model.getP()+90)
	def fire(self):
		self.phaser_bolts.append(Phaser(self.player.model.getPos(), [Vec3(item[0],item[1]-90,item[2]) for item in [list(self.player.model.getHpr())]][0], self.player.trajectory*Game.settings["phaser speed"]))
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
		death=[]
		boom=[]
		for wanderer in self.wanderers:
			wanderer.loop()
		if len(self.phaser_bolts)>0:
			for bolt in self.phaser_bolts:
				bolt.model.setFluidPos(bolt.model.getPos()+bolt.trajectory)
				for drone in self.drones:
					if drone.model.getDistance(bolt.model)<Game.drone_size*2.3:
						death.append(bolt)
						boom.append(drone)
				for planet in self.planets:
					if planet[0].model.getDistance(bolt.model)<planet[1]*1.1:
						boom.append(bolt)
						planet[0].model.setPos(planet[0].model.getPos()+bolt.trajectory*50)
						planet[1]-=10
				if self.spaceStation.model.getDistance(bolt.model)<self.spaceStation.model.getScale()*17:
					boom.append(bolt)
					if 0<self.spaceStation.model.getScale():
						self.spaceStation.model.setScale(self.spaceStation.model.getScale()-1)
				if self.player.model.getDistance(bolt.model)>Game.settings["phaser kill distance"]:
					bolt.kill()
		for planet in self.planets:
			if planet[1]<planet[0].model.getScale():
				planet[0].model.setScale(planet[0].model.getScale()-1)
		for target in death:
			target.kill()
		for target in boom:
			target.kaboom()
		self.universe.model.setP(self.universe.model.getP()+Game.settings["universe rotation"])
		self.spaceStation.model.setR(self.spaceStation.model.getR()+.3)
		self.killDeadDestructables()
		global gamedata
		self.apply_data(newgamedata)
		gamedata=self.datify()
		return Task.cont
	def droneOrbitals(self,task):
		if sType=="server":
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
			self.accept('z', self.toggleHud)
		self.accept('g', self.nextFire)
	def nextFire(self):
		if self.fire_mode.text=='Fire mode: [3 round burst]':
			self.fire_mode.text='Fire mode: [rapid fire]'
			Game.settings["max phasers"] = -1
			Game.settings["phasers cooldown"] = .1
		elif self.fire_mode.text=='Fire mode: [rapid fire]':
			self.fire_mode.text='Fire mode: [single]'
			Game.settings["max phasers"] = -1
			Game.settings["phasers cooldown"] = 2
		elif self.fire_mode.text=='Fire mode: [single]':
			self.fire_mode.text='Fire mode: [3 round burst]'
			Game.settings["max phasers"] = 3
			Game.settings["phasers cooldown"] = .1
	def toggleHud(self):
		Game.settings["display hud"] = not Game.settings["display hud"]
		if Game.settings["spaceship camera"]:
			if Game.settings["display hud"]:
				self.Hud = OnscreenImage(image= Game.textures["Hud"], pos=(0, 0, 0),scale=.1)
				self.Hud.setTransparency(1)
			else:
				self.Hud.destroy()
	def pitec(self,item1,item2):
		return (item2.model.getPos()-item1.model.getPos()).length()<item2.model.getScale()+item1.model.getScale()+Game.settings["spaceship collision buffer"]
	def pitem(self,item1,item2):
		return not ((item2.model.getPos()-item1.model.getPos()).length()<item2.model.getScale()+item1.model.getScale()-Game.settings["spaceship collision buffer"])
	def keyActions(self):
		is_down = base.mouseWatcherNode.is_button_down
		keys={
			'space':KeyboardButton.ascii_key(' '),
			'f':KeyboardButton.ascii_key('f'),
			'a':KeyboardButton.ascii_key('a'),
			'd':KeyboardButton.ascii_key('d'),
			'w':KeyboardButton.ascii_key('w'),
			's':KeyboardButton.ascii_key('s'),
			'q':KeyboardButton.ascii_key('q'),
			'e':KeyboardButton.ascii_key('e')
		}
		if is_down(keys['space']):
			self.player.model.setFluidPos(self.player.model.getPos()+self.player.trajectory*Game.settings["spaceship thrust"])
			if ((self.spaceStation.model.getPos()-self.player.model.getPos()).length()) < 150:
				self.player.model.setFluidPos(self.player.model.getPos()+self.player.trajectory*300)
			for planet in self.planets:
				if self.pitec(self.player,planet[0]):
					self.player.model.setFluidPos(self.player.model.getPos()+((planet[0].model.getPos()-self.player.model.getPos()).normalize()*Game.settings["spaceship thrust"]))
			if self.pitem(self.player,self.universe):
				self.player.model.setFluidPos(Game.center)
		if is_down(keys['f']):
			if (len(self.phaser_bolts)<Game.settings["max phasers"] or Game.settings["max phasers"]<0) and time.time() - self.lastFired >= Game.settings["phasers cooldown"]:
				self.lastFired = time.time()
				self.fire()
		if is_down(keys['a']):
			self.player.model.setH(self.player.model.getH()+Game.settings["spaceship rotation rate"])
			if(self.player.model.getH()>360):
				self.player.model.setH(self.player.model.getH()-360)
		if is_down(keys['d']):
			self.player.model.setH(self.player.model.getH()-Game.settings["spaceship rotation rate"])
			if(self.player.model.getH()<0):
				self.player.model.setH(self.player.model.getH()+360)
		if is_down(keys['w']):
			self.player.model.setP(self.player.model.getP()+Game.settings["spaceship rotation rate"])
			if(self.player.model.getP()>360):
				self.player.model.setP(self.player.model.getP()-360)
		if is_down(keys['s']):
			self.player.model.setP(self.player.model.getP()-Game.settings["spaceship rotation rate"])
			if(self.player.model.getP()<0):
				self.player.model.setP(self.player.model.getP()+360)
		if is_down(keys['q']):
			self.player.model.setR(self.player.model.getR()-Game.settings["spaceship rotation rate"])
			if(self.player.model.getR()<0):
				self.player.model.setR(self.player.model.getR()+360)
		if is_down(keys['e']):
			self.player.model.setR(self.player.model.getR()+Game.settings["spaceship rotation rate"])
			if(self.player.model.getR()>360):
				self.player.model.setR(self.player.model.getR()-360)
	def datify(self):
		player_poshpr=list(self.player.model.getPos())+list(self.player.model.getHpr())
		wanderers_pos=[]
		for wanderer in self.wanderers:
			wanderers_pos+=[round(item,3) for item in list(wanderer.model.getPos())]
		planets_poss=[]
		for planet in self.planets:
			planets_poss+=([round(item,3) for item in list(planet[0].model.getPos())+[float(planet[0].model.getScale()[0])]])
		drones_poshpr=[]
		for drone in self.drones:
			drones_poshpr+=([round(item,3) for item in list(drone.model.getPos())+list(drone.model.getHpr())])
		#print(str(player_poshpr)+"|"+str(wanderers_pos)+"|"+str(planets_poss)+"|"+str(drones_poshpr))
		#return [self.player,self.wanderers,self.planets,self.drones]
		return str(player_poshpr)+"|"+str(wanderers_pos)+"|"+str(planets_poss)+"|"+str(drones_poshpr)
		#need player xyz,hpr
		#need wanderers xyz
		#need planets xyz, size
		#need drones xyz,hpr
	def apply_data(self, data):
		#print(data)
		data_chunks=data.split("|")
		if len(data_chunks[0]) == 0:
			return
		player_poshpr=[float(datapoint) for datapoint in data_chunks[0].strip('][').split(', ')]
		wanderers_pos=group([float(datapoint) for datapoint in data_chunks[1].strip('][').split(', ')],3)
		planets_poss=group([float(datapoint) for datapoint in data_chunks[2].strip('][').split(', ')],4)
		drones_poshpr=group([float(datapoint) for datapoint in data_chunks[3].strip('][').split(', ')],6)
		self.player2.model.setPos(player_poshpr[0],player_poshpr[1],player_poshpr[2])
		self.player2.model.setHpr(player_poshpr[3],player_poshpr[4],player_poshpr[5])
		if sType=="client":
			for index,wanderer in enumerate(self.wanderers):
				wanderer.model.setPos(wanderers_pos[index])
			for index,planet in enumerate(self.planets):
				planet[0].model.setPos(planets_poss[index][0],planets_poss[index][1],planets_poss[index][2])
				planet[0].model.setScale(planets_poss[index][3])
			for index,drone in enumerate(self.drones):
				if index>=len(drones_poshpr):
					break
				drone.model.setPos(drones_poshpr[index][0:3])
				drone.model.setHpr(drones_poshpr[index][3:6])
				
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
class Wanderer(Item,Destructable):
	def __init__(self,size:float):
		super(Wanderer,self).__init__(getRandomPoint(),size,Game.models["outer sphere"], Game.textures["missing texture"])
		self.target=getRandomPoint()
		self.model.setBillboardPointWorld()
	def loop(self):
		if sType=="server":
			self.model.lookAt(self.target)
			self.trajectory=base.render.getRelativeVector(self.model,Vec3.forward())
			self.trajectory.normalize()
			self.model.setFluidPos(self.model.getPos()+self.trajectory*Game.settings["spaceship thrust"])
			if getDistance(self.model,self.target)<100:
				self.target=getRandomPoint()
		self.model.lookAt(app.player.model)
class Explosion():
	def __init__(self,posVec:Vec3):
		self.card=Card(posVec,10,Game.textures["sparkle"])
		LerpFunc(self.explode, 5.0, 0, 1).start()
	def explode(self,completion):
		self.card.model.setScale(self.card.model.getScale()*.9)
		if math.floor(completion):
			self.card.model.removeNode()

host = socket.gethostname()
port = 5000


try:
	active_socket = socket.socket()
	active_socket.connect((host, port))
	sType="client"
except ConnectionRefusedError:
	active_socket = socket.socket()
	active_socket.bind((host, port))
	active_socket.listen(2)
	conn, address = active_socket.accept()
	sType="server"
print(sType)
def recvall(sock):
	BUFF_SIZE = 4096 # 4 KiB
	data = b''
	while True:
		part = sock.recv(BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			# either 0 or end of data
			break
	return data
def coms():
	global newgamedata
	if sType == "client":
		while True:
			time.sleep(.05)
			data=recvall(active_socket).decode()
			if not data:
				break
			newgamedata=data
		active_socket.close()
	elif sType == "server":
		while True:
			time.sleep(.05)
			data=recvall(conn).decode()
			if not data:
				break
			newgamedata=data
		conn.close()
	return False
def coms2():
	if sType == "client":
		while True:
			time.sleep(.05)
			active_socket.send(gamedata.encode())
		active_socket.close()
	elif sType == "server":
		while True:
			time.sleep(.05)
			conn.send(gamedata.encode())
		conn.close()
	return False
comms=threading.Thread(target = coms).start()
comms=threading.Thread(target = coms2).start()
app = Game()
app.run()