#!/usr/bin/env python

print "CVF Generator for chunky."
print "loading dependancies..."
import struct
import os
import copy

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
		output = struct.pack('!d', fl)
		start = 111
		for i in range(len(output)):
			self.byteList[start+i] = output[i]
	def setY(self, fl):
		self.y = fl
		output = struct.pack('!d', fl)
		start = 123
		for i in range(len(output)):
			self.byteList[start+i] = output[i]
	def setZ(self, fl):
		self.z = fl
		output = struct.pack('!d', fl)
		start = 135
		for i in range(len(output)):
			self.byteList[start+i] = output[i]
	def setYaw(self, flr):
		fl = deg2rad(flr)
		self.yaw= fl
		output = struct.pack('!d', fl)
		start = 151
		for i in range(len(output)):
			self.byteList[start+i] = output[i]
	def setPitch(self, flr):
		fl = deg2rad(flr)
		self.pitch = fl
		output = struct.pack('!d', fl)
		start = 165
		for i in range(len(output)):
			self.byteList[start+i] = output[i]
	
	def setName(self, f):
		self.filename = f
	def saveToFile(self, filename):
		with open(self.filename, 'wb') as f:
			for b in self.byteList:
				f.write(b)
	
	filename = ""
	x = 0.0
	y = 0.0
	z = 0.0
	pitch = 0.0
	yaw = 0.0
	byteList = []
	def __init__(self, name):
		self.filename = name
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.pitch = 0.0
		self.pitch = 0.0
		self.byteList = []

		with open(self.filename, "rb") as f:
			byte = f.read(1)
			while byte != "":
				self.byteList.append(byte)
				byte = f.read(1)
			
			string = str(bytearray(self.byteList[111 : 119]))
			self.x = struct.unpack('!d', string)[0]
			string = str(bytearray(self.byteList[123 : 131]))
			self.y = struct.unpack('!d', string)[0]
			string = str(bytearray(self.byteList[135 : 143]))
			self.z = struct.unpack('!d', string)[0]
			string = str(bytearray(self.byteList[151 : 159]))
			self.pitch = struct.unpack('!d', string)[0]
			string = str(bytearray(self.byteList[165 : 173]))
			self.yaw = struct.unpack('!d', string)[0]


def main():
	print "done loading"
	num = int(raw_input("How many files to interpolate?"))
	cvfList = []
	i = 0
	if num < 1:
		print "No interpolation for you then!"
		return 
	
	while i<num:
		try:
			filename = raw_input("Please enter filename for cvf #"+str(i+1)+" ")
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
	outputDir = raw_input("Where shall we place output .cvfs?")

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
	
	xSpline = PiecewisePolynomial(times, xVals)
	ySpline = PiecewisePolynomial(times, yVals)
	zSpline = PiecewisePolynomial(times, zVals)
	pitchSpline = PiecewisePolynomial(times, pitchVals)
	yawSpline = PiecewisePolynomial(times, yawVals)
	
	
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
		
		print (		str(i)+": "
					"X: "+str(c.getX())+
					" Y: "+str(c.getY())+
					" Z: "+str(c.getZ())+
					" Pitch: "+str(c.getPitch())+
					" Yaw: "+str(c.getYaw()) )
		localCVFs.append(c)
	
	
	for i in range(len(localCVFs)):
		c = localCVFs[i]
		name = os.path.join(outputDir, "interpolated-"+str(i)+".cvf")
		c.setName(name)
		c.saveToFile(name);
		
	

if __name__ == "__main__":
	main()
