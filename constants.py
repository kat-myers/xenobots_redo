#Imports
import numpy as np

#Variables
iterations = 1000

maxForce = 100

sleep = 1/120


numSensorNeurons = 4
numMotorNeurons = 4

motorJointRange = 2.0
backLegAmplitude = np.pi/4
backLegFrequency = 10
backLegPhaseOffset = 5
frontLegAmplitude = np.pi/4
frontLegFrequency = 10
frontLegPhaseOffset = 5


numberOfGenerations = 10
populationSize = 2