#########################################
#########################################
#####       AUB                     #####
#####       Joseph Khoury           #####
#####       Master Thesis           #####
#####       Simulation 1            #####
#####       Random                  #####
#########################################
#########################################

import random
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
from itertools import zip_longest

## Flip a coin by defualt 50/50 can modify by passing an argument
def flip_coin(prob_true=0.5):
    return random.random() < prob_true

## Fill and return graph of the Attack Tree
def fill_graph():
    graph = [[] for i in range(32)]
    f = open("graph1.txt", "r")
    lines = f.readlines()
    severity_list = [0]
    for line in lines:
        l = line.split()
        results = list(map(int, l))
        graph[int(results[0])].append(results[0:2])
        # severity_list.append(results[2])
    severity_list = [0, 4, 1, 2, 3, 4, 2, 3, 4, 4, 2, 3, 4, 1, 1, 2, 3, 4, 1, 2, 3, 4, 2, 3, 4, 2, 3, 4, 1, 4, 4, 4]
    return graph, severity_list

## Return Alert from IDS with alert success and severity level
def ids_alert(severity_list, node, budget=0, prob_true=0.5):
    alert_success = flip_coin(prob_true + budget)
    severity = severity_list[node]
    return alert_success, severity

## Run the simulation
def simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, node, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor):
    
    if len(game_steps) <= 25:
        list_choice = []
        
        for x in range (len(graph[node])):
            list_choice.append(graph[node][x][1])

        ###########
        ## Attacker
        ###########
        ## Random choice from the available edges for the Attacker
        new_node = random.choice(list_choice)
        # attacker_success = flip_coin(1.0)
        if new_node == 1 or new_node == 9:
            attacker_success = flip_coin(0.7 - ((severity_list[new_node]/2)/10))
        else:
            attacker_success = flip_coin(0.7 - (severity_list[new_node]/10))

        ###########
        ## Defender
        ###########
        alert_success, _ = ids_alert(severity_list, new_node, prob_true=0.5)
        if alert_success:
            is_reactive = flip_coin()
            if is_reactive:
                defender_success = flip_coin(0.5)
                # defender_success = flip_coin(0.2)
            else:
                defender_success = flip_coin(0.8 * 0.7)
                # defender_success = flip_coin(0.2)

        ###########
        ## Evaluate
        ###########
        if attacker_success:
            if alert_success and defender_success:
                if graph[new_node] == []:
                    if new_node != game[-1]:
                        game.append(new_node)
                        attacker_reward.append(-10*severity_list[new_node])
                        attacker_win_factor.append(False)
                        defender_reward.append(10*severity_list[new_node])
                    elif new_node == game[-1]:
                        attacker_reward[-1] -= 10*severity_list[new_node]
                        defender_reward[-1] += 10*severity_list[new_node]
                    
                    ## Steps
                    attacker_reward_steps.append(attacker_reward_steps[-1])
                    # if (attacker_reward_steps[-1] - 10*severity_list[new_node]) <= 0:
                    #     attacker_reward_steps.append(0)
                    # else:
                    #     # attacker_reward_steps.append(attacker_reward_steps[-1] - 10*severity_list[new_node])
                    #     attacker_reward_steps.append(0)
                    
                    if (defender_reward_steps[-1] + 10*severity_list[new_node]) >= 500:
                        defender_reward_steps.append(500)
                    else:
                        defender_reward_steps.append(defender_reward_steps[-1] + 10*severity_list[new_node])

                    game_steps.append(new_node)
                    
                    ## Win Factor
                    attacker_win_sum = 0
                    for i in attacker_reward_steps:
                        if i > 0:
                            attacker_win_sum += 1
                    attacker_win_factor.append(attacker_win_sum/len(attacker_reward_steps))
                    defender_win_sum = 0
                    for i in defender_reward_steps:
                        if i > 0:
                            defender_win_sum += 1
                    defender_win_factor.append(defender_win_sum/len(defender_reward_steps))

                    simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, node, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor)
                else:
                    if new_node != game[-1]:
                        game.append(new_node)
                        attacker_reward.append(-1*severity_list[new_node])
                        defender_reward.append(1*severity_list[new_node])
                    elif new_node == game[-1]:
                        attacker_reward[-1] -= 1*severity_list[new_node]
                        defender_reward[-1] += 1*severity_list[new_node]
                    
                    ## Steps
                    attacker_reward_steps.append(attacker_reward_steps[-1])
                    # if (attacker_reward_steps[-1] - 1*severity_list[new_node]) <= 0:
                    #     attacker_reward_steps.append(0)
                    # else:
                    #     # attacker_reward_steps.append(attacker_reward_steps[-1] - 1*severity_list[new_node])
                    #     attacker_reward_steps.append(0)
                    
                    if (defender_reward_steps[-1] + 1*severity_list[new_node]) >= 500:
                        defender_reward_steps.append(500)
                    else:
                        defender_reward_steps.append(defender_reward_steps[-1] + 1*severity_list[new_node])

                    game_steps.append(new_node)

                    ## Win Factor
                    attacker_win_sum = 0
                    for i in attacker_reward_steps:
                        if i > 0:
                            attacker_win_sum += 1
                    attacker_win_factor.append(attacker_win_sum/len(attacker_reward_steps))
                    defender_win_sum = 0
                    for i in defender_reward_steps:
                        if i > 0:
                            defender_win_sum += 1
                    defender_win_factor.append(defender_win_sum/len(defender_reward_steps))

                    simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, node, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor)
            else:
                #################################
                ## Attacker have reached a Target
                #################################

                if graph[new_node] == []:
                    if new_node != game[-1]:
                        game.append(new_node)
                        attacker_reward.append(10*severity_list[new_node])
                        defender_reward.append(-10*severity_list[new_node])
                    elif new_node == game[-1]:
                        attacker_reward[-1] += 10*severity_list[new_node]
                        defender_reward[-1] -= 10*severity_list[new_node]

                    # severity_frequency[new_node] += 1

                    ## Steps
                    attacker_reward_steps.append(attacker_reward_steps[-1] + 10*severity_list[new_node])
                    # if (attacker_reward_steps[-1] + 10*severity_list[new_node]) >= 54:
                    #     attacker_reward_steps.append(54)
                    # else:
                    #     attacker_reward_steps.append(attacker_reward_steps[-1] + 10*severity_list[new_node])

                    # if (defender_reward_steps[-1] - 10*severity_list[new_node]) <= 0:
                    #     defender_reward_steps.append(0)
                    # else:
                    #     defender_reward_steps.append(defender_reward_steps[-1] - 10*severity_list[new_node])

                    # Severity
                    if 0 <= new_node <= 12:
                        severity_frequency[0] += 1
                    elif new_node == 13 or 15 <= new_node <= 17:
                        severity_frequency[1] += 1
                    elif  new_node == 14 or 18 <= new_node <= 27:
                        severity_frequency[2] += 1
                    elif  28 <= new_node <= 31:
                        severity_frequency[3] += 1

                    game_steps.append(new_node)

                    ## Win Factor
                    attacker_win_sum = 0
                    for i in attacker_reward_steps:
                        if i > 0:
                            attacker_win_sum += 1
                    attacker_win_factor.append(attacker_win_sum/len(attacker_reward_steps))
                    defender_win_sum = 0
                    for i in defender_reward_steps:
                        if i > 0:
                            defender_win_sum += 1
                    defender_win_factor.append(defender_win_sum/len(defender_reward_steps))

                    return game
                else:
                    if new_node != game[-1]:
                        game.append(new_node)
                        attacker_reward.append(1*severity_list[new_node])
                        defender_reward.append(-1*severity_list[new_node])
                    elif new_node == game[-1]:
                        attacker_reward[-1] += 1*severity_list[new_node]
                        defender_reward[-1] -= 1*severity_list[new_node]

                    # severity_frequency[new_node] += 1

                    ## Steps
                    if new_node not in [17, 24]:
                        attacker_reward_steps.append(attacker_reward_steps[-1] + 1*severity_list[new_node])
                        # if (attacker_reward_steps[-1] + 1*severity_list[new_node]) > 54:
                        #     attacker_reward_steps.append(54)
                        # else:
                        #     attacker_reward_steps.append(attacker_reward_steps[-1] + 1*severity_list[new_node])
                        
                        # if (defender_reward_steps[-1] - 1*severity_list[new_node]) <= 0:
                        #     defender_reward_steps.append(0)
                        # else:
                        #     defender_reward_steps.append(defender_reward_steps[-1] - 1*severity_list[new_node])
                    else:
                        attacker_reward_steps.append(attacker_reward_steps[-1] + 10*severity_list[new_node])
                        # if (attacker_reward_steps[-1] + 10*severity_list[new_node]) > 54:
                        #     attacker_reward_steps.append(54)
                        # else:
                        #     attacker_reward_steps.append(attacker_reward_steps[-1] + 10*severity_list[new_node])
                        
                        # if (defender_reward_steps[-1] - 10*severity_list[new_node]) <= 0:
                        #     defender_reward_steps.append(0)
                        # else:
                        #     defender_reward_steps.append(defender_reward_steps[-1] - 10*severity_list[new_node])

                    # Severity
                    if 0 <= new_node <= 12:
                        severity_frequency[0] += 1
                    elif new_node == 13 or 15 <= new_node <= 17:
                        severity_frequency[1] += 1
                    elif  new_node == 14 or 18 <= new_node <= 27:
                        severity_frequency[2] += 1
                    elif  28 <= new_node <= 31:
                        severity_frequency[3] += 1

                    game_steps.append(new_node)

                    ## Win Factor
                    attacker_win_sum = 0
                    for i in attacker_reward_steps:
                        if i > 0:
                            attacker_win_sum += 1
                    attacker_win_factor.append(attacker_win_sum/len(attacker_reward_steps))
                    defender_win_sum = 0
                    for i in defender_reward_steps:
                        if i > 0:
                            defender_win_sum += 1
                    defender_win_factor.append(defender_win_sum/len(defender_reward_steps))

                    simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, new_node, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor)
        else:
            if graph[new_node] == []:
                if new_node != game[-1]:
                    game.append(new_node)
                    attacker_reward.append(-10*severity_list[new_node])
                    defender_reward.append(10*severity_list[new_node])
                elif new_node == game[-1]:
                    attacker_reward[-1] -= 10*severity_list[new_node]
                    defender_reward[-1] += 10*severity_list[new_node]
                
                ## Steps
                attacker_reward_steps.append(attacker_reward_steps[-1])
                # if (attacker_reward_steps[-1] - 10*severity_list[new_node]) <= 0:
                #     attacker_reward_steps.append(0)
                # else:
                #     # attacker_reward_steps.append(attacker_reward_steps[-1] - 10*severity_list[new_node])
                #     attacker_reward_steps.append(0)
                
                if (defender_reward_steps[-1] + 10*severity_list[new_node]) >= 500:
                    defender_reward_steps.append(500)
                else:
                    defender_reward_steps.append(defender_reward_steps[-1] + 10*severity_list[new_node])

                game_steps.append(new_node)

                ## Win Factor
                attacker_win_sum = 0
                for i in attacker_reward_steps:
                    if i > 0:
                        attacker_win_sum += 1
                attacker_win_factor.append(attacker_win_sum/len(attacker_reward_steps))
                defender_win_sum = 0
                for i in defender_reward_steps:
                    if i > 0:
                        defender_win_sum += 1
                defender_win_factor.append(defender_win_sum/len(defender_reward_steps))

                simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, node, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor)
            else:
                if new_node != game[-1]:
                    game.append(new_node)
                    attacker_reward.append(-1*severity_list[new_node])
                    defender_reward.append(1*severity_list[new_node])
                elif new_node == game[-1]:
                    attacker_reward[-1] -= 1*severity_list[new_node]
                    defender_reward[-1] += 1*severity_list[new_node]
                
                ## Steps
                attacker_reward_steps.append(attacker_reward_steps[-1])
                # if (attacker_reward_steps[-1] - 1*severity_list[new_node]) <= 0:
                #     attacker_reward_steps.append(0)
                # else:
                #     # attacker_reward_steps.append(attacker_reward_steps[-1] - 1*severity_list[new_node])
                #     attacker_reward_steps.append(0)

                if (defender_reward_steps[-1] + 1*severity_list[new_node]) >= 500:
                    defender_reward_steps.append(500)
                else:
                    defender_reward_steps.append(defender_reward_steps[-1] + 1*severity_list[new_node])
                
                game_steps.append(new_node)

                ## Win Factor
                attacker_win_sum = 0
                for i in attacker_reward_steps:
                    if i > 0:
                        attacker_win_sum += 1
                attacker_win_factor.append(attacker_win_sum/len(attacker_reward_steps))
                defender_win_sum = 0
                for i in defender_reward_steps:
                    if i > 0:
                        defender_win_sum += 1
                defender_win_factor.append(defender_win_sum/len(defender_reward_steps))

                simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, node, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor)
    else:
        return game

