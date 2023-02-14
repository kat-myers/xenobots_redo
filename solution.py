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
        self.weights = []
        self.numSensorNeurons = 0
        self.numMotorNeurons = 0
        self.cube_list = []
        self.num_segments = 0
        self.sensor_loci = []
        self.num_joints = 0
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        # [ movement away from camera (farther away from the origin of the thing), movement left and right, up and down]

        # initializes number of segments and which ones will have a sensor
        self.num_segments = random.randint(1,10)
        print('num_segments')
        print(self.num_segments)
        self.cube_list = np.arange(0, self.num_segments)
        for i in range(self.num_segments):
             flip_coin = random.randint(0, 1)
             self.sensor_loci.append(flip_coin)
             
        # makes the snake with no neurons
        for i in range(self.num_segments):
            size_dummy = np.zeros(3)
            for x in range(2):
                size_dummy[x] = random.random()
            
            if i == 0:
                pyrosim.Send_Cube(name= str(i), pos= [0,0,size_dummy[2]/2], size= size_dummy, x= self.sensor_loci[i])
                #np.append(self.cube_list, )
                joint_position = [0, size_dummy[1]/2, size_dummy[2]/2]
                pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1) , parent= str(i), child = str(i+1) , type = "revolute", position = joint_position, jointAxis = "1 0 0")
                self.num_joints += 1 
            
            else:
                # relative to previous joint
                pyrosim.Send_Cube(name= str(i), pos= [0,size_dummy[1]/2,0], size= size_dummy, x= self.sensor_loci[i])
                # relative to previous joint
                if self.num_joints < (self.num_segments-1):
                    pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1), parent = str(i), child = str(i+1), type = "revolute", position = size_dummy, jointAxis = "1 0 0")   
                    self.num_joints += 1 
                    print('num_joints')
                    print(self.num_joints)
                    print('joint')
                    print(str(i)+'_'+ str(i+1))
        
        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        
        for i in range(self.num_segments):
            if self.sensor_loci[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = "s"+str(i), linkName = str(i))
                self.numSensorNeurons += 1
            if i < (self.num_segments-1):
                pyrosim.Send_Motor_Neuron(name = "m"+str(i), jointName = str(i)+'_'+ str(i+1))
            self.numMotorNeurons = self.num_joints
        
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons)
        self.weights = 2*self.weights - 1

        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+self.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        
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
