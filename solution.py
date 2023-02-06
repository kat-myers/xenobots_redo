#Imports
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import random
import os
import time

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = 2*self.weights - 1
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-3,-3,0.5] , size=[1,1,1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
    
        ## Torso
        #pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,3,1])
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1])        
        
        
        ## Extra Torso Segments
        pyrosim.Send_Joint(name = "Torso_Torso2" , parent= "Torso" , child = "Torso2" , type = "revolute", position = [0,0.5,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Torso2", pos=[0,0.5,0] , size=[1,1,.5])
        
        pyrosim.Send_Joint(name = "Torso_Torso3" , parent= "Torso" , child = "Torso3" , type = "revolute", position = [0,-0.5,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Torso3", pos=[0,-0.5,0] , size=[1,1,.5])

        ## Right Leg 1
        # joint absolute
        pyrosim.Send_Joint(name = "Torso_RightLeg1" , parent= "Torso" , child = "RightLeg1" , type = "revolute", position = [0.5,0,1], jointAxis = "0 0 1")
        # leg relative to above joint
        pyrosim.Send_Cube(name="RightLeg1", pos=[0.5,0,0] , size=[1,0.2,0.2])
        
        # joint relative to above joint
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg1" , parent= "RightLeg1" , child = "RightLowerLeg1" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        # leg relative to above joint
        pyrosim.Send_Cube(name="RightLowerLeg1", pos=[0,0,-0.5] , size=[0.2,0.2,1])      

        
        ## Right Leg 2
        # relative to torso 2
        pyrosim.Send_Joint(name = "Torso2_RightLeg2" , parent= "Torso2" , child = "RightLeg2" , type = "revolute", position = [.5,.5,0], jointAxis = "0 0 1")
        pyrosim.Send_Cube(name="RightLeg2", pos=[0.5,0,0] , size=[1,0.2,0.2])  

        # joint relative to above joint
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg2" , parent= "RightLeg2" , child = "RightLowerLeg2" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        # leg relative to above joint
        pyrosim.Send_Cube(name="RightLowerLeg2", pos=[0,0,-0.5] , size=[0.2,0.2,1])      

        ## Right Leg 3
        # relative to torso 3
        pyrosim.Send_Joint(name = "Torso3_RightLeg3" , parent= "Torso3" , child = "RightLeg3" , type = "revolute", position = [.5,-.5,0], jointAxis = "0 0 1")
        pyrosim.Send_Cube(name="RightLeg3", pos=[0.5,0,0] , size=[1,0.2,0.2])  

        # joint relative to above joint
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg3" , parent= "RightLeg3" , child = "RightLowerLeg3" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        # leg relative to above joint
        pyrosim.Send_Cube(name="RightLowerLeg3", pos=[0,0,-0.5] , size=[0.2,0.2,1])   

        # [ movement away from camera (farther away from the origin of the thing), movement left and right, up and down]
        # torso 2 is farther away from camera

        ## Left Leg 1
        # joint absolute
        pyrosim.Send_Joint(name = "Torso_LeftLeg1" , parent= "Torso" , child = "LeftLeg1" , type = "revolute", position = [-0.5,0,1], jointAxis = "0 0 1")
        # cube is relative to above joint
        pyrosim.Send_Cube(name="LeftLeg1", pos=[-0.5,0,0] , size=[1,0.2,0.2])
        
        # joint is relative to above joint
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg1" , parent= "LeftLeg1" , child = "LeftLowerLeg1" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        # cube is relative to above joint
        pyrosim.Send_Cube(name="LeftLowerLeg1", pos=[0,0,-0.5] , size=[0.2,0.2,1])        
    
        ## Left Leg 2
        # relative to torso 2
        pyrosim.Send_Joint(name = "Torso2_LeftLeg2" , parent= "Torso2" , child = "LeftLeg2" , type = "revolute", position = [-.5,.5,0], jointAxis = "0 0 1")
        # cube is relative to above joint
        pyrosim.Send_Cube(name="LeftLeg2", pos=[-0.5,0,0] , size=[1,0.2,0.2])
        
        # joint is relative to above joint
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg2" , parent= "LeftLeg2" , child = "LeftLowerLeg2" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        # cube is relative to above joint
        pyrosim.Send_Cube(name="LeftLowerLeg2", pos=[0,0,-0.5] , size=[0.2,0.2,1]) 

        ## Left Leg 3
        # relative to torso 3
        pyrosim.Send_Joint(name = "Torso3_LeftLeg3" , parent= "Torso3" , child = "LeftLeg3" , type = "revolute", position = [-.5,-.5,0], jointAxis = "0 0 1")
        # cube is relative to above joint
        pyrosim.Send_Cube(name="LeftLeg3", pos=[-0.5,0,0] , size=[1,0.2,0.2])
        
        # joint is relative to above joint
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg3" , parent= "LeftLeg3" , child = "LeftLowerLeg3" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        # cube is relative to above joint
        pyrosim.Send_Cube(name="LeftLowerLeg3", pos=[0,0,-0.5] , size=[0.2,0.2,1])
    
        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
    
       # # pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
       # # pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
       # # pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
       # # pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLeg")
       # # pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLeg")
        
        # pyrosim.Send_Sensor_Neuron(name = 0, linkName = "BackLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 1, linkName = "FrontLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2, linkName = "LeftLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3, linkName = "RightLowerLeg")

        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "LeftLowerLeg1")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "LeftLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "LeftLowerLeg3")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "RightLowerLeg1")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 5, linkName = "RightLowerLeg3")

        pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_LeftLeg1")
        pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso2_LeftLeg2")
        pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso3_LeftLeg3")
        pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_RightLeg1")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso2_RightLeg2")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "Torso3_RightLeg3")

        pyrosim.Send_Motor_Neuron(name = 12, jointName = "LeftLeg_LeftLowerLeg1")
        pyrosim.Send_Motor_Neuron(name = 13, jointName = "LeftLeg_LeftLowerLeg2")
        pyrosim.Send_Motor_Neuron(name = 14, jointName = "LeftLeg_LeftLowerLeg3")
        pyrosim.Send_Motor_Neuron(name = 15, jointName = "RightLeg_RightLowerLeg1")
        pyrosim.Send_Motor_Neuron(name = 16, jointName = "RightLeg_RightLowerLeg2")
        pyrosim.Send_Motor_Neuron(name = 17, jointName = "RightLeg_RightLowerLeg3")

        # pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_BackLeg")
        # pyrosim.Send_Motor_Neuron(name = 5, jointName = "Torso_FrontLeg")
        # pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_LeftLeg")
        # pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso_RightLeg")
        # pyrosim.Send_Motor_Neuron(name = 8, jointName = "BackLeg_BackLowerLeg")
        # pyrosim.Send_Motor_Neuron(name = 9, jointName = "FrontLeg_FrontLowerLeg")
        # pyrosim.Send_Motor_Neuron(name = 10, jointName = "LeftLeg_LeftLowerLeg")
        # pyrosim.Send_Motor_Neuron(name = 11, jointName = "RightLeg_RightLowerLeg")
    
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
        
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        
        #os.system("py simulate.py " + str(directOrGUI) + " " + str(self.myID) + " 2&>1&")
        os.system("start /B py simulate.py " + str(directOrGUI) + " " + str(self.myID))
        
    def Wait_For_Simulation_To_End(self, directOrGUI):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(10)
        
        f = open("fitness" + str(self.myID) + ".txt", "r")
        fitnessString = f.readline()
        self.fitness = float(fitnessString)
        f.close()
        
        os.system("del " + "fitness" + str(self.myID) + ".txt")        

    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0,1)
        self.weights[randomRow,randomColumn] = 2*random.random() - 1

    def Set_ID(self, newID):
        self.myID = newID
