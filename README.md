# Welcome to the 3D Random-Generated, Randomly-Evolved Creatures Update!
## How Creatures Are Generated
In the latest update, I create 3D, randomly-generated creatures. Each creature consists of a root link, called a torso, and has the opportunity to 
generate 0 to 4 segments coming from each branching point from the torso. The creatures can have 0 to 4 branching points, which are connected via joints at random
values along the face of the torso. A diagram for how these creatures are generated is shown below:
![A7_Creature_Generation](https://user-images.githubusercontent.com/122335561/220019495-a9e14a35-746b-4593-9f92-f7327993776e.png)
(inspiration for diagram from Karl Sims)

![IMG_0047](https://user-images.githubusercontent.com/122335561/220421421-a27ecf51-5b58-4ecf-8df8-dacae1fefaa6.jpg)

Each branch's segments are random sizes between .2 and 1, and are connected via joints at random points on the previous segment's face. The joints 
have been modified so that they can now be generated diagonally using "roll-pitch-yaw" arguments passed when the joint is defined

Each of these joints has a motor neuron, and each link has a 50% chance of gaining a sensor neuron.
Links without sensors are blue, and links with sensor are green. An example is below:

![snake](https://user-images.githubusercontent.com/122335561/220019630-9309cda5-def3-428e-beac-4a1d2ed5f204.JPG)

The creatures are also generated to minimize intersection with other segments. Adjacent cubes are allowed to intersect, but nonadjancent cubes or cubes from different
branches are stopped from doing so by checking that the next generated cube will not generate into a position where a cube already exists

## The Body
With this current code, the creature's individual links are still limited to rectangular prisms with any dimension randomly varying from .2 to 1. 
Movements are based on revolute joints with varying axes that can operated at angles with the addition of the "roll-pitch-yaw" argument I added in "Send_Joint".

## The Brain
Each creature's joints contain a motor neuron, and each link has a 50% chance of containing a sensor neuron. Within each branch from the torso root link, all motor
and sensor neurons are connected via synapses. Each motor connects to every synapse, which limits isolated behavior. In later updates this will be changed for a more complex brain

## Evolution
The creatures are given an opportunity to evolve. This is done by beginnning a population
with randomly generated creatures, and evaluating the fitness, defined as the ability of the
snakes to move in the y direction:
   stateOfLinkZero = p.getLinkState(self.robotId,0)
        positionOfLinkZero = stateOfLinkZero[1]
        yCoordinateOfLinkZero = positionOfLinkZero[1]
The creatures with the highest fitness are then randomly mutated and allowed to evolve, seeding
the next generation. To evolve the mutants, I assign each cube anumber after the body is generated and store this in a dictionary. At the end of the simulation, I store this dictionary in a temporary txt file. Then, when a child is generated, I mutate the body part corresponding to a randomly generated number. Currently, mutating is just changing the size and not the orientation of the object, but I am hoping to fix this in later simulations. Once I am able to generate more complex synapse structure, I will implement evolving the brains as well. 
This process is repeated for a certain number of generations with a certain population
size in each, defined in my constants.py file. Below is a diagram explaining how the mutation works:
![IMG_0083](https://user-images.githubusercontent.com/122335561/221695268-8e9d337f-8f35-465e-aa10-9c4526a61f41.png)

## How to Run
To run this simulation, clone my directory, fetch branch assignment8, and run "py search.py" in your terminal :)
Enjoy!!
   
This project is part of CHE 396: Artificial Life, taught by Dr. Sam Kriegman at Northwestern University, Winter 2023