## Initialize
graph, severity_list = fill_graph()
data = []
num_of_simulation = 1000000

## Run the simulation
for i in range(num_of_simulation):
    if i%1000 == 0:
        print(i, end='\r')
    game = [0]
    game_steps = [0]
    severity_frequency = [0] * 4
    attacker_reward = [0]
    defender_reward = [0]
    attacker_reward_steps = [0]
    defender_reward_steps = [500]
    attacker_win_factor = [0]
    defender_win_factor = [1]
    simulate(graph, severity_list, severity_frequency, attacker_reward, defender_reward, game, 0, attacker_reward_steps, defender_reward_steps, game_steps, attacker_win_factor, defender_win_factor)

    data.append([game, attacker_reward, defender_reward, severity_frequency, game_steps, attacker_reward_steps, defender_reward_steps, attacker_win_factor, defender_win_factor])

###########
## Sampling
###########
sample_data = random.sample(data, k = 10000)
# print("Sample")
# print(len(sample_data))
# sample_data = []
# for i in sample_data1:
#     if len(sample_data) < 1000:
#         if len(i[4]) <= 25:
#             sample_data.append(i)
#     else:
#         break



###########
## Plotting
###########
def plot_impact_graph(freq):
    fig3, ax3 = plt.subplots()
    fig3.canvas.set_window_title('Impact Level') 
    ind = np.arange(4)  # the x locations for the groups
    width = 0.35       # the width of the bars
    c = ["#82B366", "#D6B656", "#D79B00", "#B85450"]
    rects3 = ax3.bar(ind, freq, width, color= c, log=True)
    rects = ax3.patches
    # c = ["#82B366", "#D6B656", "#D79B00", "#B85450"]
    for rect in rects:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = 2
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = y_value

        # Create annotation
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va,                      # Vertically align label differently for
            fontsize=8)
                                        # positive and negative values.

    # add some text for labels, title and axes ticks
    ax3.set_ylabel('Frequency')
    ax3.set_xticks(ind)
    ax3.set_xticklabels(('DMZ Net', 'Enterprise Net', 'SCADA Net', 'Field Net'))

