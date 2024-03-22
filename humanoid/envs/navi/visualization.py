import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from pedsim import PedestrianSimulator as pedsim

def animate_agents(posx,posy):
    assert len(posx) == len(posy), "Coordinate size mismatch"
    num_agents = len(posx)

    fig, ax = plt.subplots()
    ax.set_xlim((-10,10))
    ax.set_ylim((-10,10))
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


def visualize(scenario=1):
    sim = pedsim()
    sim.create_scenario(scenario)
    #add_group(sim, (3,3),3)
    #sim.add_group([((3,-3),3),((3,3),2)])
    num_agents = sim.getNumAgents()
    print(num_agents)
    posx = [ [] for i in range(num_agents)]
    posy = [ [] for i in range(num_agents)]

    for simstep in range(50*20):
        agentpos,_ = sim.step()
        pos_matrix = []
        for i,pos in enumerate(agentpos):
            posx[i].append(pos[0])
            posy[i].append(pos[1])
            pos_matrix.append([pos[0],pos[1]])
        #membership = extract_membership(pos_matrix, 1)
    #print(pos_matrix)
    #extract_membership(pos_matrix)
    animate_agents(posx,posy)


if __name__ == "__main__":
    scenario = 1
    visualize(scenario)