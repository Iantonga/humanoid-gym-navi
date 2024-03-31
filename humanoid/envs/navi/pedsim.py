#!/usr/bin/env python
import random
import math
import numpy as np
import rvo2


#from groups import extract_membership

class PedestrianSimulator(object):

      # Class containing the simulator for pedestrians
     
    def __init__(self):
        self.sim = rvo2.PyRVOSimulator(1/60., 1.5, 7, 1.5, 2, 0.3, 1.2)
        self.rollout = []
        self.timestep = 0
        self.replay = []
        random.seed(42069)
      
    def create_scenario(self, scenario=1):
        # Scenarios:
        # 691: Corridor, opposite ped traffic


        if scenario == 691:
            a0 = self.sim.addAgent((0, 0))
            self.sim.setAgentPrefVelocity(a0,(1,0))
            reg = 12
            fast = 10
            for i in range(reg):
                self.sim.addAgent((random.uniform(0,8),random.uniform(-1,1)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.3,0.42),0))
            for i in range(reg):
                self.sim.addAgent((random.uniform(-8,0),random.uniform(-1,1)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.3,0.42),0))
            for i in range(fast):
                self.sim.addAgent((random.uniform(-8,8),random.uniform(-1,1)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.4,0.6),0))

            for i in range(reg):
                self.sim.addAgent((random.uniform(0,8),random.uniform(-1,-2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.3,-0.42),0))
            for i in range(reg):
                self.sim.addAgent((random.uniform(-8,0),random.uniform(-1,-2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.3,-0.42),0))
            for i in range(fast):
                self.sim.addAgent((random.uniform(-8,8),random.uniform(-1,-2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.4,-0.6),0))
            
            
            o1 = self.sim.addObstacle([(-10,3),(10,3)])
            o2 = self.sim.addObstacle([(-10,-3), (10,-3)])
            self.sim.processObstacles()
            
        


        if scenario == 690:
            a0 = self.sim.addAgent((0, 0))
            self.sim.setAgentPrefVelocity(a0,(1,0))

            g0 = self.sim.addAgent((5, 1))
            g1 = self.sim.addAgent((4.5, 0))
            g2 = self.sim.addAgent((4, 0.5))
            self.sim.setAgentPrefVelocity(g0,(0.4,0))
            self.sim.setAgentPrefVelocity(g1,(0.4,0))
            self.sim.setAgentPrefVelocity(g2,(0.4,0))

            self.sim.setAgentNeighborDist(a0, 10)
            self.sim.setAgentMaxNeighbors(a0, 10)
            self.sim.setAgentRadius(a0,0.5)
            self.sim.setAgentTimeHorizon(a0,10)

            o1 = self.sim.addObstacle([(-10,3),(10,3)])
            o2 = self.sim.addObstacle([(-10,-3), (10,-3)])
            self.sim.processObstacles()

        if scenario == 69:
            a0 = self.sim.addAgent((0, 0))
            self.sim.setAgentPrefVelocity(a0,(1,0))

            g0 = self.sim.addAgent((3, 1))
            g1 = self.sim.addAgent((4, 0))
            g2 = self.sim.addAgent((3.5, -1))
            self.sim.setAgentPrefVelocity(g0,(-1,0.1))
            self.sim.setAgentPrefVelocity(g1,(-1,0.1))
            self.sim.setAgentPrefVelocity(g2,(-1,0.1))




        if scenario == 100:
            a0 = self.sim.addAgent((0, 0))
            a1 = self.sim.addAgent((1, 0))
            #a2 = self.sim.addAgent((1, 1))
            #a3 = self.sim.addAgent((0, 1), 1.5, 5, 1.5, 2, 0.4, 2, (0, 0))

            # Obstacles are also supported.
            #o1 = self.sim.addObstacle([(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1)])
            #self.sim.processObstacles()

            self.sim.setAgentPrefVelocity(a0, (1, 0))
            self.sim.setAgentPrefVelocity(a1, (-1, 0))
            #self.sim.setAgentPrefVelocity(a2, (-1, -1))
            #self.sim.setAgentPrefVelocity(a3, (1, -1))

        if scenario == 0:
            a0 = self.sim.addAgent((0,-1))
            self.sim.setAgentPrefVelocity(a0, (0.1,5))
            self.sim.setAgentNeighborDist(a0, 10)
            self.sim.setAgentMaxNeighbors(a0, 10)
            self.sim.setAgentRadius(a0,0.2)
            self.sim.setAgentTimeHorizon(a0,1.5)
            o1 = self.sim.addObstacle([(-1, 1), (1, 1), (1, 2),(-1,2)])
            self.sim.processObstacles()

            self.sim.setAgentTimeHorizonObst(0, 10) 	

        if scenario == 1:
            a0 = self.sim.addAgent((0,0))
            self.sim.setAgentPrefVelocity(a0, (1,0))
            self.sim.setAgentNeighborDist(a0, 10)
            self.sim.setAgentMaxNeighbors(a0, 10)
            self.sim.setAgentRadius(a0,0.2)
            self.sim.setAgentTimeHorizon(a0,10)
            self.add_group([((3,-3),3),((3,3),2)])

        if scenario == 3:
          a0 = self.sim.addAgent((0,0))
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
                velocity = random.uniform(0,0.3)
                #y = math.sqrt(abs( velocity**2 - x**2)) * direction[random.randint(0,1)]
                self.sim.addAgent((random.randint(5,15), random.randint(-9,6)))
                x = random.uniform(0,0.5) * (-np.sign(self.sim.getAgentPosition(a+1)[0]))
                y = math.sqrt(abs( velocity**2 - x**2)) * (-np.sign(self.sim.getAgentPosition(a+1)[1]))

                #sim.setAgentPrefVelocity(a+1, (x,y))
                self.sim.setAgentPrefVelocity(a+1, (x,y))
                #self.sim.setAgentPrefVelocity(a+1, (0,0))
                self.sim.setAgentRadius(a+1,0.3)
                #sim.setAgentTimeHorizon(a+1,5)
        
          self.sim.setAgentPrefVelocity(a0, (1,0))
          self.sim.setAgentNeighborDist(a0, 10)
          self.sim.setAgentMaxNeighbors(a0, 10)
          self.sim.setAgentRadius(a0,0.2)
          self.sim.setAgentTimeHorizon(a0,10)

    def getNumAgents(self):
        return self.sim.getNumAgents()
    
    def getAgentPosition(self,a):
        return self.sim.getAgentPosition(a)
    
    def getAgentVelocity(self,a):
        return self.sim.getAgentVelocity(a)
    
    def getAgentPrefVelocity(self,a):
        return self.sim.getAgentPrefVelocity(a)

    def add_group(self,grouplist,tightness=None):
        velocity = random.uniform(0.5,0.8)
        aidx = 1
        for group in grouplist:
            center, num = group[0], group[1]
            for a in range(num):
                self.sim.addAgent((center[0]+random.uniform(-0.5,0.5),center[1]+random.uniform(-0.5,0.5)))
                if a == 0:
                    x = random.uniform(0,0.8) * (-np.sign(self.sim.getAgentPosition(a+1)[0]))
                    y = math.sqrt(abs(velocity**2 - x**2)) * (-np.sign(self.sim.getAgentPosition(a+1)[1]))

                  #sim.setAgentPrefVelocity(a+1, (x,y))
                self.sim.setAgentPrefVelocity(aidx, (x,y))
                self.sim.setAgentRadius(aidx,0.3)
                aidx += 1
    
    def step(self, replay=False):
        if not replay:
            self.sim.doStep()
            positions = []
            velocities = []
            for agent in range(self.sim.getNumAgents()):
                positions.append(self.sim.getAgentPosition(agent))
                velocities.append(self.sim.getAgentVelocity(agent))
            self.rollout.append(positions)
            #print(self.sim.getAgentVelocity(0))

        else:
            out = self.replay[self.timestep]
            self.timestep += 1
        return positions, velocities

    def set_nav_agent_pos(self,agent,pos):
        pos =(float(pos[0][0]), float(pos[0][1]))
        self.sim.setAgentPosition(agent,pos)



        #print(sim.getAgentPosition(0))
        #positions = ['(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
        #for agent_no in (a0, a1, a2, a3)]:
        #    print('step=%2i  t=%.3f  %s' % (step, sim.getGlobalTime(), '  '.join(positions)))
    



