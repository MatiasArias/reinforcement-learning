from turtle import color
import numpy as np
import random
import matplotlib.pyplot as plt


def results(steps_per_episode,reward_per_episode):
    ax = plt.subplot2grid((2, 3), (0, 0),colspan=3)
    ay = plt.subplot2grid((2, 3), (1, 0),colspan=3)
    x=np.arange(steps_per_episode.size)
    ax.plot(x, steps_per_episode,label="Pasos por episodio")
    ay.plot(x, reward_per_episode,label="Recompensa por episodio",color='orange')
    ax.legend(loc='upper left')
    ay.legend(loc='upper left')

#Funcion de politica aplicada a Q(s,a) e-greedy
def e_greedy(state,action_values):
    p = np.random.random()
    if p < egreedy:
        #Exploro
        j = np.random.choice(4)
    else:
        #Exploto
        j = np.argmax(action_values[state])
    return j

#Funcion que toma la accion de moverse de un estado a otro
def take_action(state,action):
    find_state = np.where(environment_index==state)
    fila=find_state[0][0]
    columna=find_state[1][0]
    if (action == 0):
        #Arriba
        if(fila>0):
            fila=fila-1
    if (action == 1):
        #Derecha
        if(columna<3):
            columna=columna+1   
    if (action == 2):
        #Abajo
        if(fila<3):
            fila=fila+ 1
    if (action == 3):
        #Izquierda
        if(columna>0):
            columna=columna-1

    #Si el agente se va de los limites retornará 16 que generará que salga del ciclo
    if(fila<4 and columna<4 and fila>=0 and columna>=0):
        return environment_index[fila][columna]
#loop
#Inicializa la accion y el estado

def algorithm_qlearning(totaliterations):
    state = 0
    action = 0
    iterations=0
    ## Inicializar matrices
    # Matrices de los valores Q(s,a)
    action_values = np.zeros((total_states,total_actions))
    steps_per_episode = np.zeros(totaliterations)
    reward_per_episode = np.zeros(totaliterations)
    while (iterations<totaliterations):
        iterations=iterations+1
        #Inicializar S
        state=0
        
        #Comienza el episodio
        while(state!=total_states-1):
            #Seleccionar accion a desde el estado s usando una politica derivada de Q
            action = e_greedy(state,action_values)
            # Proximo estado
            next_state = take_action(state,action)
            # Recompensa del proximo estado
            find_state = np.where(environment_index==state+1)
            reward = environment_reward[find_state[0][0]][find_state[1][0]]
            #Formula principal de Sarsa
            best_action = np.argmax(action_values[next_state])
            action_values[state][action] = action_values[state][action] + step_size*(reward + discount_rate*action_values[next_state][best_action]-action_values[state][action])
            steps_per_episode[iterations-1]+=1
            reward_per_episode[iterations-1]+=action_values[state][action]
            #Asigna nuevos estados y nuevas acciones
            state=next_state
    return steps_per_episode,reward_per_episode

# Parametros
egreedy = 0.8 #epsilon
discount_rate = 0.5 #phi
step_size = 0.2 #alpha
total_states = 16 #matriz 4x4
total_actions = 4 #up,down,right,left

#El "ambiente" por donde se va a mover el agente con recompensa en la posicion 3,3
environment_reward = np.zeros((4,4))
environment_reward[3][3] = 1
#Matriz para indicar los indices de los estados en donde se encuentra agente
environment_index = mat = np.arange(16).reshape((4, 4))


steps_per_episode,reward_per_episode = algorithm_qlearning(1000)

results(steps_per_episode,reward_per_episode)
plt.show()
