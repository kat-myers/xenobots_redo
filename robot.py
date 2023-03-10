#Imports
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
class ROBOT:        
    def __init__(self):        
        self.robotId = p.loadURDF("body.urdf")        
        pyrosim.Prepare_To_Simulate(self.robotId)               
        self.Prepare_To_Sense()       
        self.nn = NEURAL_NETWORK("brain.nndf")        
        self.Prepare_To_Act()                
    #Sensing    
    def Prepare_To_Sense(self):        
        self.sensors = {}        
        for linkName in pyrosim.linkNamesToIndices:            
            self.sensors[linkName] = SENSOR(linkName = linkName)            
    def Sense(self, i):        
        for j,s in enumerate(self.sensors):            
            SENSOR.Get_Value(self.sensors[s], i)        
    #Thinking    
    def Think (self):        
        self.nn.Update()        
        self.nn.Print()            
    #Acting    
    def Prepare_To_Act(self):        
        self.motors = {}        
        for jointName in pyrosim.jointNamesToIndices:            
            self.motors[jointName] = MOTOR(jointName = jointName)            
    def Act(self, i):        
        for neuronName in self.nn.Get_Neuron_Names():            
            if self.nn.Is_Motor_Neuron(neuronName):                
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)                
                desiredAngle = self.nn.Get_Value_Of(neuronName)    
                MOTOR.Set_Value(self.motors[jointName], self, desiredAngle)      
                #print(jointName, neuronName, desiredAngle)               