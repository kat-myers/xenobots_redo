import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.motorValues = np.zeros(c.iterations)

    def Set_Value(self, robot, t):
        # print ('joint', self.jointName)

        if self.jointName == "Torso_BackLeg":
            self.motorValues[t] = pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotID, jointName = self.jointName,
            controlMod = p.POSITION_CONTROL, targetPosition = robot.targetAngles2[t], maxForce = c.force)

        else:
            self.motorValues[t] = pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotId, jointName = self.jointName,
            controlMode = p.POSITION_CONTROL, targetPosition = robot.targetAngles[t], maxForce = c.force)
    
    def Save_Values(self):
        np.save('data/motorValues.npy', self.motorValues)