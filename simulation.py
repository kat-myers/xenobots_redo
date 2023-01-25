import numpy
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import constants as c
import pybullet as p
import time
from world import WORLD
from sensor import SENSOR
from robot import ROBOT

class SIMULATION: #names class
    def __init__(self): # defines constructor for class
        self.world = WORLD()
        self.robot = ROBOT()
    
    def Run(self):
        for i in range(c.iterations):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)
            time.sleep(c.sleep_time)
    
    def __del__(self):
        p.disconnect