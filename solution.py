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
        self.num_segments_1 = 0
        self.num_segments_2 = 0
        self.num_segments_3 = 0
        self.num_segments_4 = 0

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
        self.num_segments_1 = random.randint(0,3)
        self.num_segments_2 = random.randint(0,3)
        self.num_segments_3 = random.randint(0,3)
        print('self.num_segments_1 after init ' + str(self.num_segments_1))
        print('self.num_segments_2 after init ' + str(self.num_segments_2))
        print('self.num_segments_3 after init ' + str(self.num_segments_3))

        ### MAKE THE TORSO
        flip_coin = random.randint(0,1)
        self.sensor_loci_1.append(flip_coin)
        size_dummy = np.zeros(3)
        for x in range(3):
            size_dummy[x] = random.uniform(0,1) * 1.3
        pyrosim.Send_Cube(name= str(0), pos= [0,0,size_dummy[2]*1.5], size= size_dummy, x= self.sensor_loci_1[0])
        
        if self.num_segments_1 > 0:
            print('self.num_segments_1 for torso joint' + str(self.num_segments_1))
            joint_position = [0, size_dummy[1]/2, size_dummy[2]*1.5]
            pyrosim.Send_Joint(name = '0_1' , parent= str(0), child = str(1) , type = "revolute", position = joint_position, jointAxis = "1 0 0", rpy = 0)
            self.num_joints_1 += 1

        if self.num_segments_2 > 0:
            print('self.num_segments_2 for torso joint' + str(self.num_segments_2))
            joint_position = [0, -size_dummy[1]/2, size_dummy[2]*1.5]
            pyrosim.Send_Joint(name = '0_5' , parent= str(0), child = str(self.i_start_2) , type = "revolute", position = joint_position, jointAxis = "1 0 0", rpy = 2)
            self.num_joints_2 += 1
    
        if self.num_segments_3 > 0:
            print('self.num_segments_3 for torso joint' + str(self.num_segments_3))
            joint_position = [0, size_dummy[1]/2, 2*size_dummy[2]]
            pyrosim.Send_Joint(name = '0_10' , parent= str(0), child = str(self.i_start_3) , type = "revolute", position = joint_position, jointAxis = "1 0 0", rpy = 1)
            self.num_joints_3 += 1
        

        ### MAKE BRANCH 1
        # initializes number of segments and which ones will have a sensor
        self.cube_list = np.arange(0, self.num_segments_1)
        for i in range(1,self.num_segments_1):
             flip_coin = random.randint(0, 1)
             self.sensor_loci_1.append(flip_coin)
        
        # makes the snake with no neurons
        i = self.i_start_1
        self.num_segments_1 = self.num_segments_1 + self.i_start_1
        print('self.num_segments_1 for cube generation ' + str(self.num_segments_1))
        while i < self.num_segments_1 :
            print('i_1:' + str(i))
            size_dummy = np.zeros(3)
            for x in range(3):
                size_dummy[x] = random.uniform(0,1) * .9          
            # relative to previous joint
            pyrosim.Send_Cube(name= str(i), pos= [np.random.uniform(-1,1)*size_dummy[0]/2,size_dummy[1]/2,np.random.uniform(-1,1)*size_dummy[2]/2], size= size_dummy, x= self.sensor_loci_1[i - self.i_start_1])
            # relative to previous joint
            #if self.num_joints < (self.num_segments-1) & i < self.num_segments:
            if i < (self.num_segments_1 -1):
                pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1), parent = str(i), child = str(i+1), type = "revolute", position = [0,size_dummy[1],0], jointAxis = "1 0 0", rpy = 1)   
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
        self.num_segments_2 = self.num_segments_2 + self.i_start_2
        print('self.num_segments_2 for cube generation ' + str(self.num_segments_2))
        while i < self.num_segments_2:
            print('i_2:' + str(i))
            size_dummy = np.zeros(3)
            for x in range(3):
                size_dummy[x] = random.uniform(0,1) * .9           
            # relative to previous joint
            pyrosim.Send_Cube(name= str(i), pos= [np.random.uniform(-1,1)*size_dummy[0]/2,-size_dummy[1]/2,np.random.uniform(-1,1)*size_dummy[2]/2], size= size_dummy, x= self.sensor_loci_2[i - self.i_start_2])
            # relative to previous joint
            #if self.num_joints < (self.num_segments-1) & i < self.num_segments:
            if i < (self.num_segments_2 -1):
                pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1), parent = str(i), child = str(i+1), type = "revolute", position = [0,-size_dummy[1],0], jointAxis = "1 0 0", rpy = 1)   
                self.num_joints_2 += 1 
            i += 1
        
        ### MAKE BRANCH 3
        self.sensor_loci_3.append(self.sensor_loci_1[0])
        for i in range(1,self.num_segments_3):
             flip_coin = random.randint(0, 1)
             self.sensor_loci_3.append(flip_coin)
        
        # makes the snake with no neurons
        i = self.i_start_3
        #print('i_3' + str(i))
        self.num_segments_3 = self.num_segments_3 + self.i_start_3
        print('self.num_segments_3 for cube generation ' + str(self.num_segments_3))
        while i < self.num_segments_3:
            print('i_3:' + str(i))
            size_dummy = np.zeros(3)
            for x in range(3):
                size_dummy[x] = random.uniform(0,1) * .9           
            # relative to previous joint
            pyrosim.Send_Cube(name= str(i), pos= [np.random.uniform(-1,1)*size_dummy[0]/2,np.random.uniform(-1,1)*size_dummy[1]/2,size_dummy[2]/2], size= size_dummy, x= self.sensor_loci_3[i - self.i_start_3])
            # relative to previous joint
            #if self.num_joints < (self.num_segments-1) & i < self.num_segments:
            if i < (self.num_segments_3 -1):
                pyrosim.Send_Joint(name = str(i)+'_'+ str(i+1), parent = str(i), child = str(i+1), type = "revolute", position = [0,0,size_dummy[2]], jointAxis = "1 1 0", rpy = 2)   
                self.num_joints_3 += 1 
            i += 1

        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        
        self.sensor_b1 = []
        self.sensor_b2 = []
        self.sensor_b3 = []
        self.sensor_b4 = []
        
        self.motor_b1 = []
        self.motor_b2 = []
        self.motor_b3 = []
        self.motor_b4 = []

        for i in range(self.num_segments_1):
            if self.sensor_loci_1[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = "s"+str(i), linkName = str(i))
                np.append(self.sensor_b1, "s"+str(i))
            if i < (self.num_segments_1-1):
                pyrosim.Send_Motor_Neuron(name = "m"+str(i), jointName = str(i)+'_'+ str(i+1))
                np.append(self.motor_b1, "m"+str(i))
                
        for i in range(self.i_start_2,self.num_segments_2):
            if self.sensor_loci_2[i - self.i_start_2] == 1:
                pyrosim.Send_Sensor_Neuron(name = "s"+str(i), linkName = str(i))
                np.append(self.sensor_b2, "s"+str(i))
            if i < (self.num_segments_2-1):
                pyrosim.Send_Motor_Neuron(name = "m"+str(i), jointName = str(i)+'_'+ str(i+1))
                np.append(self.motor_b2, "m"+str(i))
        
        for i in range(self.i_start_3,self.num_segments_3):
            if self.sensor_loci_3[i - self.i_start_3] == 1:
                pyrosim.Send_Sensor_Neuron(name = "s"+str(i), linkName = str(i))
                np.append(self.sensor_b3, "s"+str(i))
            if i < (self.num_segments_3-1):
                pyrosim.Send_Motor_Neuron(name = "m"+str(i), jointName = str(i)+'_'+ str(i+1))
                np.append(self.motor_b3, "m"+str(i))
        
        self.weights_1 = 2*(np.random.rand(len(self.sensor_b1),len(self.motor_b1))) -1
        self.weights_2 = 2*(np.random.rand(len(self.sensor_b2),len(self.motor_b2))) -1
        self.weights_3 = 2*(np.random.rand(len(self.sensor_b3),len(self.motor_b3))) -1
        self.weights_4 = 2*(np.random.rand(len(self.sensor_b4),len(self.motor_b4))) -1

        ### loops for creating synapses
        for i in range(len(self.sensor_b1)):
             for j in range(len(self.motor_b1)):
                pyrosim.Send_Synapse(sourceNeuronName = i, targetNeuronName = j+len(self.sensor_b1), weight = self.weights_1[i][j])
        
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