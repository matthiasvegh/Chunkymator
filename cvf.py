import json

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

    def getSunAltitude(self):
        return self.sun_altitude
    def getSunAzimuth(self):
       return self.sun_azimuth
    def getSunIntensity(self):
       return self.sun_intensity

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
    def setSunAltitude(self, fl):
        self.sun_altitude = fl
        self.inputJson['sun']['altitude'] = fl
    def setSunAzimuth(self, fl):
        self.sun_azimuth = fl
        self.inputJson['sun']['azimuth'] = fl
    def setSunIntensity(self, fl):
        self.sun_intensity = fl
        self.inputJson['sun']['intensity'] = fl

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

    sun_altitude = 0.0
    sun_azimuth = 0.0
    sun_intensity = 0.0
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

        self.sun_altitude = self.inputJson['sun']['altitude']
        self.sun_azimuth = self.inputJson['sun']['azimuth']
        self.sun_intensity = self.inputJson['sun']['intensity']



