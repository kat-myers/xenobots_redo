import pyrosim.pyrosim as pyrosim
import numpy
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import constants as c
import pybullet as p
import time
from world import WORLD

def Create_World():
    length = 1
    width = 1
    height = 1
    x = 3
    y = 3
    z = .5

    pyrosim.Start_SDF("world.sdf")
    pyrosim.End()

Create_World()

def Generate_Body():
    length = 1
    width = 1
    height = 1
    x = 3
    y = 3
    z = .5
    pyrosim.Start_URDF("body.urdf")   
    pyrosim.Send_Cube(name = "Torso", pos = [1.5,0,1.5], size = [length,width,height])
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name = "BackLeg", pos = [-.5,0,-.5], size = [length,width,height])
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
    pyrosim.Send_Cube(name = "FrontLeg", pos = [.5,0,-.5], size = [length,width,height])
    pyrosim.End()

Generate_Body()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
    pyrosim.End()

Generate_Brain()



#%%
#%%