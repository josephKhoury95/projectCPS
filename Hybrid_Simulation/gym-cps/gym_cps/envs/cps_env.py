import gym, os, random, sys, time, threading
from gym import error, spaces, utils
from gym.utils import seeding
import random
from random import sample

#from mininet.net import Mininet
#from mininet.topo import Topo
#from mininet.node import Controller, RemoteController, OVSController
#from mininet.node import CPULimitedHost, Host, Node
#from mininet.node import OVSKernelSwitch, UserSwitch
#from mininet.node import IVSSwitch
#from mininet.log import setLogLevel, info
#from mininet.link import TCLink, Intf
#from mininet.term import makeTerm
#from random import randint

## Class node
class node(object):

    def __init__(self, i, n, p, m, a_s, a_v, d_v, n_v, r):
        ## Constructor of Class Node
        ## i: Index of the Node
        ## n: name of the node
        ## p: path of the node(Host, Switch)
        ## m: moves for a specific Node
        ## a_v: Attacker value
        ## d_v: Defender value
        self.index = i
        self.name = n
        self.path = p
        self.moves = m
        self.attacker_space = a_s
        self.attacker_value = a_v
        self.defender_value = d_v
        self.nb_vulnerability = n_v
        self.reward = r

def worker(net, receiver):
    ## Threading function for Receiver
    ## Made with thread to avoid blocking
    net.terms += makeTerm(net.get(receiver.name), term='xterm', cmd='nc -lp 1234 > ' + receiver.path + 'a.txt')

## Class to Create our GYM Environment
class CpsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Set initial state of our RL problem

        self.net = None
        ## PATH where all the directories are stored
        self.virus_path = 'Start/'
        ## All the initial state of our environment
        ## All the instances of type Class Node

        self.state = [  node(0,     's',    '',     [1],            [0, 0, 0, 0, 0],                                                [0, 0, 0, 0, 0],    [0, 0, 0, 0, 0, 0], 0, 0),     # Start state           0
        node(1,     's1',   '',     [2, 3, 4, 1],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [5, 4, 6, 2, 8, 9], 1, 50),    ##### Firewall A            1
        node(2,     'h1',   '',     [5, 2, 3, 4],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 6, 5, 6, 6, 7], 1, 100),   # Email Server          2
        node(3,     'h2',   '',     [5, 2, 3, 4],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [5, 4, 8, 7, 7, 8], 1, 100),   # Web Server            3
        node(4,     'h3',   '',     [5, 2, 3, 4],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 5, 4, 7, 8, 8], 1, 100),   # Database Server       4
        node(5,     's2',   '',     [6, 7, 8, 5],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 6, 2, 5, 6, 7], 1, 1000),  ##### Firewall B            5
        node(6,     'h4',   '',     [9, 6, 7, 8],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 2, 6, 5, 8, 2], 1, 100),   # Office Computer1      6
        node(7,     'h5',   '',     [9, 6, 7, 8],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [6, 1, 7, 4, 6, 2], 1, 100),   # Office Computer2      7
        node(8,     'h6',   '',     [9, 6, 7, 8],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 5, 6, 2, 7, 2], 1, 100),   # Office Computer3      8
        node(9,     's3',   '',     [10, 11, 12, 9],        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 1, 7, 8, 6, 2], 1, 2000),  ##### Firewall C            9
        node(10,    'h7',   '',     [13, 10, 11, 12],       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 2, 6, 7, 7, 3], 1, 3000),  # SCADA Server          10
        node(11,    'h8',   '',     [13, 10, 11, 12],       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 8, 0, 1, 7, 3], 1, 3000),  # SCADA HMI             11
        node(12,    'h9',   '',     [13, 10, 11, 12],       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [6, 7, 2, 8, 9, 3], 1, 3000),  # SCADA Historian       12
        node(13,    's4',   '',     [14, 13],               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],                                 [0, 0, 0, 0, 0],    [8, 6, 5, 2, 8, 3], 1, 4000),  ##### Firewall D (switch)   13
        node(14,    'h10',  '',     [14],                   [0, 0, 0, 0, 0],                                                [0, 0, 0, 0, 0],    [8, 0, 7, 3, 6, 3], 1, 5000),  # Field Device (PLC)    14
        node(15,    'e',    '',     [],                     [],                                                             [],                 [], 0, 0),
        ]

        ## Done=False this means our game is not Done, True means Done!
        self.done = False
        self.win = False
        ## Reward points for both Attacker and Defender
        self.attacker_reward = 0
        self.defender_reward = 0
        
        ## Win factor for attacker and defender
        # Attacker win factor is: -1
        # Defender win factor is: 1
        self.win_factor = 1
        ## Win step only for attacker to tell if the step was successful or not
        # 0: not successful
        # 1: successful
        self.win_step = 0
        
        ## Observation of type Node (Class Node)
        self.observation, self.d_observation = self.make_directories()

        self.cur_host = self.observation

    def set_environment(self, net):
        self.net = net

    def make_directories(self):
        # This function is used to create the directories of the CPS network devices
        # This will also insert a virus randomly on the network

        path = self.virus_path
        ## TODO: REMOVE COMMENT
