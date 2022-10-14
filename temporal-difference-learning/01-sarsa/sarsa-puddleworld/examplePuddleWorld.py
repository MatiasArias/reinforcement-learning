from app import Environment
from sarsa import SARSA
import matplotlib.pyplot as plt
import numpy as np

def results(steps_per_episode,reward_per_episode):
    print("FINISH SARSA")
    print(steps_per_episode)
    ax = plt.subplot2grid((2, 3), (0, 0),colspan=3)
    ay = plt.subplot2grid((2, 3), (1, 0),colspan=3)
    x=np.arange(steps_per_episode.size)
    ax.plot(x, steps_per_episode,label="Pasos por episodio")
    ay.plot(x, reward_per_episode,label="Recompensa por episodio",color='orange')
    ax.legend(loc='upper left')
    ay.legend(loc='upper left')

if __name__ == "__main__":
    screen = Environment()
    brain = SARSA(view=screen) 
    steps_per_episode, reward_per_episode = brain.algorithm_sarsa(1000)
    screen.mainloop()
    results(steps_per_episode, reward_per_episode)
    plt.show()

    
