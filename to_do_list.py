# %%
import numpy as np
import pandas as pd
import operator

# %%
# Dataframe for tasks and corresponding reards and duration.
data = pd.DataFrame(
    None, columns=['Tasks', 'Fair Price', 'Duration', 'Rewards'])
data.loc[0] = ['one', 3, 5, -3]
data.loc[1] = ['two', 3.25, 10, -3.25]
data.loc[2] = ['three', 2.25, 15, -2.25]
data.loc[3] = ['four', 3, 20, -3]
data.loc[4] = ['five', 1, 25, -1]

# %%
# This function is used to output the next available states given the current state as input.


def available_states(current_state):
    curr = current_state
    s = []
    actions = [i for i, e in enumerate(curr) if e == 0]
    # print (actions)
    for a in actions:
        cs = curr.copy()
        cs[a] = 1
        s.append(cs)
    return s


# To get the value of rewards if the user opts to leave the experiment given the current state.
def reward_forgotten(current_state):
    r = 0
    completed_tasks = [i for i, e in enumerate(current_state) if e == 1]
    for i in completed_tasks:
        r += (float(data.iloc[i]['Duration']))*hour_value/60
    return r

# to get the value of reward given current and next state.


def reward(current_state, next_state):
    diff = list(map(operator.sub, next_state, current_state))
    action = [i for i, e in enumerate(diff) if e == 1]
    return float(data.iloc[action]['Rewards'])


# %%
# Change these value to check the effect on pseudo rewards in different environments.
gamma = 0.95
hour_value = 8
# %%

# To calculate state values


def calc_val(current_state, steps_rem):
    v = []
    if current_state.count(0) == steps_rem:
        while steps_rem >= 0:
            if steps_rem == 0:
                return 20
            else:
                for next_state in available_states(current_state):
                    q = reward(current_state, next_state) + gamma * \
                        (0.975 * calc_val(next_state, steps_rem - 1) +
                         0.025 * (reward_forgotten(current_state)))
                    v.append(q)
                return (max(v))
    else:
        return print("Please enter valid state")
# %%

# To calculate psuedo reward given current and next state.


def calc_pseudo_reward(current_state, next_state, steps_rem):
    prew = (gamma *
            (calc_val(next_state, steps_rem-1))) - \
        calc_val(current_state, steps_rem)

    return prew


# %%
# To calculate psuedo reward of all possible next state given the current state.
def preward(current_state):
    if len(current_state) == 5:
        steps_remaining = current_state.count(0)
        for i in available_states(current_state):
            print("\n{}>>>>>>{}".format(i, calc_pseudo_reward(
                current_state, i, steps_remaining)))
    else:
        print("Please enter status of FIVE tasks.")


# %%
# Execution code
if __name__ == "__main__":
    current_state = list(
        map(int, input("\nEnter states status separated by spaces (0 for incomplete and 1 for completed): ").strip().split()))[:5]
    print("\nAvailable states >>>>>> Incentives for completing")
    preward(current_state)


# %%
