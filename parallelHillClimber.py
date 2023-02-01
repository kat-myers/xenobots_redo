#Imports
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim
import copy
import constants as c
from solution import SOLUTION
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        
        self.nextAvailableID = 0
        self.parents = {}
        
        for i in range(0, c.populationSize):
            result = SOLUTION(self.nextAvailableID)
            self.parents[i] = result
            self.nextAvailableID += 1
           
    def Evolve(self, directOrGUI):        
        self.Evaluate(self.parents, directOrGUI)
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(directOrGUI)
            
    def Evolve_For_One_Generation(self, directOrGUI):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children, directOrGUI)
                
        self.Print()

        self.Select()
                       
    def Spawn(self):
        self.children = {}
        
        for parent in self.parents.keys():
            child = copy.deepcopy(self.parents[parent])
            child.Set_ID(self.nextAvailableID)
            self.children[parent] = child
            self.nextAvailableID += 1
    
    def Mutate(self):
        for child in self.children.keys():
            self.children[child].Mutate()
        
    def Select(self):
        for key in self.parents.keys():
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]
        
    def Print(self):
        for key in self.parents.keys():
            print()
            print('Parent Fitness:', self.parents[key].fitness, ' Child Fitness:', self.children[key].fitness)

    def Show_Best(self):
        bestKey = 0
        
        for parent in self.parents.keys():
            if self.parents[parent].fitness < self.parents[bestKey].fitness:
                bestKey = parent
                
        self.parents[bestKey].Start_Simulation("GUI")
    
    def Evaluate(self, solutions, directOrGUI):        
        for solution in solutions.keys():
            solutions[solution].Start_Simulation(directOrGUI)
            
        for solution in solutions.keys():
            solutions[solution].Wait_For_Simulation_To_End(directOrGUI)

        