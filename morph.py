#!/usr/bin/env python

print "CVF Generator for chunky."
print "loading dependancies..."
import struct
import readline
import os
import copy
import optparse
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

        yaw = atan2(dx, dz) + pi/2
        pitch = atan2(sqrt(dz*dz + dx*dx), dy) + pi

        yawVals.append(rad2deg(yaw))
        pitchVals.append(rad2deg(pitch))

    yawVals.append(yawVals[-1])
    pitchVals.append(pitchVals[-1])
    # duplicate last values

    return yawVals, pitchVals


def main():
    parser = optparse.OptionParser(
            usage="%prog [options] scene1 scene2 scene3 scene4 ...",
            description="Chunkymator scene interpolator.")
    parser.add_option("-o", "--outputdir", dest="outputdir",
            help="Directory to place interpoalted scenes to.",
            metavar="DIR")
    print "done loading"
    (options, scenes) = parser.parse_args()

    num = len(scenes)

    cvfList = []
    i = 0
    if num < 4:
        print "This script requires at least 4 input jsons to generate a route between them."
        return


    while i<num:
        try:
            filename = scenes[i]
            print "loading ",filename

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
            return
    print "done loading "+str(num)+" files."
    outputDir = options.outputdir
    if outputDir is None:
        outputDir = './outputs'

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
    sunAltitudeVals = [cvfList[0].getSunAltitude()]
    sunAzimuthVals = [cvfList[0].getSunAzimuth()]

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
        sunAltitude = cvfList[nextFrame].getSunAltitude()
        sunAzimuth = cvfList[nextFrame].getSunAzimuth()

        xVals.append(x)
        yVals.append(y)
        zVals.append(z)
        sunAltitudeVals.append(sunAltitude)
        sunAzimuthVals.append(sunAzimuth)



    print "length of requested route: "+str(totalLength)+"m"

    print "total number of frames to be generated: "+str(int(r*(totalLength/v)))

    xSpline = UnivariateSpline(times, xVals)
    ySpline = UnivariateSpline(times, yVals)
    zSpline = UnivariateSpline(times, zVals)
    sunAltitudeSpline = UnivariateSpline(times, sunAltitudeVals)
    sunAzimuthSpline = UnivariateSpline(times, sunAzimuthVals)

    yawPath, pitchPath = getCameraAngles(xSpline, ySpline, zSpline, times)

    localCVFs = []


    for i in range(int(times[-1])):

        x = xSpline(i)
        y = ySpline(i)
        z = zSpline(i)
        pitch = pitchPath[i]
        yaw = yawPath[i]
        sunAltitude = sunAltitudeSpline(i)
        sunAzimuth = sunAzimuthSpline(i)


        c=copy.deepcopy(cvfList[-1])
        c.setX(x)
        c.setY(y)
        c.setZ(z)
        c.setPitch(pitch)
        c.setYaw(yaw)
        c.setSunAltitude(sunAltitude)
        c.setSunAzimuth(sunAzimuth)

        print (str(i)+": "
                "X: "+str(c.getX())+
                " Y: "+str(c.getY())+
                " Z: "+str(c.getZ())+
                " Pitch: "+str(c.getPitch())+
                " Yaw: "+str(c.getYaw())+
                " Sun Altitude: "+str(c.getSunAltitude())+
                " Sun Azimuth: "+str(c.getSunAzimuth()))
        localCVFs.append(c)


    for i in range(len(localCVFs)):
        c = localCVFs[i]
        name = os.path.join(outputDir, "interpolated-"+str(i)+".json")
        c.setName("interpolated-"+str(i))
        c.saveToFile(name);



if __name__ == "__main__":
    main()

