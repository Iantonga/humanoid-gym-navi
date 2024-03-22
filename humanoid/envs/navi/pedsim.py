#!/usr/bin/env python
import random
import math
import numpy as np
import rvo2
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from sklearn.cluster import DBSCAN

def create_nav_sim(scenario=3):
      sim = rvo2.PyRVOSimulator(1/50., 1.5, 7, 1.5, 2, 0.2, 2)

# Pass either just the position (the other parameters then use
# the default values passed to the PyRVOSimulator constructor),
# or pass all available parameters.
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


      if scenario == 4:
           a0 = sim.addAgent((0,0))
           sim.setAgentPrefVelocity(a0, (1,0))
           sim.setAgentNeighborDist(a0, 10)
           sim.setAgentMaxNeighbors(a0, 10)
           sim.setAgentRadius(a0,0.2)
           sim.setAgentTimeHorizon(a0,10)

      return sim

def add_group(sim,grouplist,tightness=None):
     velocity = random.uniform(0.5,0.8)
     aidx = 1
     for group in grouplist:
         center, num = group[0], group[1]
         for a in range(num):
              sim.addAgent((center[0]+random.uniform(-0.5,0.5),center[1]+random.uniform(-0.5,0.5)))
              if a == 0:
                  x = random.uniform(0,0.8) * (-np.sign(sim.getAgentPosition(a+1)[0]))
                  y = math.sqrt(abs(velocity**2 - x**2)) * (-np.sign(sim.getAgentPosition(a+1)[1]))

                  #sim.setAgentPrefVelocity(a+1, (x,y))
              sim.setAgentPrefVelocity(aidx, (x,y))
              sim.setAgentRadius(aidx,0.3)
              aidx += 1
    


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

def animate_agents(posx,posy):
    assert len(posx) == len(posy), "Coordinate size mismatch"
    num_agents = len(posx)

    fig, ax = plt.subplots()
    e, = ax.plot(posx[0][0],
                 posy[0][0], 'ro')
    p, = ax.plot([posx[i+1][0] for i in range(num_agents-1)],
                 [posy[j+1][0] for j in range(num_agents-1)], 'bo')
    def animation_update(frame):
        p.set_data([posx[i+1][frame] for i in range(num_agents-1)],
                   [posy[j+1][frame] for j in range(num_agents-1)])
        e.set_data(posx[0][frame],
                   posy[0][frame])
               
        return p,
    ani = animation.FuncAnimation(fig=fig, func=animation_update,frames=50*20,interval=20)
    plt.show()

if __name__ == "__main__":
    sim = create_nav_sim(4)
    #add_group(sim, (3,3),3)
    add_group(sim, [((3,-3),3),((3,3),2)])
    num_agents = sim.getNumAgents()
    print(num_agents)
    posx = [ [] for i in range(num_agents)]
    posy = [ [] for i in range(num_agents)]

    for step in range(50*20):
        sim.doStep()
        for agent in range(num_agents):
            posx[agent].append(sim.getAgentPosition(agent)[0])
            posy[agent].append(sim.getAgentPosition(agent)[1])
    
    animate_agents(posx,posy)

        #print(sim.getAgentPosition(0))
        #positions = ['(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
        #for agent_no in (a0, a1, a2, a3)]:
        #    print('step=%2i  t=%.3f  %s' % (step, sim.getGlobalTime(), '  '.join(positions)))