#print('Simulation has %i agents and %i obstacle vertices in it.' %
 #     (sim.getNumAgents(), sim.getNumObstacleVertices()))

#print('Running simulation')


    # Pass either just the position (the other parameters then use
# the default values passed to the PyRVOSimulator constructor),
# or pass all available parameters.
# Obstacles are also supported.
#     o1 = sim.addObstacle([(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1)])
#      sim.processObstacles()
      # if scenario == 0:
      #       a0 = sim.addAgent((0,0))
      #       a1 = sim.addAgent((2, 2))
      #       a2 = sim.addAgent((2.5, 2.5))
      #       a3 = sim.addAgent((3, -3))
      #       a4 = sim.addAgent((3.5, -3.5))
      #       a5 = sim.addAgent((4.5, 7.5))
      #       a6 = sim.addAgent((5, 8))
      #       sim.setAgentPrefVelocity(a1, (0, -1))
      #       sim.setAgentPrefVelocity(a2, (0, -1))
      #       sim.setAgentPrefVelocity(a3, (0, 1))
      #       sim.setAgentPrefVelocity(a4, (0, 1))
      #       sim.setAgentPrefVelocity(a5, (0, -1))
      #       sim.setAgentPrefVelocity(a6, (0, -1))

      #       sim.setAgentPrefVelocity(a0, (1,0))
      #       sim.setAgentNeighborDist(a0, 5)
      #       sim.setAgentRadius(a0,0.25)
      #       sim.setAgentTimeHorizon(a0,3.5)

      # if scenario == 1:
      #       a0 = sim.addAgent((0,0))
      #       a1 = sim.addAgent((6, 0))
      #       #a2 = sim.addAgent((6.5, 0.3))
      #       sim.setAgentPrefVelocity(a1, (-1, 0))
      #       sim.setAgentMaxNeighbors(a1,0)
      #       #sim.setAgentPrefVelocity(a2, (-1, 0))
            
      #       sim.setAgentPrefVelocity(a0, (1,0))
      #       sim.setAgentNeighborDist(a0, 10)
      #       sim.setAgentRadius(a0,0.3)
      #       sim.setAgentTimeHorizon(a0,10)

      # if scenario == 2:
      #       a0 = sim.addAgent((0,0))
      #       a1 = sim.addAgent((2, 0))
      #       #a2 = sim.addAgent((6.5, 0.3))
      #       sim.setAgentPrefVelocity(a1, (0.5, 0))
      #       sim.setAgentMaxNeighbors(a1,0)
      #       #sim.setAgentPrefVelocity(a2, (-1, 0))
            
      #       sim.setAgentPrefVelocity(a0, (1,0))
      #       sim.setAgentNeighborDist(a0, 10)
      #       sim.setAgentRadius(a0,0.3)
      #       sim.setAgentTimeHorizon(a0,10)

      # if scenario == 3:
      #       a0 = sim.addAgent((0,0))
      #       direction = [1,-1]
      #       for a in range (19):
      #            # if sim.getAgentPosition(a+1)[0] >= 0:
      #                #   x = random.uniform(-1,-0.5)
      #             #else:
      #               #    x = random.uniform(0.5,1)
      #             #if sim.getAgentPosition(a+1)[1] >= 0:
      #              #     y = random.uniform(-1.1, -0.6)
      #             #else:
      #             #      y = random.uniform(0.6,1.1)
      #             velocity = random.uniform(0.5,0.8)
      #             #y = math.sqrt(abs( velocity**2 - x**2)) * direction[random.randint(0,1)]
      #             sim.addAgent((random.randint(5,15), random.randint(-9,6)))
      #             x = random.uniform(0,0.8) * (-np.sign(sim.getAgentPosition(a+1)[0]))
      #             y = math.sqrt(abs( velocity**2 - x**2)) * (-np.sign(sim.getAgentPosition(a+1)[1]))

      #             #sim.setAgentPrefVelocity(a+1, (x,y))
      #             sim.setAgentPrefVelocity(a+1, (x,y))
      #             sim.setAgentRadius(a+1,0.3)
      #             #sim.setAgentTimeHorizon(a+1,5)
            
      #       sim.setAgentPrefVelocity(a0, (1,0))
      #       sim.setAgentNeighborDist(a0, 10)
      #       sim.setAgentMaxNeighbors(a0, 10)
      #       sim.setAgentRadius(a0,0.2)
      #       sim.setAgentTimeHorizon(a0,10)

