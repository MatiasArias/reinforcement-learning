import math
from operator import truediv
from xml.etree.ElementTree import QName
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
        origin = np.array([ 20,  20])

        # Creacion de la recomepensa
        oval_center = origin + GRID * 7
        self.reward = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')
        coords_deep_puddle = np.zeros((3,4))
        
        puddle_center = origin + GRID * 4
        puddle_center[0] =puddle_center[0] + 2*GRID
        self.deep_puddle = self.canvas.create_rectangle(
            puddle_center[0] - 20, puddle_center[1] -  20,
            puddle_center[0] + 20, puddle_center[1] +  20,
            fill='black')
        coords_deep_puddle[0] = self.canvas.coords(self.deep_puddle)
        coords_deep_puddle[0] = coords_deep_puddle[0] - [-5,-5,5,5]
        puddle_center[0] =puddle_center[0] - GRID
        self.deep_puddle = self.canvas.create_rectangle(
            puddle_center[0] - 20, puddle_center[1] - 20,
            puddle_center[0] + 20, puddle_center[1] + 20,
            fill='black')
        coords_deep_puddle[1] = self.canvas.coords(self.deep_puddle)
        coords_deep_puddle[1] = coords_deep_puddle[1] - [-5,-5,5,5]
        puddle_center[0] =puddle_center[0] + GRID
        puddle_center[1] =puddle_center[1] - GRID
        self.deep_puddle = self.canvas.create_rectangle(
            puddle_center[0] - 20, puddle_center[1] - 20,
            puddle_center[0] + 20, puddle_center[1] + 20,
            fill='black')
        coords_deep_puddle[2] = self.canvas.coords(self.deep_puddle)
        coords_deep_puddle[2] = coords_deep_puddle[2] - [-5,-5,5,5]
        coords_puddle = np.zeros((coords_deep_puddle.size*4,4))
        count=0
        for i in coords_deep_puddle:
            coords = np.array(i)
            for j in range(4):
                coords = np.array(i)
                if j==0:
                    coords[0] = coords[0]-GRID
                    coords[2] = coords[2]-GRID
                if j==1:
                    coords[1] = coords[1]+GRID
                    coords[3] = coords[3]+GRID
                if j==2:
                    coords[0] = coords[0]+GRID
                    coords[2] = coords[2]+GRID
                if j==3:
                    coords[1] = coords[1]-GRID
                    coords[3] = coords[3]-GRID
                if not (self.equalsCoords(coords,coords_deep_puddle)):
                    coords = coords+[-5,-5,5,5]
                    self.puddle = self.canvas.create_rectangle(coords[0],coords[1],coords[2],coords[3],fill='gray')
                    coords_puddle[count]=self.canvas.coords(self.puddle)
                    coords_puddle[count]= coords_puddle[count] - [-5,-5,5,5]
                    count+=1
                coords = np.array(i)
        self.coords_deep_puddle = coords_deep_puddle
        self.coords_puddle = coords_puddle[0:count]

        # creacion del agente
        self.agente = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
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
            reward = 1
            done = True
            next_state = 'terminal'
        elif self.equalsCoords(next_state,self.coords_puddle):
            reward = -2
            done = False     
        elif self.equalsCoords(next_state,self.coords_deep_puddle):
            reward = -3
            done = False   
        else:
            reward = 0.2
            done = False
        if next_state == self.canvas.coords(self.deep_puddle):
            print("Toca")
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
        origin = np.array([ 20,  20])
        self.agente = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.agente)
if __name__ == "__main__":
    env = Environment()
    tk.mainloop()