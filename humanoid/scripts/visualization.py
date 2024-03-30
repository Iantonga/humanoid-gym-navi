import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_agents(posx,posy,save):
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
        
    ani = animation.FuncAnimation(fig=fig, func=animation_update,frames=50*20,interval=20)
    if save:
        writer = animation.PillowWriter(fps=50,
                                 metadata=dict(artist='Me'),
                                 bitrate=1800)
        print("Saving pedsim gif...")
        ani.save('pedsim.gif', writer=writer)
        print("Complete")
    else:
        plt.show()

def animate_rollout(rollout):
    frames = len(rollout)
    num_agents = len(rollout[0])
    posx = [ [] for i in range(num_agents)]
    posy = [ [] for i in range(num_agents)]
    for f in range(frames):
        for i,agentpos in enumerate(rollout[f]):
            posx[i].append(agentpos[0])
            posy[i].append(agentpos[1])
    animate_agents(posx,posy,False)
