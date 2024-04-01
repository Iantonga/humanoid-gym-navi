#!/usr/bin/env python
import random
import math
import numpy as np
import rvo2


#from groups import extract_membership

class PedestrianSimulator(object):

      # Class containing the simulator for pedestrians
     
    def __init__(self):
        # Sim params:                  timestep, nbdist, maxnb, horizon, horizonobs, radius,maxspeed
        self.sim = rvo2.PyRVOSimulator(1/60.,    1.5,    7,     1.5,     2,          0.3,   1.2)
        self.rollout = []
        self.timestep = 0
        self.replay = []
        self.num_walls = 0
        random.seed(42069)

    def get_num_walls(self):
        return self.num_walls
      
    def create_scenario(self, scenario=1):
        # Scenarios:
        # 691: Corridor-wide, opposite ped traffic
        # 692: Corridor-narrow, oppsite ped traffic

        if scenario == 691:
            a0 = self.sim.addAgent((0, 0))
            self.sim.setAgentPrefVelocity(a0,(1,0))
            reg = 10
            fast = 18
            #interval = 20 / (reg + fast)
            for i in range(reg):
                self.sim.addAgent((random.uniform((20/reg) * i - 11, (20/reg) * i - 9),random.uniform(-2,2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.3,0.6),random.uniform(-0.1,0.1)))
            for i in range(fast):
                self.sim.addAgent((random.uniform((20/fast) * i - 11, (20/fast) * i - 9),random.uniform(-2,2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.4,0.6),random.uniform(-0.1,0.1)))

            for i in range(reg):
                self.sim.addAgent((random.uniform((20/reg) * i - 11, (20/reg) * i - 9),random.uniform(-6, -2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.3,-0.6),random.uniform(-0.1,0.1)))
            for i in range(fast):
                self.sim.addAgent((random.uniform((20/fast) * i - 11, (20/fast) * i - 9),random.uniform(-6,-2)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.4,-0.6),random.uniform(-0.1,0.1)))
            
            
            o1 = self.sim.addObstacle([(-20,3),(20,3)])
            o2 = self.sim.addObstacle([(-20,-7), (20,-7)])
            self.sim.processObstacles()
            
        if scenario == 692:
            self.num_walls = 2
            a0 = self.sim.addAgent((0, 0))
            self.sim.setAgentPrefVelocity(a0,(1,0))
            reg = 10
            fast = 18
            #interval = 20 / (reg + fast)
            for i in range(reg):
                self.sim.addAgent((random.uniform((40/reg) * i - 21, (40/reg) * i - 19),random.uniform(-1,1.5)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.3,0.6),random.uniform(0,0.1)))
            for i in range(fast):
                self.sim.addAgent((random.uniform((40/fast) * i - 21, (40/fast) * i - 19),random.uniform(-1,1)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(0.4,0.6),random.uniform(0,0.1)))

            for i in range(reg):
                self.sim.addAgent((random.uniform((40/reg) * i - 21, (40/reg) * i - 19),random.uniform(-3, -1.5)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.3,-0.6),random.uniform(-0.1,0)))
            for i in range(fast):
                self.sim.addAgent((random.uniform((40/fast) * i - 21, (40/fast) * i - 19),random.uniform(-3,-1.5)))
                self.sim.setAgentPrefVelocity(self.sim.getNumAgents()-1, (random.uniform(-0.4,-0.6),random.uniform(-0.1,0)))
            
            
            o1 = self.sim.addObstacle([(-20,2),(20,2)])
            o2 = self.sim.addObstacle([(-20,-4), (20,-4)])
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

            g0 = self.sim.addAgent((10, 1))
            g1 = self.sim.addAgent((12, 0))
            g2 = self.sim.addAgent((11, -1))
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
          for a in range (15):
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
                self.sim.addAgent((random.randint(2,13), random.randint(-9,6)))
                x = random.uniform(0,0.5) * (-np.sign(self.sim.getAgentPosition(a+1)[0]))
                y = math.sqrt(abs( velocity**2 - x**2)) * (-np.sign(self.sim.getAgentPosition(a+1)[1]))

                #sim.setAgentPrefVelocity(a+1, (x,y))
                self.sim.setAgentPrefVelocity(a+1, (x,y))
                #self.sim.setAgentPrefVelocity(a+1, (0,0))
                self.sim.setAgentRadius(a+1,0.3)
                #sim.setAgentTimeHorizon(a+1,5)
        
          self.sim.setAgentPrefVelocity(a0, (1,0))
          self.sim.setAgentNeighborDist(a0, 15)
          self.sim.setAgentMaxNeighbors(a0, 10)
          self.sim.setAgentRadius(a0,0.3)
          self.sim.setAgentTimeHorizon(a0,15)

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

