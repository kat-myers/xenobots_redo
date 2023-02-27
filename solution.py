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
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 -1
        self.myID = nextAvailableID
        self.links_with_neurons = 0

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
        
    def Set_ID(self, newID):
        self.myID = newID

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()


    def Create_Body(self):
        # [ movement away from camera (farther away from the origin of the thing), movement left and right, up and down]
                # decide which ones will be sensor neurons now
        j = 0
        #neuron_list = []
        links_with_neurons = []

        for i in range(c.numMotorNeurons):
            if j == c.numSensorNeurons:
                break
            is_sensor = random.choice([True, False])
            if is_sensor == True:
                links_with_neurons.append(i)
                j+=1 
                #neuron_list.append(j)

        self.links_with_neurons = links_with_neurons
        
        
        pyrosim.Start_URDF("body.urdf")


        ### MAKE THE TORSO
        size_dummy = np.zeros(3)
        for x in range(3):
            size_dummy[x] = random.uniform(0,1) * 1.3
        pyrosim.Send_Cube(name= str(0), pos= [0,0,.25], size= [.5,.5,.5], x= 0)
        pyrosim.Send_Cube(name= str(0), pos= [0,0,size_dummy[2]*1.5], size= size_dummy, x= 0)
        
        
        i=1
        while i < c.numMotorNeurons:
            l = random.uniform(0,1)*.9
            w = random.uniform(0,1)*.9
            h = random.uniform(0,1)*.9
            side = random.choice([1,2,3,4])

        # pick a side
            if side == 1:
                posn_cube = [0, -w/2, 0]
                posn_joint = [0,-w,0]
                #curr_absy = [absy[0] + w,]
                
            

            elif side == 2:
                posn_cube = [0, 0, w/2]
                posn_joint = [0,0,w]
                #absz += w

            elif side == 3:
                posn_cube = [0, w/2, 0]
                posn_joint = [0,w,0]
                #absy += w
            
            elif side == 4:
                posn_cube = [0, -w/2, 0]
                posn_joint = [0,-w,0]
                #absz+= -w

            pyrosim.Send_Cube(name = str(i), pos = posn_cube, size = [l,w,h], x = 0)
            pyrosim.Send_Joint(name = str(i) +'_'+ str(i+1), parent = str(i), child = str(i+1), type = 'revolute', position = posn_joint,jointAxis = '1 0 0',rpy = random.randint(0,2))
            i +=1

        # the last block
        l = random.uniform(0,1)
        w = random.uniform(0,1)
        h = random.uniform(0,1)
        pyrosim.Send_Cube(name = str(c.numMotorNeurons), pos = [0,w/2,0], size = [l,w,h], x = 0)

        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        
        def generate_pairs(numbers_list):
            pairs = []
            for i, num1 in enumerate(numbers_list):
                for j, num2 in enumerate(numbers_list[i+1:]):
                    pairs.append((num1, num2))
            return pairs

        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        # make motor neurons
        for i in range(c.numMotorNeurons-1):
            pyrosim.Send_Motor_Neuron(name=i, jointName = str(i) +'_'+ str(i+1))
        
        # randomly place your sensors
        j = c.numMotorNeurons
        neuron_list = []
        links_with_neurons = []

        for i in range(c.numMotorNeurons):
            if j == c.numSensorNeurons:
                break
            is_sensor = random.choice([True, False])
            if is_sensor == True:
                j+=1 
                pyrosim.Send_Sensor_Neuron(name = j, linkName = str(i)) # j is sensor name, linkName is the link it correspond to
                neuron_list.append(j)
                links_with_neurons.append(i)

        pyrosim.End()


    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0,1)
        #self.weights[randomRow,randomColumn] = 2*random.random() - 1

