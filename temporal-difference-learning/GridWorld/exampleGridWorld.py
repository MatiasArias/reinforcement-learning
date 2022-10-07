from app import Environment
from sarsa import SARSA
import matplotlib.pyplot as plt
import numpy as np

def results():
    print("FINISH SARSA")
    print("El agente llego "+str(count_finish)+" veces a la recompensa con esta cantidad de movimientos:")
    print(actions_to_finish)
    fig, ax = plt.subplots()
    x=np.arange(100)
    ax.plot(x, actions_to_finish)
    plt.show()

if __name__ == "__main__":
    screen = Environment()
    brain = SARSA(view=screen)
    count_finish, actions_to_finish = brain.algorithm_sarsa(100)
    screen.mainloop()
    results()

    
