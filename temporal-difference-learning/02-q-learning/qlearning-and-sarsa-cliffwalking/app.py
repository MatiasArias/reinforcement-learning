import math
from operator import truediv
from sre_parse import State
from xml.etree.ElementTree import QName
import numpy as np
import time
import tkinter as tk
import winsound


GRID = 40   # pixels
GRID_X = 12  # grid height
GRID_Y = 4  # grid width

class Environment(tk.Tk,object):
    def __init__(self,title):
        super(Environment, self).__init__()
        self.title(title)
        self.geometry('{0}x{1}'.format(GRID_X * GRID, GRID_Y * GRID))
        self.build_app()
        

    def build_app(self):
        #Pantalla blanca
        self.canvas = tk.Canvas(self,bg='white',height=GRID_Y * GRID,width=GRID_X * GRID)
        #Casilleros/Grids
        for c in range(0, GRID_X * GRID, GRID):
            x0, y0, x1, y1 = c, 0, c, GRID_X * GRID
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, GRID_Y * GRID, GRID):
            x0, y0, x1, y1 = 0, r, GRID_X * GRID, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([ 20,  20])

        # Creacion de la recomepensa
        oval_center = origin + GRID*3
        oval_center[0] += 8*GRID
        self.reward = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')
        coords_cliff = np.zeros((10,4))
        coords = origin
        coords[1] += 3*GRID
        coords[0] += GRID
        count=0
        for i in coords_cliff:
                self.cliff = self.canvas.create_rectangle(coords[0]-20,coords[1]-20,coords[0]+20,coords[1]+20,fill='black')
                coords_cliff[count]=self.canvas.coords(self.cliff)
                coords_cliff[count]= coords_cliff[count] - [-5,-5,5,5]
                count+=1
                coords[0] += GRID 
        self.coords_cliff = coords_cliff
        # creacion del agente
        agente_spawn = np.array([ 20,  20])
        agente_spawn[1] += GRID*3
        self.agente = self.canvas.create_rectangle(
        agente_spawn[0] - 15, agente_spawn[1] - 15,
        agente_spawn[0] + 15, agente_spawn[1] + 15,
        fill='red')
        # Empaquetar todo
        self.canvas.pack()

    def equalsCoords(self,coords,arrayCoords):
        for i in arrayCoords:
            if all(coords == i):
                return True
        return False

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
            reward = 10
            done = True
            #winsound.Beep(2000, 100)
            next_state = 'terminal'     
        elif self.equalsCoords(next_state,self.coords_cliff):
            reward = -100
            done = True   
        else:
            reward = -1
            done = False
        return next_state_index, reward, done

    #Pasa las coordenadas a un indice que logra interprestar SARSA.class
    def coordsToIndex(self,state):
        environment_index =  np.arange(GRID_X*GRID_Y).reshape((GRID_Y, GRID_X))
        state_index = environment_index[math.floor(state[1]/40)][math.floor(state[0]/40)]
        return state_index

    #Velocidad con cual se mueve el agente
    def render(self):
        #time.sleep(0.00001)
        self.update()

    #Reseta el agente a la posicion inicial
    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.agente)
        agente_spawn = np.array([ 20,  20])
        agente_spawn[1] += GRID*3
        self.agente = self.canvas.create_rectangle(
        agente_spawn[0] - 15, agente_spawn[1] - 15,
        agente_spawn[0] + 15, agente_spawn[1] + 15,
        fill='red')
        # return observation
        return self.canvas.coords(self.agente)

if __name__ == "__main__":
    env = Environment()
    tk.mainloop()