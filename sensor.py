#Imports
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.iterations)
                       
    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        
    def Save_Values(self):
        np.save("data/sensorValues", self.values)