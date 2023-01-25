import pybullet as p
import numpy
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import matplotlib.pyplot as plt

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
worldId = p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")
pyrosim.Prepare_To_Simulate(robotId)
frontLegSensorValues = numpy.zeros(1000)
backLegSensorValues = numpy.zeros(1000)
#targetAngles = numpy.sin(numpy.linspace(-numpy.pi/4, numpy.pi/4, 1000))
# values for motor angle vectors
bl_amplitude = numpy.pi/4
bl_frequency = 20
bl_phaseOffset = 0

fl_amplitude = numpy.pi/4
fl_frequency = 20
fl_phaseOffset = -10
targetAngles = []

# motor angle vectors
angle_range = numpy.linspace(0, 2*numpy.pi, 1000)
targetAngles_BackLeg = bl_amplitude * numpy.sin(bl_frequency * angle_range + bl_phaseOffset)
targetAngles_FrontLeg = fl_amplitude * numpy.sin(fl_frequency * angle_range + fl_phaseOffset)
for x in range(1000):
    p.stepSimulation()
    frontLegSensorValues[x] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[x] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_BackLeg[x],
        maxForce = 400)
    
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_FrontLeg[x],
        maxForce = 400)
    time.sleep(1/60)
with open('frontsensorvalues.npy', 'wb') as f:
    numpy.save(f, frontLegSensorValues, allow_pickle=True, fix_imports=True)
with open('backsensorvalues.npy', 'wb') as f:
    numpy.save(f, backLegSensorValues, allow_pickle=True, fix_imports=True)
# with open('sinwave.npy', 'wb') as f:
#     numpy.save(f, targetAngles, allow_pickle=True, fix_imports=True)
p.disconnect()