import math
from random import random
from panda3d.core import *
def Cloud(radius=1):
	x=2*random()-1
	y=2*random()-1
	z=2*random()-1
	unitVec=Vec3(x,y,z)
	unitVec.normalize()
	return unitVec*radius
def XY(step,count,radius=1):
	theta=step*2*math.pi/count
	x=math.cos(theta)
	y=math.sin(theta)
	z=0
	unitVec=Vec3(x,y,z)
	unitVec.normalize()
	return unitVec*radius
def XZ(step,count,radius=1):
	theta=step*2*math.pi/count
	x=math.cos(theta)
	y=0
	z=math.sin(theta)
	unitVec=Vec3(x,y,z)
	unitVec.normalize()
	return unitVec*radius
def YZ(step,count,radius=1):
	theta=step*2*math.pi/count
	x=0
	y=math.sin(theta)
	z=math.cos(theta)
	unitVec=Vec3(x,y,z)
	unitVec.normalize()
	return unitVec*radius
def BaseballSeams(step,numSeams,B,radius=1,F=1):
	time=step/float(numSeams)*2*math.pi
	F4=0
	R=1
	xxx=math.cos(time)-B*math.cos(3*time)
	yyy=math.sin(time)+B*math.sin(3*time)
	zzz=F*math.cos(2*time)+F4*math.cos(4*time)
	rrr=math.sqrt(xxx**2+yyy**2+zzz**2)
	x=xxx/rrr
	y=yyy/rrr
	z=zzz/rrr
	return Vec3(x,y,z)*radius