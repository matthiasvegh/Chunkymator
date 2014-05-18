#!/usr/bin/env python

print "CVF Generator for chunky."
print "loading dependancies..."
import struct
import os
import copy
import json


from scipy.interpolate import UnivariateSpline
from math import sin, cos, tan, asin, acos, atan2

def rad2deg(theta):
	if theta > 2*3.14159265358:
		return rad2deg(theta-2*3.14159265358)
	if theta < 0.0:
		return rad2deg(theta+2*3.14159265358)
	return theta * 180/3.14159265358

def deg2rad(theta):
	if theta > 360.0:
		return deg2rad(theta-360)
	if theta < 0.0:
		return deg2rad(theta+360)
	return theta * 3.14159265358/180

class cvf:
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getZ(self):
		return self.z
	def getPitch(self):
		return rad2deg(self.pitch)
	def getYaw(self):
		return rad2deg(self.yaw)

	def setX(self, fl):
		self.x = fl
		self.inputJson['camera']['position']['x'] = fl
	def setY(self, fl):
		self.y = fl
		self.inputJson['camera']['position']['y'] = fl
	def setZ(self, fl):
		self.z = fl
		self.inputJson['camera']['position']['z'] = fl
	def setYaw(self, flr):
		fl = deg2rad(flr)
		self.inputJson['camera']['orientation']['yaw'] = fl
	def setPitch(self, flr):
		fl = deg2rad(flr)
		self.inputJson['camera']['orientation']['pitch'] = fl

	def setName(self, f):
		self.filename = f
		self.inputJson['name'] = f
	def saveToFile(self, filename):
		with open(filename, 'w+') as f:
			json.dump(self.inputJson, f)


	filename = ""
	x = 0.0
	y = 0.0
	z = 0.0
	pitch = 0.0
	yaw = 0.0
	inputJson = {}

	def __init__(self, name):
		self.filename = name
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.pitch = 0.0
		self.yaw = 0.0

		inputJsonString = open(name).read()

		self.inputJson = json.loads(inputJsonString)

		self.x = self.inputJson['camera']['position']['x']
		self.y = self.inputJson['camera']['position']['y']
		self.z = self.inputJson['camera']['position']['z']
		self.pitch = self.inputJson['camera']['orientation']['pitch']
		self.yaw = self.inputJson['camera']['orientation']['yaw']


def normalize(list, ammount=180):
	for i in range(len(list)-1):
		if(list[i+1] - list[i] > ammount):
			list[i+1] -= 2*ammount
		elif(list[i+1] - list[i] < -ammount):
			list[i+1] += 2*ammount

def main():
	print "done loading"
	num = int(raw_input("How many files to interpolate?"))
	cvfList = []
	i = 0
	if num < 4:
		print "This script requires at least 4 input jsons to generate a route between them."
		return

	baseFilename = raw_input("Filenamebase? If empty, will prompt for all files.")


	while i<num:
		try:
			if baseFilename != "":
				filename = baseFilename+str(i)+".json"
				print "loading ",filename
			else:
				filename = raw_input("Please enter filename for json #"+str(i+1)+" ")


			c = cvf(filename)
			cvfList.append(c)
			print ("X: "+str(c.getX())+
				" Y: "+str(c.getY())+
				" Z: "+str(c.getZ())+
				" Pitch: "+str(c.getPitch())+
				" Yaw: "+str(c.getYaw()) )

			i += 1
		except EnvironmentError as err:
			print "could not get file #"+str(i+1)+" please try again!"
			pass
	print "done loading "+str(num)+" files."
	outputDir = raw_input("Where shall we place output .jsons?")

	######################## input got, start actual work here.

	totalLength = 0.0

	#############################
	v=5.4		#Flying Speed	#
	r=25		#Frame Rate		#
	#############################

	times = []
	times.append(0)
	xVals = [cvfList[0].getX()]
	yVals = [cvfList[0].getY()]
	zVals = [cvfList[0].getZ()]
	pitchVals = [cvfList[0].getPitch()]
	yawVals = [cvfList[0].getYaw()]

	for i in range(num-1):
		# calculate euclidean distance between (i)->(i+1)
		nextFrame = (i+1)%num
		nextNextFrame = (i+2)%num
		lastFrame = (i)%num
		dx = cvfList[nextFrame].getX() - cvfList[lastFrame].getX()
		dy = cvfList[nextFrame].getY() - cvfList[lastFrame].getY()
		dz = cvfList[nextFrame].getZ() - cvfList[lastFrame].getZ()
		length = ((dx*dx+dy*dy+dz*dz)**.5)

		totalLength += length
		times.append( r*(totalLength/v) )

		x = cvfList[nextFrame].getX()
		y = cvfList[nextFrame].getY()
		z = cvfList[nextFrame].getZ()
		pitch = cvfList[nextFrame].getPitch()
		yaw = cvfList[nextFrame].getYaw()

		xVals.append(x)
		yVals.append(y)
		zVals.append(z)
		pitchVals.append(pitch)
		yawVals.append(yaw)



	print "length of requested route: "+str(totalLength)+"m"

	print "total number of frames to be generated: "+str(int(r*(totalLength/v)))

	# Handle camera modularities here
	# if distance between values is >180deg, shift camera value up/down 360
	normalize(pitchVals)
	normalize(yawVals)


	xSpline = UnivariateSpline(times, xVals)
	ySpline = UnivariateSpline(times, yVals)
	zSpline = UnivariateSpline(times, zVals)
	pitchSpline = UnivariateSpline(times, pitchVals)
	yawSpline = UnivariateSpline(times, yawVals)


	localCVFs = []


	for i in range(int(times[-1])):

		x = xSpline(i)
		y = ySpline(i)
		z = zSpline(i)
		pitch = yawSpline(i)
		yaw = pitchSpline(i)
		c=copy.deepcopy(cvfList[-1])
		c.setX(x)
		c.setY(y)
		c.setZ(z)
		c.setPitch(pitch)
		c.setYaw(yaw)

		print (str(i)+": "
				"X: "+str(c.getX())+
				" Y: "+str(c.getY())+
				" Z: "+str(c.getZ())+
				" Pitch: "+str(c.getPitch())+
				" Yaw: "+str(c.getYaw()) )
		localCVFs.append(c)


	for i in range(len(localCVFs)):
		c = localCVFs[i]
		name = os.path.join(outputDir, "interpolated-"+str(i)+".json")
		c.setName("interpolated-"+str(i))
		c.saveToFile(name);



if __name__ == "__main__":
	main()

