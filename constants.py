import pybullet as p
import numpy
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random

bl_amplitude = numpy.pi/4
bl_frequency = 100
bl_phaseOffset = 0

fl_amplitude = numpy.pi/4
fl_frequency = 100
fl_phaseOffset = -10

iterations = 1000
sleep_time = 1/60

maxForce = 100