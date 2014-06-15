#!/usr/bin/env python

print "CVF Generator for chunky."
print "loading dependancies..."
import struct
import os
import copy
from cvf import *

from scipy.interpolate import UnivariateSpline
from math import sin, cos, tan, asin, acos, atan2, sqrt, pi

def normalize(list, ammount=180):
    for i in range(len(list)-1):
        if(list[i+1] - list[i] > ammount):
            list[i+1] -= 2*ammount
        elif(list[i+1] - list[i] < -ammount):
            list[i+1] += 2*ammount

def getCameraAngles(xSpline, ySpline, zSpline, times):

    yawVals = []
    pitchVals = []
    for frame in range(int(times[-1])):
        currentXVal = xSpline(frame)
        currentYVal = ySpline(frame)
        currentZVal = zSpline(frame)

        nextXVal = xSpline(frame+1)
        nextYVal = ySpline(frame+1)
        nextZVal = zSpline(frame+1)

        dx = nextXVal - currentXVal
        dy = nextYVal - currentYVal
        dz = nextZVal - currentZVal

        yaw = atan2(dz, dx)
        pitch = atan2(sqrt(dz*dz + dx*dx), dy) + pi

        yawVals.append(rad2deg(yaw))
        pitchVals.append(rad2deg(pitch))
        print rad2deg(yaw), rad2deg(pitch)

    yawVals.append(yawVals[-1])
    pitchVals.append(pitchVals[-1])
    # duplicate last values

    return yawVals, pitchVals


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
                filename = baseFilename+str(i+1).zfill(3)+".json"
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
    v=5.4       #Flying Speed   #
    r=25        #Frame Rate         #
    #############################

    times = []
    times.append(0)
    xVals = [cvfList[0].getX()]
    yVals = [cvfList[0].getY()]
    zVals = [cvfList[0].getZ()]

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

        xVals.append(x)
        yVals.append(y)
        zVals.append(z)



    print "length of requested route: "+str(totalLength)+"m"

    print "total number of frames to be generated: "+str(int(r*(totalLength/v)))

    xSpline = UnivariateSpline(times, xVals)
    ySpline = UnivariateSpline(times, yVals)
    zSpline = UnivariateSpline(times, zVals)

    yawPath, pitchPath = getCameraAngles(xSpline, ySpline, zSpline, times)

    localCVFs = []


    for i in range(int(times[-1])):

        x = xSpline(i)
        y = ySpline(i)
        z = zSpline(i)
        pitch = pitchPath[i]
        yaw = yawPath[i]


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