#        os.system('mkdir -p ' + self.virus_path)
#        os.system('touch ' + self.virus_path + 'a.txt')
        self.virus_path = self.virus_path + 'a.txt'

        ## TODO: REMOVE COMMENT
#        for n in self.state[1:]:
#            if n.name == 's1':
#                path += str(n.name) + '/'
#                n.path = path
#                os.system('mkdir -p ' + path)
#            elif n.name == 's2':
#                path += str(n.name) + '/'
#                n.path = path
#                os.system('mkdir -p ' + path)
#            elif n.name == 's3':
#                path += str(n.name) + '/'
#                n.path = path
#                os.system('mkdir -p ' + path)
#            elif n.name == 's4':
#                path += str(n.name) + '/'
#                n.path = path
#                os.system('mkdir -p ' + path)
#            else:
#                n.path = path + str(n.name) + '/'
#                os.system('mkdir -p ' + path + str(n.name) + '/')

        # Selecting only hosts from the state list
        # By other mean removing the Start state and the four switches
        host_list = []
        for h in self.state:
            if h.name not in ['s', 's1', 's2', 's3', 's4', 'e']:
                host_list.append(h)

        ## Choose a random Host
        p = random.choice(host_list)

        ## ************************
        ## Random start for Defender
        ## Defender can start on a switch!!!
        d_host_list = []
        for d_h in self.state:
            if d_h.name not in ['s', 'e']:
                d_host_list.append(d_h)
        ## Choose a random Host for Defender
        d_p = random.choice(d_host_list)

        ## TODO: REMOVE COMMENT
        ## Insert a virus in the randomly chosen Host
        #os.system('cp ' + self.virus_path + ' ' + p.path)
        self.virus_path = p.path + 'a.txt'

        ## p returned is a host of type Class Node
        return p, p

    def biased_flip(self, prob_true=0.5):
        return random.random() < prob_true

    #########################
    ### Attacker Action Space
    def attacker_action_space(self, node):
        ## This function is used to return the action space for the attacker..

        ## It return a list of the possible node moves
        ## Each instance of the list is of type Node
        action_space = []

        for x in node.moves:
            action_space.append(self.state[x])

        ## [Node1, ...]
        return action_space

    def attacker_action_space_sample(self, node):
        ## node: of Type Node (Instance of class node)

        ## If Virus is on the last host no need to sample..
        ## This case is only valid for whenever the random host chosen at the begining
        ## Was "h10"
        
        ## Get the moves of this node [6, 7, 8, 9]
        node_moves = node.moves
        node_moves.sort()

        ## Get attack space [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ## attack_index_value = (index, value)
        attack_space_index_value = random.choice(list(enumerate(node.attacker_space)))
        
        index = -1
        for i in range(4):
            if i*5 <= attack_space_index_value[0] < (i+1)*5:
                index = i
                break

        ## Next node
        next_node = self.state[node_moves[index]]

        attack_val_index = attack_space_index_value[0] - (5*index)
        
        return [node, next_node, attack_val_index]

    #########################
    ### Defender Action Space
    def defender_action_space_sample(self, node):
        # This function is used to return the action space for the defender..

        ## Take a sample from the states
        ## Skip first state the start state
        next_move_node_choice = sample(self.state[1:], 1)

        ## Sample from the DefenceValue of the chosen Node
        ## Enumerate was used to get the index of the Attack value
        defense_value_index = sample(list(enumerate(next_move_node_choice[0].defender_value)), 1)

        ## [Node, NextNode, Index.of.Next.Node.AttackValue]
        action_space_inner_sample = [node, next_move_node_choice[0], defense_value_index[0][0]]

        ## [Node, NextNode, Index.of.Next.Node.AttackValue]
        return action_space_inner_sample

    #######################################
    ### Both Attacker&Defender Action Space
    def action_sample(self, node):
        ## This function is used to return a tuple of both actions
        ## AttackerSampleAction at index 0
        ## DefenderSampleAction at index 1
        return self.attacker_action_space_sample(node)

    def action_sample_jk(self, node):
        ## node: of Type Node (Instance of class node)
        
        ## Get the moves of this node [6, 7, 8, 9]
        node_moves = node.moves
        node_moves.sort()

        ## Get attack space [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ## attack_index_value = (index, value)

        index = random.choice(node_moves)
        ## Next node
        next_node = self.state[index]

        ## This is done to do a weighted random choice on the defenders list this way the defender will less be likely to find the ZERO-DAY Vulnerability...
        weights = []
        special_weight = 0
        for e in range(len(next_node.attacker_value)):
            if next_node.defender_value[e] != 0:
                weights.append(1/(len(next_node.attacker_value))-0.01)
                special_weight += 0.01
            else:
                weights.append(0)

        for i in range (len(weights)):
            if weights[i] == 0:
                weights[i] = special_weight

        ## Next node index
        ## [(index, value)]
        next_node_index = random.choices(list(enumerate(next_node.attacker_value)), weights)
        attack_val_index = next_node_index[0][0]

        return [node, next_node, attack_val_index]


    def defender_action_sample_1(self, attacker_action):
        ## Random node
        # returned in a list with node inside it
        # defender_next_move_node_choice = sample(self.state[1: -1], 1)

        ## Same next node as Attacker
        defender_next_move_node_choice = [attacker_action[1]]

        ## This is done to do a weighted random choice on the defenders list this way the defender will less be likely to find the ZERO-DAY Vulnerability...
        weights = []
        special_weight = 0
        for e in defender_next_move_node_choice[0].defender_value:
            if e != 0:
                weights.append(1/(len(defender_next_move_node_choice[0].defender_value)-1)-0.01)
                special_weight += 0.01
            else:
                weights.append(0)

        for i in range (len(weights)):
            if weights[i] == 0:
                weights[i] = special_weight
        
        ## [(index, value)]
        defender_next_move_node_index = random.choices(list(enumerate(defender_next_move_node_choice[0].defender_value)), weights)

        next_move_node_index = defender_next_move_node_index[0][0]
        ## Return format
        ## [attacker_action, Next_node_move, next_move_node_index]
        return [attacker_action, defender_next_move_node_choice[0], next_move_node_index]

    def defender_action_sample_jk(self, a_action, d_observation):
        ## Argument: a_action = [observation, new_node, new_node_index, win_step]

        ## Random from the states
        defender_next_move_node_choice = [random.choice(self.state[1:-1])]

        defender_next_move_node_index = random.choices(list(enumerate(defender_next_move_node_choice[0].defender_value[:-1])))

        ## Return format
        ## [attacker_action, defender_curr_state, Next_node_move, next_move_node_index]
        return [a_action, d_observation, defender_next_move_node_choice[0], defender_next_move_node_index[0][0]]

    
    def defender_action_sample_jk_jk(self, attacker_action):
        ## attacker_action = [a_observation, a_next_node, a_next_node_index]

        ## Same next node as Attacker
        # defender_next_move_node_choice = attacker_action[1]
        
        ## Random from the states
        defender_next_move_node_choice = [random.choice(self.state[1:-1])][0]

        ## This is done to do a weighted random choice on the defenders list this way the defender will less be likely to find the ZERO-DAY Vulnerability...
        weights = []
        special_weight = 0
        for e in defender_next_move_node_choice.defender_value:
            if e != 0:
                weights.append(1/(len(defender_next_move_node_choice.defender_value)-1)-0.01)
                special_weight += 0.01
            else:
                weights.append(0)

        for i in range (len(weights)):
            if weights[i] == 0:
                weights[i] = special_weight
        
        ## [(index, value)]
        defender_next_move_node_index = random.choices(list(enumerate(defender_next_move_node_choice.defender_value)), weights)

        next_move_node_index = defender_next_move_node_index[0][0]
        ## Return format
        ## [attacker_action, Next_node_move, next_move_node_index]
        return [attacker_action, defender_next_move_node_choice, next_move_node_index]


    def defender_action_sample_jk_jk2(self, attacker_action, d_observation):
        ## attacker_action = [a_observation, a_next_node, a_next_node_index]

        ## Use node that should be a target
        # moves
        a_winned_node_moves = attacker_action[1].moves
        a_winned_node_moves.sort()
        
        ## If gateway
        if attacker_action[1].name in ['s1', 's2', 's3']:
            # Block next gateway or block MINIMUM in the network
            # FOR NOW BLOCK THE NEXT GATEWAY!!!!!!
            defender_next_move_node_choice = self.state[a_winned_node_moves[-1]+1]

        # Else not a gateway
        else:
            defender_next_move_node_choice = self.state[a_winned_node_moves[-1]]

        ## This is done to do a weighted random choice on the defenders list this way the defender will less be likely to find the ZERO-DAY Vulnerability...
        weights = []
        special_weight = 0
        for e in defender_next_move_node_choice.defender_value:
            if e != 0:
                weights.append(1/(len(defender_next_move_node_choice.defender_value)-1)-0.01)
                special_weight += 0.01
            else:
                weights.append(0)

        for i in range (len(weights)):
            if weights[i] == 0:
                weights[i] = special_weight
        
        ## [(index, value)]
        defender_next_move_node_index = random.choices(list(enumerate(defender_next_move_node_choice.defender_value)), weights)

        next_move_node_index = defender_next_move_node_index[0][0]
        ## Return format
        ## [attacker_action, Next_node_move, next_move_node_index]
        return [attacker_action, d_observation, defender_next_move_node_choice, next_move_node_index]


    ## This is used to sample defender action
    def defender_action_sample(self, attacker_action):
        
        if attacker_action[-1] == 1 and attacker_action[1].name not in ['s4', 'h10']:

            ## Next Node
            sort_moves = attacker_action[1].moves
            defender_next_move_node_choice = self.state[sort_moves[-1]+1]

            ## Next Index, to be the next gateway with the minimum defense value
            ind = 0
            mini = 100
            for index in range (len(defender_next_move_node_choice.defender_value)):
                if defender_next_move_node_choice.defender_value[index] < mini:
                    mini = defender_next_move_node_choice.defender_value[index]
                    ind = index
            defender_next_move_node_index=[[ind]]

        else:
            ## Same next node as Attacker
            defender_next_move_node_choice = attacker_action[1]

            ## This is done to do a weighted random choice on the defenders list this way the defender will less be likely to find the ZERO-DAY Vulnerability...
            weights = []
            special_weight = 0
            for e in defender_next_move_node_choice.defender_value:
                if e != 0:
                    weights.append(1/(len(defender_next_move_node_choice.defender_value)-1)-0.01)
                    special_weight += 0.01
                else:
                    weights.append(0)

            for i in range (len(weights)):
                if weights[i] == 0:
                    weights[i] = special_weight
            
            ## [(index, value)]
            defender_next_move_node_index = random.choices(list(enumerate(defender_next_move_node_choice.defender_value)), weights)

        next_move_node_index = defender_next_move_node_index[0][0]
        ## Return format
        ## [attacker_action, Next_node_move, next_move_node_index]
        return [attacker_action, defender_next_move_node_choice, next_move_node_index]

    ### This function is made to be used in the exploitattion part in the Q-learning algorithm
    ## It will take as input an object of type Node (it is the observation)
    # and return the same pattern as (action_sample) function [node, next_node, attack value] (for both attacker and defender)
    def return_action_space(self, node):
        ## action_space=List of all possible moves
        ## action_space=[Node1, ...]
        action_space = self.attacker_action_space(node)
        return action_space

    def defense_step_1(self, d_action):
        ## This function takes an argument with the following format
        ## [a_action, next_move_node, next_move_node_index]

        defender_reward = 0

        ## Apply Defender action
        if d_action[1].defender_value[d_action[2]] < 10:
            d_action[1].defender_value[d_action[2]] += 1

        if d_action[1].defender_value[-1] < 10:
            d_action[1].defender_value[-1] += 1

        ## Check if condition applies and assign the reward
        
        ########################################
        ########################################
        ##  Testing on the random functionnnnn

        # If a successful attack: get reward, move to next node
        if d_action[0][1] == d_action[1] and d_action[0][2] == d_action[2] and d_action[0][-1] == 0:
            defender_reward = d_action[1].reward
            self.d_observation = d_action[1]
        ## Else: get reward, stay on the same node
        elif d_action[0][1] == d_action[1] and d_action[0][2] == d_action[2] and d_action[0][-1] == 1:
            defender_reward = d_action[1].reward
            self.d_observation = d_action[0][0]
        
        return defender_reward, self.d_observation

    def defense_step_jk(self, d_action):
        ## This function takes an argument with the following format
        ## [a_action, defender_curr_observation, next_move_node, next_move_node_index]

        defender_reward = 0

        ## If winning step
        if d_action[0][3] == 1:
            
            # moves
            a_winned_node_moves = d_action[0][1].moves
            a_winned_node_moves.sort()

            # If it is a gateway
            if d_action[0][1].name in ['s1', 's2', 's3']:
                
                # Block next gateway or block MINIMUM in the network
                # FOR NOW BLOCK THE NEXT GATEWAY!!!!!!
                defender_target_node = self.state[a_winned_node_moves[-1]+1]
                minimum = min(defender_target_node.defender_value)
                defender_target_min_node_index = defender_target_node.defender_value.index(minimum)

                if d_action[2] == defender_target_node and d_action[3] == defender_target_min_node_index:
                    defender_reward = d_action[2].reward
                
            
            # If it is a normal host
            else:
                defender_target_node = self.state[a_winned_node_moves[-1]]
                minimum = min(defender_target_node.defender_value)
                defender_target_min_node_index = defender_target_node.defender_value.index(minimum)

                if d_action[2] == defender_target_node and d_action[3] == defender_target_min_node_index:
                    defender_reward = d_action[2].reward

        ## Apply Defender action
        if d_action[2].defender_value[d_action[3]] < 10:
            d_action[2].defender_value[d_action[3]] += 1

        if d_action[2].defender_value[-1] < 10:
            d_action[2].defender_value[-1] += 1

        return self.d_observation, defender_reward

    def defense_step_jk_jk(self, d_action):
        ## d_action = [a_action, d_next_move_node, d_next_move_node_index]

        self.defender_reward = 0
        self.d_observation = d_action[1]

        if self.d_observation.defender_value[d_action[2]] < 10:
            self.d_observation.defender_value[d_action[2]] += 1

        return self.defender_reward


    def defense_step_jk_jk2(self, d_action):
        ## d_action = [a_action, d_cur_observation, d_next_move_node, d_next_move_node_index]

        self.defender_reward = 0
        self.d_observation = d_action[2]

        if self.d_observation.defender_value[d_action[3]] < 10:
            self.d_observation.defender_value[d_action[3]] += 3

        #moves
        a_winned_node_moves = d_action[0][1].moves
        a_winned_node_moves.sort()

        ## If it is a gateway
        if d_action[0][1].name in ['s1', 's2', 's3']:

            ## Get the target node for the defender
            defender_target_node = self.state[a_winned_node_moves[-1]+1]
            minimum = min(defender_target_node.defender_value)
            defender_target_min_node_index = defender_target_node.defender_value.index(minimum)

            if d_action[2] == defender_target_node:
                if defender_target_min_node_index == d_action[3]:
                    self.defender_reward = d_action[2].reward*10
        ## If it is a host
        else:
            ## Get the target node for the defender
            defender_target_node = self.state[a_winned_node_moves[-1]]
            minimum = min(defender_target_node.defender_value)
            defender_target_min_node_index = defender_target_node.defender_value.index(minimum)

            if d_action[2] == defender_target_node:
                if defender_target_min_node_index == d_action[3]:
                    self.defender_reward = d_action[2].reward*10

        return self.d_observation, self.defender_reward

    def defense_step(self, d_action):
        ## This function takes an argument with the following format
        ## [a_action, next_move_node, next_move_node_index]

        defender_reward = 0
        ## Apply Defender action
        if d_action[1].defender_value[d_action[2]] < 10:
            d_action[1].defender_value[d_action[2]] += 1

        if d_action[1].defender_value[-1] < 10:
            d_action[1].defender_value[-1] += 1

        ########################################
        ########################################
        ##  Testing on the random functionnnnn

        if d_action[0][1] == d_action[1] and d_action[0][2] == d_action[2]:
            defender_reward = d_action[1].reward

        return defender_reward

    def attack_step(self, action):

        ## Check if eligible attack
        if action[1].attacker_value[action[2]] > action[1].defender_value[action[2]] or (action[1].attacker_value[action[2]] == 0 and action[1].defender_value[action[2]] == 0) :

            if action[1].attacker_value[action[2]] < 10:
                ## Increment Attack Value
                action[1].attacker_value[action[2]] += 1
                if action[1].defender_value[action[2]] > 0:
                    ## Decrement Defender Value
                    action[1].defender_value[action[2]] -= 1

            self.observation = action[1]
            
            if self.observation.nb_vulnerability > 0:
                self.observation.nb_vulnerability -= 1
            
            if action[1].name not in ['s', 's1', 's2', 's3', 's4']:

                ## TODO: REMOVE BELOW COMMENT TO SEND VIRUS BETWEEN FILES!!!!!!!
                # port = 1234
                # threads = []

                # ## Receiver
                # t = threading.Thread(target=worker, args=(self.net, action[0][1]))
                # threads.append(t)
                # t.start()

                # time.sleep(3)

                # ## Sender
                # self.net.terms += makeTerm(self.net.get(self.cur_host.name), cmd='nc -w 3 ' + self.net.get(action[0][1].name).IP() + ' 1234 < ' + self.virus_path)

                self.virus_path = action[1].path + 'a.txt'
                self.cur_host = action[1]

            if self.observation.name == 'h10' and self.observation.nb_vulnerability == 0:
                self.done = True
                self.win = True
                self.attacker_reward = self.observation.reward

                self.win_factor = -1
            else:
                self.done = False
                self.attacker_reward = self.observation.reward

        else:
            ## Attack not successful because attack values are much less
            ## We can make use of probability of detection..
            
            ## TODO: REMOVE BELOW COMMENT TO RETURN FUNCTIONALITY OF IDS (for Defender)
            # if random.randint(1, 10) > action[1][1].defender_value[-1]:
            #     ## This case if the random value above the detection value
            #     ## the attack is detected and the defender wins!
                
            #     self.observation = action[0][0]
            #     self.done = True
            #     self.attacker_reward += -100
            #     self.defender_reward = 100
            
            if action[1].attacker_value[action[2]] < 10:
                ## Increment Attacker value
                action[1].attacker_value[action[2]] += 1
                ### I REMOVED THE DECREMENT FOR THE DEFENDER !!!!!!
                # if action[0][1].defender_value[action[0][2]] > 0:
                #     ## Decrement Defender value
                #     action[0][1].defender_value[action[0][2]] -= 1

            ## TODO: here I didn't include the defender!!!!
            ## Fix this ELSE section to include the defender
            # self.observation = action[0][0]
            # self.done = False
            # # self.attacker_reward = -(self.observation.reward/2)
            # self.attacker_reward = 0

            ## This case when the attack is not successfull
            if  random.random()*10 < action[0].defender_value[-1]:
                ## Attack failed and was detected by the defender (IDS)
                self.observation = action[0]
                self.done = True
                self.attacker_reward = 0
                self.defender_reward = action[0].reward

                self.win_factor = 1
            else:
                self.observation = action[0]
                self.done = False
                self.attacker_reward = 0
                self.defender_reward = 0

        ## [Node, AttackerReward, DefenderReward, Done]
        ## Should add an element for the defender to detect the virus 
        ## and if it was detected the defender can start making pressusre on the virus
        return [self.observation, self.attacker_reward, self.defender_reward, self.done, self.win_factor]



    def attack_step_1(self, action):
        ## Takes action argument: [observation, next_state, next_state_index]
        ## Returns: new_observation, reward_a, reward_b, done, win-factor

        ## Apply Attacker action
        if action[1].attacker_value[action[2]] < 10:
            action[1].attacker_value[action[2]] += 1
            if action[1].defender_value[action[2]] > 0:
                action[1].defender_value[action[2]] -= 1
                    
        ## Check condition for a successful attack
        if action[1].attacker_value[action[2]] > action[1].defender_value[action[2]]:

            ## Attack successful move to next node!
            self.observation = action[1]
            self.win_step = 1
            
            ## Decrement the number of vulnerability needed to compromise a node
            ## In our case we kept it for one only
            if self.observation.nb_vulnerability > 0:
                self.observation.nb_vulnerability -= 1
            
            ## This is used for networking implementation; explantion below
            if action[1].name not in ['s', 's1', 's2', 's3', 's4']:

                ## TODO: REMOVE BELOW COMMENT TO SEND VIRUS BETWEEN FILES!!!!!!!
                # port = 1234
                # threads = []

                # ## Receiver
                # t = threading.Thread(target=worker, args=(self.net, action[0][1]))
                # threads.append(t)
                # t.start()

                # time.sleep(3)

                # ## Sender
                # self.net.terms += makeTerm(self.net.get(self.cur_host.name), cmd='nc -w 3 ' + self.net.get(action[0][1].name).IP() + ' 1234 < ' + self.virus_path)

                self.virus_path = action[1].path + 'a.txt'
                self.cur_host = action[1]
            
            ## Check if game is done
            if self.observation.name == 'h10' and self.observation.nb_vulnerability == 0:

                self.done = True
                self.win = True
                self.attacker_reward = self.observation.reward
                self.win_factor = -1
            else:

                self.done = False
                self.attacker_reward = self.observation.reward
        
        ## Else if attack was not successful
        else:
            if  random.random()*10 < action[0].defender_value[-1]:
                ## Attack failed and was detected by the defender (IDS)
                self.observation = action[0]
                self.done = True
                self.attacker_reward = 0
                self.defender_reward = action[0].reward
                self.win_factor = 1

            else:
                ## Attack failed and was not detecteds
                self.observation = action[0]
                self.done = False
                self.attacker_reward = 0
                self.defender_reward = 0

        return [self.observation, self.attacker_reward, self.defender_reward, self.done, self.win_factor, self.win_step]



    def attack_step_1_jk(self, action, a_strategy='s', d_strategy='h'):
        ## Takes action argument: [observation, next_state, next_state_index]
        ## strategy: s-> stealthy only              sb-> stealthy+budget
        ## Returns: new_observation, reward_a, reward_b, done, win-factor
        
        self.attacker_reward = 0

        if a_strategy == 's':
            rand = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        elif a_strategy == 'sb':
            rand = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])

        # if random.randint(0, 10) > (action[1].defender_value[action[2]]):
        if rand > (action[1].defender_value[action[2]]):
            
            ## Attack successful move to next node!
            action[1].attacker_value[action[2]] += 1
            self.observation = action[1]
            self.win_step = 1
            
            ## Decrement the number of vulnerability needed to compromise a node
            ## In our case we kept it for one only
            if self.observation.nb_vulnerability > 0:
                self.observation.nb_vulnerability -= 1
            
            ## This is used for networking implementation; explantion below
            if action[1].name not in ['s', 's1', 's2', 's3', 's4']:

                ## TODO: REMOVE BELOW COMMENT TO SEND VIRUS BETWEEN FILES!!!!!!!
                # port = 1234
                # threads = []

                # ## Receiver
                # t = threading.Thread(target=worker, args=(self.net, action[0][1]))
                # threads.append(t)
                # t.start()

                # time.sleep(3)

                # ## Sender
                # self.net.terms += makeTerm(self.net.get(self.cur_host.name), cmd='nc -w 3 ' + self.net.get(action[0][1].name).IP() + ' 1234 < ' + self.virus_path)

                self.virus_path = action[1].path + 'a.txt'
                self.cur_host = action[1]
            
            ## Check if game is done
            if self.observation.name == 'h10' and self.observation.nb_vulnerability == 0:
                # game done
                self.done = True
                self.win = True
                self.attacker_reward = self.observation.reward
                self.win_factor = -1
            else:
                self.done = False
                self.attacker_reward = self.observation.reward
        
        ## Else if attack was not successful
        else:
            if d_strategy == 'h':
                rand = random.random()*10 < action[0].defender_value[-1]
            elif d_strategy == 'm':
                rand = random.random()*10 > action[0].defender_value[-1]

            if  rand:
                # game done
                ## Attack failed and was detected by the defender (IDS)
                self.observation = action[0]
                self.done = True
                self.attacker_reward = 0
                self.defender_reward = action[0].reward
                self.win_factor = 1

            else:
                ## Attack failed and was not detecteds
                self.observation = action[0]
                self.done = False
                self.attacker_reward = 0
                self.defender_reward = 0

        return [self.observation, self.attacker_reward, self.defender_reward, self.done, self.win_factor, self.win_step, self.win]

    def step(self, action):
    
        if action[0][0].name == 'h10' and action[0][1].name == 'h10':
            ## This case where the virus was directly installed on the last Node
            ## The control Unit (PLC)
            ## So we end the Game..

            self.observation = action[0][1]
            self.attacker_reward += self.observation.reward
            self.done = True
        else:
            ## TODO: REMOVE BELOW COMMENT TO IMPLEMENT DEFENDER!!!!!!!
            # if action[1][1].defender_value[action[1][2]] < 10:
            #     ## Make sure Defense values does not exceed (10) and increment based on the choice
            #     action[1][1].defender_value[action[1][2]] += 1

            if action[0][1].attacker_value[action[0][2]] > action[0][1].defender_value[action[0][2]] or (action[0][1].attacker_value[action[0][2]] == 0 and action[0][1].defender_value[action[0][2]] == 0) :

                action[0][1].attacker_value[action[0][2]] += 1
                ## TODO: REMOVE BELOW COMMENT TO IMPLEMENT DEFENDER!!!!!!!
                # if action[0][1].defender_value[action[0][2]] != 0:
                #     action[0][1].defender_value[action[0][2]] -= 1

                self.observation = action[0][1]
                if action[0][1].name not in ['s', 's1', 's2', 's3', 's4']:

                    ## TODO: REMOVE BELOW COMMENT TO SEND VIRUS BETWEEN FILES!!!!!!!
                    # port = 1234
                    # threads = []

                    # ## Receiver
                    # t = threading.Thread(target=worker, args=(self.net, action[0][1]))
                    # threads.append(t)
                    # t.start()

                    # time.sleep(3)

                    # ## Sender
                    # self.net.terms += makeTerm(self.net.get(self.cur_host.name), cmd='nc -w 3 ' + self.net.get(action[0][1].name).IP() + ' 1234 < ' + self.virus_path)

                    self.virus_path = action[0][1].path + 'a.txt'
                    self.cur_host = action[0][1]

                if self.observation.name == 'h10':
                    self.done = True
                    self.attacker_reward += self.observation.reward
                    # self.defender_reward = -100
                else:
                    self.done = False
                    self.attacker_reward += self.observation.reward
                    # self.defender_reward = 0
            else:
                ## Attack not successful because attack values are much less
                ## We can make use of probability of detection..
                
                ## TODO: REMOVE BELOW COMMENT TO RETURN FUNCTIONALITY OF IDS (for Defender)
                # if random.randint(1, 10) > action[1][1].defender_value[-1]:
                #     ## This case if the random value above the detection value
                #     ## the attack is detected and the defender wins!
                    
                #     self.observation = action[0][0]
                #     self.done = True
                #     self.attacker_reward += -100
                #     self.defender_reward = 100
                

                ## TODO: here I didn't include the defender!!!!
                ## Fix this ELSE section to include the defender
                self.observation = action[0][0]
                self.done = False
                self.attacker_reward += 0



                ## TODO: REMOVE BELOW COMMENT TO RETURN FUNCTIONALITY OF IDS (for Defender)
                # else:
                #     ## This case where the attack goes undetected by the defender
                #     ## In other word when the Intrusion detection system does not catch the attack

                #     ## This is used to find if the next node the attacker has chance to attacker
                #     ## if the boolean value return True this means the game did not end
                #     ## The attacker can still attack
                #     ## If value return is False this means that the game ended the attacker
                #     ## have no chance to attack

                #     can_attack = False
                #     for a_v, d_v in zip(action[0][1].attacker_value, action[0][1].defender_value[:-1]):
                #         if a_v > d_v:
                #             can_attack = True

                #     if can_attack:
                #         self.observation = action[0][0]
                #         self.done = False
                #         self.attacker_reward += 0
                #         self.defender_reward = 0

                #     else:
                #         self.observation = action[0][0]
                #         self.done = True
                #         self.attacker_reward += -100
                #         self.defender_reward = 100

        ## [Node, AttackerReward, DefenderReward, Done]
        return [self.observation, self.attacker_reward, self.defender_reward, self.done]

    def reset(self):
        ## Reset state and other variables of the environment to the start state

        ## Set the virus location back to the START directory
        self.virus_path = 'Start/'
        ## TODO
        ## Clean all directories..
        # os.system('rm -r ' + self.virus_path + '*')

        ## THIS IS
        self.state = [  node(0,     's',    '',     [1],            [0, 0, 0, 0, 0],                                                [0, 0, 0, 0, 0],    [0, 0, 0, 0, 0, 0], 0, 0),     # Start state           0
        node(1,     's1',   '',     [2, 3, 4, 1],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [5, 4, 6, 2, 8, 9], 1, 50),    ##### Firewall A            1
        node(2,     'h1',   '',     [5, 2, 3, 4],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 6, 5, 6, 6, 7], 1, 100),   # Email Server          2
        node(3,     'h2',   '',     [5, 2, 3, 4],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [5, 4, 8, 7, 7, 8], 1, 100),   # Web Server            3
        node(4,     'h3',   '',     [5, 2, 3, 4],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 5, 4, 7, 8, 8], 1, 100),   # Database Server       4
        node(5,     's2',   '',     [6, 7, 8, 5],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 6, 2, 5, 6, 7], 1, 1000),  ##### Firewall B            5
        node(6,     'h4',   '',     [9, 6, 7, 8],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 2, 6, 5, 8, 2], 1, 100),   # Office Computer1      6
        node(7,     'h5',   '',     [9, 6, 7, 8],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [6, 1, 7, 4, 6, 2], 1, 100),   # Office Computer2      7
        node(8,     'h6',   '',     [9, 6, 7, 8],           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 5, 6, 2, 7, 2], 1, 100),   # Office Computer3      8
        node(9,     's3',   '',     [10, 11, 12, 9],        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [7, 1, 7, 8, 6, 2], 1, 2000),  ##### Firewall C            9
        node(10,    'h7',   '',     [13, 10, 11, 12],       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 2, 6, 7, 7, 3], 1, 3000),  # SCADA Server          10
        node(11,    'h8',   '',     [13, 10, 11, 12],       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [8, 8, 0, 1, 7, 3], 1, 3000),  # SCADA HMI             11
        node(12,    'h9',   '',     [13, 10, 11, 12],       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   [0, 0, 0, 0, 0],    [6, 7, 2, 8, 9, 3], 1, 3000),  # SCADA Historian       12
        node(13,    's4',   '',     [14, 13],               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],                                 [0, 0, 0, 0, 0],    [8, 6, 5, 2, 8, 3], 1, 4000),  ##### Firewall D (switch)   13
        node(14,    'h10',  '',     [14],                   [0, 0, 0, 0, 0],                                                [0, 0, 0, 0, 0],    [8, 0, 7, 3, 6, 3], 1, 5000),  # Field Device (PLC)    14
        node(15,    'e',    '',     [],                     [],                                                             [],                 [], 0, 0),
        ]

        self.done = False
        self.win = False
        self.reward = 0
        self.attacker_reward = 0
        self.defender_reward = 0

        self.win_factor = 1
        self.win_step = 0

        ## Used to create the appropriarte directories for the Hosts and Switches
        # self.make_directories()
        self.observation, self.d_observation = self.make_directories()
        self.cur_host = self.observation
        return self.observation, self.d_observation

    def render(self, mode='human', close=False):
        ## Gives out relevant information about the behavior of our environment so far
        result = ""
        for i in self.state:
            result += "State %2s: %3s - %23s - %20s - %24s - %10s\n" % (str(i.index), str(i.name), str(i.path), str(i.attacker_value), str(i.defender_value), str(i.reward))

        ## Return result of appropriate string format
        return result
