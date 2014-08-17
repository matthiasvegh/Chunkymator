#!/usr/bin/env python

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

def getCameraAngles(xSpline, ySpline, zSpline, times, fixedX=None, fixedY=None, fixedZ=None):

    yawVals = []
    pitchVals = []
    for frame in range(int(times[-1])):
        currentXVal = xSpline(frame)
        currentYVal = ySpline(frame)
        currentZVal = zSpline(frame)

        nextXVal = xSpline(frame+1) if fixedX is None else fixedX
        nextYVal = ySpline(frame+1) if fixedY is None else fixedY
        nextZVal = zSpline(frame+1) if fixedZ is None else fixedZ

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

def createRegularSpline(times, values):
	return UnivariateSpline(times, values)


def main():
    parser = optparse.OptionParser(
            usage="%prog [options] scene1 scene2 scene3 scene4 ...",
            description="Chunkymator scene interpolator."
            "Source available at https://github.com/matthiasvegh/Chunkymator")
    parser.add_option("-o", "--outputdir", dest="outputdir",
            help="Directory to place interpoalted scenes to.",
            metavar="DIR")
    parser.add_option("-f", "--frame-rate", dest="frameRate",
            help="What frame rate you intend to play back thetae interpolated images (default: %default fps).",
            metavar="NUM", default=25, type=float)
    parser.add_option("-s", "--traveling-speed", dest="flyingSpeed",
            help="What speed the camera should be traveling (default: %default m/s).",
            metavar="NUM", default=5.4, type=float)
    cameraPointOptionsGroup = optparse.OptionGroup(parser, "Camera settings",
            "If you specify these, the camera will always point in the direction of "
            "these coordinates, if you do not specify them, the camera shall always "
            "point forward."
            "Either specify them all, or specify none.")
    cameraPointOptionsGroup.add_option("-x", "--focus-on-x",
            help="X coordinate of where camera should look.",
            dest="cameraX",
            metavar="NUM", type=float)
    cameraPointOptionsGroup.add_option("-y", "--focus-on-y",
            help="Y coordinate of where camera should look.",
            dest="cameraY",
            metavar="NUM", type=float)
    cameraPointOptionsGroup.add_option("-z", "--focus-on-z",
            help="Z coordinate of where camera should look.",
            dest="cameraZ",
            metavar="NUM", type=float)

    parser.add_option_group(cameraPointOptionsGroup)

    (options, scenes) = parser.parse_args()

    fixedCameraCoord = (options.cameraX, options.cameraY, options.cameraZ)

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
    v = options.flyingSpeed
    r = options.frameRate
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

    xSpline = createRegularSpline(times, xVals)
    ySpline = createRegularSpline(times, yVals)
    zSpline = createRegularSpline(times, zVals)
    sunAltitudeSpline = createRegularSpline(times, sunAltitudeVals)
    sunAzimuthSpline = createRegularSpline(times, sunAzimuthVals)

    yawPath, pitchPath = getCameraAngles(xSpline, ySpline, zSpline, times, *fixedCameraCoord)

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

