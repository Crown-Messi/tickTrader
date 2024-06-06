import numpy as np
import pandas as pd
import time

np.random.seed(2)#随机种子

N_STATES = 6 #状态个数
ACTIONS = ['left','right']#可选择的动作
EPSLION = 0.9 #greedy  随机选择的几率，增加不确定性，利于发现更好的路
ALPHA = 0.1 #学习率
LAMBDA = 0.9 #对于奖励的衰减率
MAX_EPISODES = 20 #学习的回合数
FRESH_TIME = 0.01#每步的刷新时间

def build_q_table(n_states, actions):#创建q表，初始全零，空白小本本
    table = pd.DataFrame(
        np.zeros((n_states,len(actions))),
        columns= actions
    )
    print(table)
    return table


def choose_action(state,q_table):#每一步选择怎么走（动作）
    state_actions = q_table.iloc[state,:]
    if (np.random.uniform()>EPSLION) or (state_actions.all() == 0): #如果是随机选择或者是最初始的状态
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax()#选择最大的
    return action_name



def get_env_feedback(S,A):#环境的反馈
    if A=='right':
        if S==N_STATES-1:#最终状态
            S_ = 'terminal'
            R = 1
        else:
            S_ = S+1
            R = 0
    else:
        R=0
        if S==0:
            S_ = S
        else:
            S_ = S-1
    return S_,R


def update_env(S, episode , step_counter):#环境的更新，初学者可以不看

    env_list = ['-']*(N_STATES-1)+['T']
    if S == 'terminal':
        interaction = 'episode %s: total_steps = %s' %(episode+1,step_counter)
        print('\r{}'.format(interaction),end="")
        time.sleep(2)
        print('\r                          ',end="")
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end="")
        time.sleep(FRESH_TIME)


def rl():#主循环
    q_table = build_q_table(N_STATES,ACTIONS)#创建表

    for episode in range(MAX_EPISODES):#每个回合
        step_counter = 0
        S = 0#初始化
        is_terminal = False
        update_env(S,episode,step_counter)
        while not is_terminal:#一直循环找路

            A = choose_action(S,q_table)#选择动作
            S_,R = get_env_feedback(S,A)#下一个状态和回报
            q_predict = q_table.loc[S,A] #估计值-Q表中的
            if S_ != 'terminal':
                q_target = R+LAMBDA*q_table.iloc[S_,:].max()#实际值
            else:
                q_target = R#到终点了
                is_terminal = True

            q_table.loc[S,A]+=ALPHA*(q_target-q_predict)#更新小本本 
            S = S_
            print(q_table)
            update_env(S,episode,step_counter+1)
            step_counter+=1
    return q_table






class sudoA(type):
    def __init__(tm, name, bases, dct) -> None:
        tm.x = 1


    def modified(tm):
        tm.x = 10

# class sudoB(sudoA):
#     def __init__(dk):
#         super(sudoB, dk).__init__()
#         dk.h = 11

#     def suModified(dk):
#         dk.h = 69


class hjkg(object):
    x = []
    def __init__(self):
        self.m = 10
        pass


def wsh():
    for i in range(10):
        yield i




import enum

if __name__ == '__main__':
    # a = hjkg()
    # print(a.x)
    # b = hjkg()
    # b.x = 100
    # hjkg.x = 99
    # print(a.x)
    # print(b.x)

    # gh = enum.Enum("wsh", ("a", "b", "c"))
    # print(gh.b)
    # print(gh.b.name)
    # print(type(gh.b.value))
    # print
    # print(gh(1))


    aa = hjkg()
    bb = hjkg()
    aa.x.append(aa)
    bb.x.append(bb)

    print(aa.x)
    print(bb.x)