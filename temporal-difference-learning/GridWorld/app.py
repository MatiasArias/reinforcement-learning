import numpy as np
import time
import tkinter as tk

GRID = 40   # pixels
GRID_Y = 8  # grid height
GRID_X = 8  # grid width

class Pantalla(tk.Tk,object):
    def __init__(self):
        super(Pantalla, self).__init__()
        self.action_space = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        self.n_actions = len(self.action_space)
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

        # create oval
        oval_center = origin + GRID * 7
        self.reward = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create red rect
        self.agente = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()

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

        # reward function
        if next_state == self.canvas.coords(self.reward):
            reward = 1
            done = True
            next_state = 'terminal'
        else:
            reward = 0
            done = False

        return next_state, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()

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
        return self.canvas.coords(self.rect)
if __name__ == "__main__":
    env = Pantalla()
    action=2
    env.step(action)
    tk.mainloop()