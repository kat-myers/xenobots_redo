import pybullet as p
import numpy
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
worldId = p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")
pyrosim.Prepare_To_Simulate(robotId)
frontLegSensorValues = numpy.zeros(1000)
backLegSensorValues = numpy.zeros(1000)

for x in range(1000):
    p.stepSimulation()
    frontLegSensorValues[x] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[x] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    time.sleep(1/60)
with open('frontsensorvalues.npy', 'wb') as f:
    numpy.save(f, frontLegSensorValues, allow_pickle=True, fix_imports=True)
with open('backsensorvalues.npy', 'wb') as f:
    numpy.save(f, backLegSensorValues, allow_pickle=True, fix_imports=True)
p.disconnect()