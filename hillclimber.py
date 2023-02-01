#Imports
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim
import copy
import constants as c
from solution import SOLUTION

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()
           
    def Evolve(self, directOrGUI):
        self.parent.Evaluate("GUI")
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(directOrGUI)
            
    def Evolve_For_One_Generation(self, directOrGUI):
        self.Spawn()

        self.Mutate()

        self.child.Evaluate(directOrGUI)
        
        self.Print()

        self.Select()
                
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
    
    def Mutate(self):
        self.child.Mutate()
        
    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
        
    def Print(self):
        print('\n', 'Parent Fitness:', self.parent.fitness, ' Child Fitness:', self.child.fitness)
        
    def Show_Best(self):
        self.parent.Evaluate("GUI")

        