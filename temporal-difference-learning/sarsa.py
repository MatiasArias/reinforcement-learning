from itertools import count
from msilib.schema import Environment
import numpy as np
import random
# Parametros
egreedy = 0.8 #epsilon
discount_rate = 0.5 #phi
step_size = 0.2 #alpha
total_states = 16 #matriz 4x4
total_actions = 4 #up,down,right,left

## Inicializar matrices
# Matrices de los valores Q(s,a)
action_values = np.zeros((total_states,total_actions))
#El "ambiente" por donde se va a mover el agente con recompensa en la posicion 3,3
environment_reward = np.zeros((4,4))
environment_reward[3][3] = 1
#Matriz para indicar los indices de los estados en donde se encuentra agente
environment_index = mat = np.arange(16).reshape((4, 4))
print(environment_index)
print(environment_reward)

#Funcion de politica aplicada a Q(s,a) e-greedy
def e_greedy(state):
    p = np.random.random()
    if p < egreedy:
        #Exploro
        j = np.random.choice(3)
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
        fila=fila-1
    if (action == 1):
        #Derecha
        columna=columna+1
    if (action == 2):
        #Abajo
        fila=fila+ 1
    if (action == 3):
        #Izquierda
        columna=columna-1

    #Si el agente se va de los limites retornará 16 que generará que salga del ciclo
    if(fila<4 and columna<4 and fila>=0 and columna>=0):
        return environment_index[fila][columna]
    else:
        return 16
#loop
#Inicializa la accion y el estado
state = 0
action = 0
iterations=0
count_reward = 0
while (iterations<1000):
    iterations=iterations+1
    #Inicializar S
    state=0
    #Seleccionar accion a desde el estado s usando una politica derivada de Q
    action = e_greedy(state)
    print("Buscando...")
    #Comienza el episodio
    while(state!=total_states-1):
        # Proximo estado
        next_state = take_action(state,action)
        #Evalua si se va de los limites
        if (next_state==16):
            break
        # Recompensa del proximo estado
        find_state = np.where(environment_index==state+1)
        reward = environment_reward[find_state[0][0]][find_state[1][0]]
        #Seleccionar accion a' desde el estado s' usando una politica derivada de Q
        next_action = e_greedy(next_state)
        #Formula principal de Sarsa
        action_values[state][action] = action_values[state][action] + step_size*(reward + discount_rate*action_values[next_state][next_action]-action_values[state][action])
        #Asigna nuevos estados y nuevas acciones
        state=next_state
        action=next_action
        #Cuenta cuantas veces llegó a la salida
        if (state==15):
            count_reward=count_reward+1


print("Terminó la busqueda")
print("El agente encontró "+str(count_reward)+" veces la salida")
print('\n RESULTADOS:')
print(action_values)