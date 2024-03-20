#!/usr/bin/env python

import humanoid.envs.navi.pedsim as pedsim
import random
import math
import numpy as np
import rvo2

def create_nav_sim(scenario=3):
      sim = rvo2.PyRVOSimulator(1/50., 1.5, 7, 1.5, 2, 0.2, 2)

# Pass either just the position (the other parameters then use
# the default values passed to the PyRVOSimulator constructor),
# or pass all available parameters.
      
#      a3 = sim.addAgent((2, -4.5), 1.5, 5, 1.5, 2, 0.4, 2, (0, 0))

# Obstacles are also supported.
 #     o1 = sim.addObstacle([(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1)])
#      sim.processObstacles()
      if scenario == 0:
            a0 = sim.addAgent((0,0))
            a1 = sim.addAgent((2, 2))
            a2 = sim.addAgent((2.5, 2.5))
            a3 = sim.addAgent((3, -3))
            a4 = sim.addAgent((3.5, -3.5))
            a5 = sim.addAgent((4.5, 7.5))
            a6 = sim.addAgent((5, 8))
            sim.setAgentPrefVelocity(a1, (0, -1))
            sim.setAgentPrefVelocity(a2, (0, -1))
            sim.setAgentPrefVelocity(a3, (0, 1))
            sim.setAgentPrefVelocity(a4, (0, 1))
            sim.setAgentPrefVelocity(a5, (0, -1))
            sim.setAgentPrefVelocity(a6, (0, -1))

            sim.setAgentPrefVelocity(a0, (1,0))
            sim.setAgentNeighborDist(a0, 5)
            sim.setAgentRadius(a0,0.25)
            sim.setAgentTimeHorizon(a0,3.5)

      if scenario == 1:
            a0 = sim.addAgent((0,0))
            a1 = sim.addAgent((6, 0))
            #a2 = sim.addAgent((6.5, 0.3))
            sim.setAgentPrefVelocity(a1, (-1, 0))
            sim.setAgentMaxNeighbors(a1,0)
            #sim.setAgentPrefVelocity(a2, (-1, 0))
            
            sim.setAgentPrefVelocity(a0, (1,0))
            sim.setAgentNeighborDist(a0, 10)
            sim.setAgentRadius(a0,0.3)
            sim.setAgentTimeHorizon(a0,10)

      if scenario == 2:
            a0 = sim.addAgent((0,0))
            a1 = sim.addAgent((2, 0))
            #a2 = sim.addAgent((6.5, 0.3))
            sim.setAgentPrefVelocity(a1, (0.5, 0))
            sim.setAgentMaxNeighbors(a1,0)
            #sim.setAgentPrefVelocity(a2, (-1, 0))
            
            sim.setAgentPrefVelocity(a0, (1,0))
            sim.setAgentNeighborDist(a0, 10)
            sim.setAgentRadius(a0,0.3)
            sim.setAgentTimeHorizon(a0,10)

      if scenario == 3:
            a0 = sim.addAgent((0,0))
            direction = [1,-1]
            for a in range (19):
                 # if sim.getAgentPosition(a+1)[0] >= 0:
                     #   x = random.uniform(-1,-0.5)
                  #else:
                    #    x = random.uniform(0.5,1)
                  #if sim.getAgentPosition(a+1)[1] >= 0:
                   #     y = random.uniform(-1.1, -0.6)
                  #else:
                  #      y = random.uniform(0.6,1.1)
                  velocity = random.uniform(0.5,0.8)
                  #y = math.sqrt(abs( velocity**2 - x**2)) * direction[random.randint(0,1)]
                  sim.addAgent((random.randint(5,15), random.randint(-9,6)))
                  x = random.uniform(0,0.8) * (-np.sign(sim.getAgentPosition(a+1)[0]))
                  y = math.sqrt(abs( velocity**2 - x**2)) * (-np.sign(sim.getAgentPosition(a+1)[1]))

                  #sim.setAgentPrefVelocity(a+1, (x,y))
                  sim.setAgentPrefVelocity(a+1, (x,y))
                  sim.setAgentRadius(a+1,0.3)
                  #sim.setAgentTimeHorizon(a+1,5)
            
            sim.setAgentPrefVelocity(a0, (1,0))
            sim.setAgentNeighborDist(a0, 10)
            sim.setAgentMaxNeighbors(a0, 10)
            sim.setAgentRadius(a0,0.2)
            sim.setAgentTimeHorizon(a0,10)



      return sim

def compute_nav_sim(sim):
     sim.doStep()
     positions = []
     for agent in range(sim.getNumAgents()):
           positions.append(sim.getAgentPosition(agent))
     return positions

def set_nav_agent_pos(sim,agent,pos):
      #print("agentpos", pos)
      pos =(float(pos[0][0]), float(pos[0][1]))
      sim.setAgentPosition(agent,pos)

#print('Simulation has %i agents and %i obstacle vertices in it.' %
 #     (sim.getNumAgents(), sim.getNumObstacleVertices()))

#print('Running simulation')

#for step in range(20):
 #   sim.doStep()
  #  print(sim.getAgentPosition(a0)[0])
   # positions = ['(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
    #             for agent_no in (a0, a1, a2, a3)]
    #print('step=%2i  t=%.3f  %s' % (step, sim.getGlobalTime(), '  '.join(positions)))

