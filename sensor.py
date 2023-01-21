import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import pybullet as p
import pybullet_data
import constants as c

class SENSOR: #names class
    def __init__(self, linkName): # defines constructor for class
        self.linkName = linkName
        self.values = np.zeros(c.iterations)

    def Get_Value(self,t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if t == c.iterations - 1:
            print(self.values)

    def Save_Values(self):
        np.save('data/sensorValues.npy', self.values)