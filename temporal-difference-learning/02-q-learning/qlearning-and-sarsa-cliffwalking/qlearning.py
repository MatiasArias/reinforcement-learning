import winsound
import numpy as np
import math
from app import Environment
from asyncio.windows_events import NULL


class Q_learning(object):
    def __init__(self,epsilon=0.8,phi=0.2,alpha=0.5,total_states=64,total_actions=4,view=NULL):
        # Parametros
        self.egreedy = epsilon #epsilon
        self.discount_rate = phi #phi
        self.step_size = alpha #alpha
        self.total_states = total_states #matriz 4x4
        self.total_actions = total_actions #up,down,right,left
        self.view = view #Pantalla
         
    #Funcion de politica aplicada a Q(s,a) e-greedy
    def e_greedy(self,state,action_values):
        p = np.random.random()
        if p < self.egreedy:
            #Exploro
            next_action = np.random.choice(3)
        else:
            #Exploto
            next_action = np.argmax(action_values[state])
        return next_action

    def algorithm_q_learning(self,totaliterations):
        #Inicializa la accion y el estado
        state = 0
        action = 0
        iterations=0
        steps_per_episode = np.zeros(totaliterations)
        reward_per_episode = np.zeros(totaliterations)
        # Matriz de los valores Q(s,a)
        action_values = np.zeros((self.total_states,self.total_actions))
        optimal=0
        
        while (iterations<totaliterations):
            #Resetea la pantalla
            self.view.reset()
            iterations=iterations+1
            #Inicializar S
            state=0
            
            #Comienza el episodio
            while(state!=self.total_states-1):
                #Seleccionar accion a desde el estado s usando una politica derivada de Q
                action = self.e_greedy(state,action_values)
                #Actualizar pantalla
                self.view.render()
                # Proximo estado, recompensa de ese estado y boolean si logra la recompensa o no
                next_state, reward, done = self.view.step(action)
                #Seleccionar accion a' desde el estado s' usando una politica derivada de Q
                best_action = self.e_greedy(next_state,action_values)
                #Formula principal de Sarsa
                action_values[state][action] = action_values[state][action] + self.step_size*(reward + self.discount_rate*action_values[next_state][best_action]-action_values[state][action])
                #Contador para saber en cuantos pasos realizó y recolectar la recompensa de este episodio
                steps_per_episode[iterations-1] += 1
                reward_per_episode[iterations-1]+= action_values[state][action]
                #Asigna nuevos estados y nuevas acciones
                state=next_state
                #Termina el episodio
                if (done):
                    if(steps_per_episode[iterations-1]<15):
                        winsound.Beep(2000, 100)
                        optimal+=1
                    break
        print(optimal)
        return steps_per_episode, reward_per_episode



