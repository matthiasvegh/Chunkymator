#!/usr/bin/env python

import os
import copy
import optparse
from cvf import *
from dictionary_spline import *

from math import sin, cos, tan, asin, acos, atan2, sqrt, pi

def getCameraAngles(xSpline, ySpline, zSpline, frames, fixedX=None, fixedY=None, fixedZ=None):

    yawVals = []
    pitchVals = []
    for frame in range(int(frames)):
        currentXVal = xSpline[frame]
        currentYVal = ySpline[frame]
        currentZVal = zSpline[frame]

        nextXVal = xSpline[(frame+1) % frames] if fixedX is None else fixedX
        nextYVal = ySpline[(frame+1) % frames] if fixedY is None else fixedY
        nextZVal = zSpline[(frame+1) % frames] if fixedZ is None else fixedZ

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

def getTimes(cvfList, r, v, fixedLength=None):
    times = [0.0]
    totalLength = 0.0

    xes = [cvf.getX() for cvf in cvfList]
    yes = [cvf.getY() for cvf in cvfList]
    zes = [cvf.getZ() for cvf in cvfList]
    areAllSame = (
            xes.count(xes[0]) == len(xes) and
            yes.count(yes[0]) == len(yes) and
            zes.count(zes[0]) == len(zes))

    if areAllSame and len(cvfList) > 1:
        times = [i*(fixedLength)/(len(cvfList) -1) for i in range(len(cvfList))]
        totalLength = fixedLength
    else:
        for i in range(len(cvfList) -1):
            previousFrame = cvfList[i]
            nextFrame = cvfList[i+1]

            dx = nextFrame.getX() - previousFrame.getX()
            dy = nextFrame.getY() - previousFrame.getY()
            dz = nextFrame.getZ() - previousFrame.getZ()

            distance = (dx*dx + dy*dy + dz*dz)**0.5

            times.append(distance*r/v)
            times[-1] += times[-2]
            totalLength += distance

    if fixedLength is not None:
        factor = fixedLength / times[-1]
        times[:] = [time*factor for time in times]

    return (times, totalLength)

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
    parser.add_option("-t", "--length", dest="length",
            help="Usually the number of intermediate jsons to be generated are calcualated by taking "
            "the distance between keyframes. This can be overridden by setting this option.",
            metavar="NUM", type=int)
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


    #############################
    v = options.flyingSpeed
    r = options.frameRate
    #############################

    times, totalLength = getTimes(cvfList, r, v, options.length)

    print "length of requested route: "+str(totalLength)+"m"

    print "total number of frames to be generated: "+str(int(r*(totalLength/v)))


    jsonList = [c.inputJson for c in cvfList]
    jsonSpline = VectorSpline([jsonList], times)

    localCVFs = []

    for i in range(int(times[-1])):

        json = jsonSpline(i)[0]
        c=copy.deepcopy(cvfList[-1])
        c.inputJson = json
        c.inputJson['renderTime'] = cvfList[-1].inputJson['renderTime']
        localCVFs.append(c)

    xValues = []
    yValues = []
    zValues = []
    print times

    for cvf_ in localCVFs:
        xValues.append(cvf_.getX())
        yValues.append(cvf_.getY())
        zValues.append(cvf_.getZ())

    yawPath, pitchPath = getCameraAngles(xValues, yValues, zValues, len(localCVFs), *fixedCameraCoord)

    for cvfIndex in range(len(localCVFs)):
        localCVFs[cvfIndex].setYaw(yawPath[cvfIndex])
        localCVFs[cvfIndex].setPitch(pitchPath[cvfIndex])

    for i in range(len(localCVFs)):
        c = localCVFs[i]
        name = os.path.join(outputDir, "interpolated-"+str(i)+".json")
        c.setName("interpolated-"+str(i))
        print (str(i)+": "
                "X: "+str(c.getX())+
                " Y: "+str(c.getY())+
                " Z: "+str(c.getZ())+
                " Pitch: "+str(c.getPitch())+
                " Yaw: "+str(c.getYaw())+
                " Sun Altitude: "+str(c.getSunAltitude())+
                " Sun Azimuth: "+str(c.getSunAzimuth()))
        c.saveToFile(name);



if __name__ == "__main__":
    main()

