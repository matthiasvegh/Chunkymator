import json


def rad2deg(theta):
    if theta > 2 * 3.14159265358:
        return rad2deg(theta - 2 * 3.14159265358)
    if theta < 0.0:
        return rad2deg(theta + 2 * 3.14159265358)
    return theta * 180 / 3.14159265358


def deg2rad(theta):
    if theta > 360.0:
        return deg2rad(theta - 360)
    if theta < 0.0:
        return deg2rad(theta + 360)
    return theta * 3.14159265358 / 180


class cvf(object):

    def getX(self):
        return self.inputJson['camera']['position']['x']

    def getY(self):
        return self.inputJson['camera']['position']['y']

    def getZ(self):
        return self.inputJson['camera']['position']['z']

    def getPitch(self):
        return self.inputJson['camera']['orientation']['pitch']

    def getYaw(self):
        return self.inputJson['camera']['orientation']['yaw']

    def getSunAltitude(self):
        return self.inputJson['sun']['altitude']

    def getSunAzimuth(self):
        return self.inputJson['sun']['azimuth']

    def getSunIntensity(self):
        return self.inputJson['sun']['intensity']

    def setX(self, fl):
        self.inputJson['camera']['position']['x'] = fl

    def setY(self, fl):
        self.inputJson['camera']['position']['y'] = fl

    def setZ(self, fl):
        self.inputJson['camera']['position']['z'] = fl

    def setYaw(self, flr):
        fl = deg2rad(flr)
        self.inputJson['camera']['orientation']['yaw'] = fl

    def setPitch(self, flr):
        fl = deg2rad(flr)
        self.inputJson['camera']['orientation']['pitch'] = fl

    def setSunAltitude(self, fl):
        self.inputJson['sun']['altitude'] = fl

    def setSunAzimuth(self, fl):
        self.inputJson['sun']['azimuth'] = fl

    def setSunIntensity(self, fl):
        self.inputJson['sun']['intensity'] = fl

    def setName(self, f):
        self.filename = f
        self.inputJson['name'] = f

    def saveToFile(self, filename):
        with open(filename, 'w+') as f:
            json.dump(self.inputJson, f)

    filename = ""
    inputJson = {}

    def __init__(self, name):
        self.filename = name
        inputJsonString = open(name).read()

        self.inputJson = json.loads(inputJsonString)
