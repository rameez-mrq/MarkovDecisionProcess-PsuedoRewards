
# %%
import numpy as np
# %%
# shorthands for cities anme
J = "Jonesville"
S = "Smithsville"
Ba = "Bakersville"
C = "Clarksville"
Br = "Brownsville"
W = "Williamsville"
# %%
# Data used in MDP. Used dictionary instad of a dataframe for clarity in code.
graph_reward = {
    J: {0: -30, 1: -70},
    S: {0: 140, 1: 30},
    W: {0: -70, 1: -30},
    Br: {0: -30, 1: 30},
    C: {0: -30, 1: -70},
    Ba: {0: -30, 1: 30}}
graph_states = {
    J: {0: W, 1: C},
    S: {0: J, 1: Br},
    W: {0: Ba, 1: Br},
    Br: {0: C, 1: J},
    C: {0: Ba, 1: S},
    Ba: {0: S, 1: W}}

states = [J, S, Ba, C, Br, W]

# %%
# Calculate value function
v = []


def calc_val(start, steps):
    v = []
    while steps != 0:
        if steps == 1:
            for a in range(2):
                q = graph_reward[start][a]
                v.append(q)
                # print(q)
            return (max(v))
        else:
            for a in range(2):
                q = graph_reward[start][a] + \
                    calc_val(graph_states[start][a], steps-1)
                v.append(q)
                # print
            return (max(v))


# %%
# To calculate Pseudo reward as per equation 10 in Lieder et al. (2019)
graph_mod = {
    J: {W: -30, C: -70},
    S: {J: 140, Br: 30},
    W: {Ba: -70, Br: -30},
    Br: {C: -30, J: 30},
    C: {Ba: -30, S: -70},
    Ba: {S: -30, W: 30}}


def calc_prew(steps, final={}):
    for curr_s in graph_mod.keys():
        next_state_dict = {}
        for next_s in graph_mod[curr_s]:
            if steps == 1:
                prew = graph_mod[curr_s][next_s]
            else:
                prew = (graph_mod[curr_s][next_s] +
                        calc_val(next_s, steps-1)-calc_val(curr_s, steps))
            next_state_dict[next_s] = prew
        final[curr_s] = next_state_dict
    return final


# %%

# Formatting required output.
def avail_options(start, steps):
    graph = calc_prew(steps)
    for i in graph[start]:
        print("Available paths:: {} >>>>>>>>>>> {} : Reward = {}".format(
            start, i, graph[start][i]))


# %%
# Execution code
states_dict = {'J': "Jonesville",
               'S': "Smithsville",
               'Ba': "Bakersville",
               'C': "Clarksville",
               'Br': "Brownsville",
               'W': "Williamsville"}
if __name__ == "__main__":
    print(states_dict)
    start = states_dict[input("\nEnter starting point : ")]
    steps = int(input("\nEnter number of flights remaining:"))
    avail_options(start, steps)


# %%