def plot_attacker_graph():
    fig1 = plt.figure("Attacker Reward")
    ax1 = plt.subplot(111)
    # Max number of game steps
    max_game = 0
    # Max number of rewards
    max_reward = 0
    # Average of frequency
    a_avg = []
    # Frequency of each target
    a_freq = []
    # Frequency of Impact levels
    d_t_impact_level = [0] * 4

    for sample in sample_data:
        ## Get Game, Reward, Frequency
        game = sample[4]
        a_reward = sample[5]
        impact_frequency = sample[3]

        ## Get longest Game
        if len(game) > max_game:
            max_game = len(game)

        ## Get Highest Reward
        if a_reward[-1] > max_reward:
            max_reward = a_reward[-1]

        a_freq.extend([0] * (len(a_reward) - len(a_freq)))
        ## Get Frequency
        for i in range(len(a_reward)):
            a_freq[i] += 1

        # Normalize reward
        for i in range(len(a_reward)):
            a_reward[i] = a_reward[i] / max_reward

        a_avg = [sum(n) for n in zip_longest(a_avg, a_reward, fillvalue=0)]

        # Impact Frequency
        for i in range(len(impact_frequency)):
            d_t_impact_level[i] += impact_frequency[i]

        ax1.plot(np.arange(len(game)), a_reward, linewidth=0.5)
    ax1.plot(np.arange(len([])), [], linewidth=0.5, label="Games")
    # print("^^^^^")
    # print(max_game)
    # print(max_reward)

    plot_impact_graph(d_t_impact_level)
    # print(d_t_impact_level)

    for i in range (len(a_avg)):
        a_avg[i] = a_avg[i]/a_freq[i]
    for i in range (1, len(a_avg)):
        if a_avg[i] < a_avg[i-1]:
            a_avg[i] = a_avg[i-1]
    # print(a_avg)
    ax1.plot(np.arange(len(a_avg)), a_avg, color='black', linewidth=2, label="Average of Games")
    ax1.set_xlabel('Actions')
    ax1.set_ylabel('Reward')
    ax1.legend()



    ax1.set_xticks(list(range(0, max_game, 1)))
    [tick.label.set_fontsize(7) for tick in ax1.xaxis.get_major_ticks()]

