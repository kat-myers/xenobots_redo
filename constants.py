#Imports
import numpy as np

#Variables
iterations = 1000

maxForce = 100

sleep = 1/120


numSensorNeurons = 4
numMotorNeurons = 8

motorJointRange = 1.0
backLegAmplitude = np.pi/4.0
backLegFrequency = 10
backLegPhaseOffset = 0
frontLegAmplitude = np.pi/4.0
frontLegFrequency = 10
frontLegPhaseOffset = 0


numberOfGenerations = 1
populationSize = 2