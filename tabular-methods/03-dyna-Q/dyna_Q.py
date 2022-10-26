from ast import For
from stat import S_ENFMT
import numpy as np
import matplotlib.pyplot as plt


def results(step_per_episode,reward_per_episode):
    ax = plt.subplot2grid((2, 3), (0, 0),colspan=3)
    ay = plt.subplot2grid((2, 3), (1, 0),colspan=3)
    x=np.arange(step_per_episode.size)
    ax.plot(x, step_per_episode,label="Pasos por episodio")
    ay.plot(x, reward_per_episode,label="Recompensa por episodio",color='orange')
    ax.legend(loc='upper left')
    ay.legend(loc='upper left')

def e_greedy(state,action_values):
    p = np.random.random()
    if p < egreedy:
        #Exploro
        j = np.random.choice(4)
    else:
        #Exploto
        j = np.argmax(action_values[state])
    return j

def take_action(s,a):
    s_ = s
    if a==0:
        if s>5:
            s_-=GRID
    if a==1:
        if (s+1)%6!=0 and s!=35:
            s_+=1
    if a==2:
        if s<30:
            s_+=GRID
    if a==3:
        if s%6!=0 and s!=0:
            s_-=1
    if s_ == GRID*GRID-1:
        r = 1
        done = True
    else:
        r = 0 
        done = False
    return s_,r,done

def random_previously_observed(Q):
    find = True
    limit=0
    while find:
        limit+=1
        s = np.random.choice(GRID*GRID)
        a = np.random.choice(4)
        if Q[s][a] > 0 or limit>50:
            find = False
            return s,a
def algorithm_dyna(totalepisodes):
    Q = np.zeros((total_states,total_actions))
    model = np.zeros((total_states,total_actions,2))
    episode=0
    steps_per_episode = np.zeros(totalepisodes)
    reward_per_episode = np.zeros(totalepisodes)
    while(episode<totalepisodes):
        s=0
        print("Episodio numero " + str(episode+1))
        done=False
        while not done:
            a=e_greedy(s,Q)
            s_,r,done=take_action(s,a)
            a_ = np.argmax(Q[s_])
            Q[s][a]=Q[s][a]+step_size*(r+discount_rate*Q[s_][a_]-Q[s][a])
            model[s][a][0]=s_
            model[s][a][1]=r
            for i in range(10):
                model_s,model_a= random_previously_observed(Q)
                model_s_ = int(model[model_s][model_a][0])
                model_r = int(model[model_s][model_a][1])
                model_a_ = np.argmax(Q[model_s_])
                Q[model_s][model_a]=Q[model_s][model_a]+step_size*(model_r+discount_rate*Q[model_s_][model_a_]-Q[model_s][model_a])
            steps_per_episode[episode] += 1
            reward_per_episode[episode]+= Q[s][a]
            s=s_
        episode+=1
    return steps_per_episode,reward_per_episode

# Parametros
egreedy = 0.8 #epsilon
discount_rate = 0.5 #phi
step_size = 0.2 #alpha
GRID = 6
total_states = GRID * GRID  #matriz GRIDxGRID
total_actions = 4 #up,down,right,left


steps_per_episode,reward_per_episode = algorithm_dyna(800)

results(steps_per_episode,reward_per_episode)
plt.show()
