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
        self.num_segments_1 = random.randint(0,4)
        self.num_segments_2 = random.randint(0,4)
        self.num_segments_3 = random.randint(0,4)
        self.num_segments_4 = random.randint(0,4)
        
        self.sensor_loci_1 = []
        self.sensor_loci_2 = []
        self.sensor_loci_3 = []
        self.sensor_loci_4 = []
        
        self.num_joints_1 = 0
        self.num_joints_2 = 0
        self.num_joints_3 = 0
        self.num_joints_4 = 0

        self.i_start_1 = 1
        self.i_start_2 = 5
        self.i_start_3 = 10
        self.i_start_4 = 15

    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        # [ movement away from camera (farther away from the origin of the thing), movement left and right, up and down]
             
        ### MAKE THE TORSO
        flip_coin = random.randint(0,1)
        self.sensor_loci_1.append(flip_coin)
        size_dummy = np.zeros(3)
        for x in range(3):
            size_dummy[x] = random.uniform(0,1)
        pyrosim.Send_Cube(name= str(0), pos= [0,size_dummy[1]/2,size_dummy[2]/2], size= size_dummy, x= self.sensor_loci_1[0])
        
        if self.num_segments_1 > 0:
            print('self.num_segments_1' + str(self.num_segments_1))
            joint_position = [0, size_dummy[1]/2, size_dummy[2]/2]
            pyrosim.Send_Joint(name = '0_1' , parent= str(0), child = str(1) , type = "revolute", position = joint_position, jointAxis = "1 0 0")
            self.num_joints_1 += 1

        if self.num_segments_2 > 0:
            print('self.num_segments_2' + str(self.num_segments_2))
            joint_position = [0, -size_dummy[1]/2, size_dummy[2]/2]
            pyrosim.Send_Joint(name = '0_5' , parent= str(0), child = str(self.i_start_2) , type = "revolute", position = joint_position, jointAxis = "1 0 0")
            self.num_joints_2 += 1
    
        # if self.num_segments_3 > 0:
        
        # if self.num_segments_4 > 0:

        ### MAKE BRANCH 1
        # initializes number of segments and which ones will have a sensor
        # self.num_segments_1 = random.randint(0,4)
        self.cube_list = np.arange(0, self.num_segments_1)
        for i in range(1,self.num_segments_1):
             flip_coin = random.randint(0, 1)
             self.sensor_loci_1.append(flip_coin)
        
        # makes the snake with no neurons
        i = self.i_start_1
        while i < self.num_segments_1:
            size_dummy = np.zeros(3)
            for x in range(3):
                size_dummy[x] = random.uniform(0,1)            
            # relative to previous joint
            pyrosim.Send_Cube(name= str(i), pos= [0,size_dummy[1]/2,0], size= size_dummy, x= self.sensor_loci_1[i])
            # relative to previous joint
            #if self.num_joints < (self.num_segments-1) & i < self.num_segments:
            if i < (self.num_segments_1 -1):
                pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1), parent = str(i), child = str(i+1), type = "revolute", position = [0,size_dummy[1],0], jointAxis = "1 0 0")   
                self.num_joints_1 += 1 
            i += 1
        
        ### MAKE BRANCH 2
        #self.num_segments_2 = random.randint(0,4) + self.i_start_2
        self.sensor_loci_2.append(self.sensor_loci_1[0])
        for i in range(1,self.num_segments_2):
             flip_coin = random.randint(0, 1)
             self.sensor_loci_2.append(flip_coin)
        
        # makes the snake with no neurons
        i = self.i_start_2
        print('i_2' + str(i))
        self.num_segments_2 = self.num_segments_2 + self.i_start_2
        print('self.num_segments_2' + str(self.num_segments_2))
        while i < self.num_segments_2:
            print('i_2' + str(i))
            size_dummy = np.zeros(3)
            for x in range(3):
                size_dummy[x] = random.uniform(0,1)            
            # relative to previous joint
            pyrosim.Send_Cube(name= str(i), pos= [0,-size_dummy[1]/2,0], size= size_dummy, x= self.sensor_loci_2[i - self.i_start_2])
            # relative to previous joint
            #if self.num_joints < (self.num_segments-1) & i < self.num_segments:
            if i < (self.num_segments_2 -1):
                pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1), parent = str(i), child = str(i+1), type = "revolute", position = [0,-size_dummy[1],0], jointAxis = "1 0 0")   
                self.num_joints_2 += 1 
            i += 1
        
        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        
        for i in range(self.num_segments_1):
            if self.sensor_loci_1[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = "s"+str(i), linkName = str(i))
                self.numSensorNeurons += 1
            if i < (self.num_segments_1-1):
                pyrosim.Send_Motor_Neuron(name = "m"+str(i), jointName = str(i)+'_'+ str(i+1))
                self.numMotorNeurons += self.num_segments_1
        
        for i in range(self.i_start_2,self.num_segments_2):
            if self.sensor_loci_2[i - self.i_start_2] == 1:
                pyrosim.Send_Sensor_Neuron(name = "s"+str(i), linkName = str(i))
                self.numSensorNeurons += 1
            if i < (self.num_segments_1-1):
                pyrosim.Send_Motor_Neuron(name = "m"+str(i), jointName = str(i)+'_'+ str(i+1))
            self.numMotorNeurons += self.num_segments_2- 2
        
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons)
        self.weights = 2*self.weights - 1

        # for currentRow in range(self.numSensorNeurons):
        #     for currentColumn in range(self.numMotorNeurons):
        #         pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+self.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        
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
        #self.weights[randomRow,randomColumn] = 2*random.random() - 1

    def Set_ID(self, newID):
        self.myID = newID