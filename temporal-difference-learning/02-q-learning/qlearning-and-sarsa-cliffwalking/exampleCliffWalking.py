from app import Environment
from qlearning import Q_learning
from sarsa import SARSA
import matplotlib.pyplot as plt
import numpy as np

def results(steps_per_episodeS,reward_per_episodeS,steps_per_episodeQ,reward_per_episodeQ):
    print("FINISH Q LEARNING")
    ax = plt.subplot2grid((2, 3), (0, 0),colspan=3)
    ay = plt.subplot2grid((2, 3), (1, 0),colspan=3)
    x=np.arange(steps_per_episodeQ.size)
    ax.plot(x, steps_per_episodeQ,label="Pasos por episodio - Q-Learning")
    ax.plot(x, steps_per_episodeS,label="Pasos por episodio - Sarsa",color='orange')
    ay.plot(x, reward_per_episodeQ,label="Recompensa por episodio - Q-Learning")
    ay.plot(x, reward_per_episodeS,label="Recompensa por episodio - Sarsa",color='orange')
    ax.legend(loc='upper left')
    ay.legend(loc='upper left')



if __name__ == "__main__":
    screen_QLEARNING = Environment("Q-LEARNING AND SARSA")
    brain_qlearning = Q_learning(epsilon=0.1,view=screen_QLEARNING)
    brain_sarsa =SARSA(epsilon=0.1,view=screen_QLEARNING)
    steps_per_episodeQ, reward_per_episodeQ = brain_qlearning.algorithm_q_learning(1000)
    steps_per_episodeS, reward_per_episodeS = brain_sarsa.algorithm_sarsa(1000)
    results(steps_per_episodeQ, reward_per_episodeQ,steps_per_episodeS, reward_per_episodeS)
    plt.show()

    