def plot_defender_graph():
    fig2 = plt.figure("Defender Reward")
    ax2 = plt.subplot(111)
    max_game = 0
    d_avg = []
    d_freq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    d_t_impact_level = [0] * 4
    for sample in sample_data:
        ## Get the Game, and reward for each actions
        game = sample[4]
        d_reward = sample[6]
        impact_frequency = sample[3]

        # Get longest Game
        if len(game) > max_game:
            max_game = len(game)
        
        ## Get Frequency
        for i in range(len(d_reward)):
            d_freq[i] += 1
        
        # Normalize
        for i in range(len(d_reward)):
            # d_reward[i] = ((d_reward[i] * 54) / 674) / 54
            d_reward[i] = d_reward[i] / 500
        d_avg = [sum(n) for n in zip_longest(d_avg, d_reward, fillvalue=0)]

        ax2.plot(np.arange(len(game)), d_reward, color='gray', linewidth=0.5)
    ax2.plot(np.arange(len([])), [], color='gray', linewidth=0.5, label="Games")

    for i in range (len(d_avg)):
        d_avg[i] = d_avg[i]/d_freq[i]

    ax2.plot(np.arange(len(d_avg)), d_avg, color='black', linewidth=2, label="Average of Games")
    ax2.set_xlabel('Actions')
    ax2.set_ylabel('Reward')
    ax2.legend()
    ax2.set_xticks(list(range(0, max_game, 1)))

plot_attacker_graph()
# plot_defender_graph()
plt.show()
input()