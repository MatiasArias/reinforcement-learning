import math
import numpy as np
import time
import tkinter as tk

GRID = 40   # pixels
GRID_Y = 8  # grid height
GRID_X = 8  # grid width

class Environment(tk.Tk,object):
    def __init__(self):
        super(Environment, self).__init__()
        self.title('S.A.R.S.A')
        self.geometry('{0}x{1}'.format(GRID_X * GRID, GRID_Y * GRID))
        self.build_app()
        

    def build_app(self):
        #Pantalla blanca
        self.canvas = tk.Canvas(self,bg='white',height=GRID_X * GRID,width=GRID_Y * GRID)
        #Casilleros/Grids
        for c in range(0, GRID_X * GRID, GRID):
            x0, y0, x1, y1 = c, 0, c, GRID_Y * GRID
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, GRID_Y * GRID, GRID):
            x0, y0, x1, y1 = 0, r, GRID_X * GRID, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # Creacion de la recomepensa
        oval_center = origin + GRID * 7
        self.reward = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # creacion del agente
        self.agente = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # Empaquetar todo
        self.canvas.pack()

    #Es el anterior take_action, es el paso del agente
    def step(self,action):
        state = self.canvas.coords(self.agente)
        base_action=np.array([0,0])
        if (action == 0):
            #Arriba
            if state[1] > GRID:
                base_action[1] -= GRID
        if (action == 1):
            #Derecha
            if state[0] < (GRID_X - 1) * GRID:
                base_action[0] += GRID
        if (action == 2):
            #Abajo
            if state[1] < (GRID_Y - 1) * GRID:
                base_action[1] += GRID
        if (action == 3):
            #Izquierda
            if state[0] > GRID:
                base_action[0] -= GRID
        self.canvas.move(self.agente, base_action[0], base_action[1])
        
        next_state = self.canvas.coords(self.agente)  # next state
        next_state_index = self.coordsToIndex(next_state)
        # reward function
        if next_state == self.canvas.coords(self.reward):
            reward = 1
            done = True
            next_state = 'terminal'
        else:
            reward = 0
            done = False
        
        return next_state_index, reward, done

    #Pasa las coordenadas a un indice que logra interprestar SARSA.class
    def coordsToIndex(self,state):
        environment_index = mat = np.arange(GRID_X*GRID_Y).reshape((GRID_X, GRID_Y))
        state_index = environment_index[math.floor(state[1]/40)][math.floor(state[0]/40)]
        return state_index

    #Velocidad con cual se mueve el agente
    def render(self):
        time.sleep(0.00001)
        self.update()

    #Reseta el agente a la posicion inicial
    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.agente)
        origin = np.array([20, 20])
        self.agente = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.agente)
if __name__ == "__main__":
    env = Pantalla()
    action=2
    env.step(action)
    tk.mainloop()